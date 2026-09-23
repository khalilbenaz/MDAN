import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';
import { install, resolveOptions } from '../tools/cli/commands/install.js';
import { startServer } from '../tools/mcp/server.js';

const bin = fileURLToPath(new URL('../tools/mcp/bin.js', import.meta.url));
let project, claude, client;

const call = async (name, args = {}) => {
  const r = await client.callTool({ name, arguments: args });
  return { error: Boolean(r.isError), text: r.content[0].text };
};

async function connect(env) {
  const c = new Client({ name: 'test', version: '1' });
  await c.connect(new StdioClientTransport({ command: process.execPath, args: [bin], env: { ...process.env, ...env }, stderr: 'ignore' }));
  return c;
}

before(async () => {
  project = mkdtempSync(join(tmpdir(), 'mdan-mcp-'));
  install(project, resolveOptions({ lang: 'en', user: 'tester', modules: 'fintech' }, null));
  claude = mkdtempSync(join(tmpdir(), 'mdan-claude-'));
  mkdirSync(join(claude, 'skills/react-testing'), { recursive: true });
  writeFileSync(join(claude, 'skills/react-testing/SKILL.md'), '---\nname: react-testing\ndescription: Test React components\n---\nbody');
  client = await connect({ MDAN_PROJECT_ROOT: project, MDAN_CLAUDE_DIR: claude });
});

after(async () => { await client?.close(); });

test('server exposes generic tools with real input schemas', async () => {
  const { tools } = await client.listTools();
  const names = tools.map(t => t.name);
  for (const n of ['mdan_run_workflow', 'mdan_consult_agent', 'mdan_party_mode', 'mdan_create_decision_record', 'mdan_graph_stale', 'mdan_ecosystem_search']) {
    assert.ok(names.includes(n), n);
  }
  const run = tools.find(t => t.name === 'mdan_run_workflow');
  assert.ok(run.inputSchema.properties.name.enum.includes('create-prd'));
  assert.deepEqual(run.inputSchema.required, ['name']);
});

test('workflows and agents are also MCP prompts', async () => {
  const { prompts } = await client.listPrompts();
  assert.ok(prompts.some(p => p.name === 'create-prd'));
  assert.ok(prompts.some(p => p.name === 'agent-risk-manager'));
  const p = await client.getPrompt({ name: 'create-prd', arguments: { topic: 'Wallet' } });
  assert.match(p.messages[0].content.text, /\*\*Topic:\*\* Wallet/);
});

test('run_workflow passes the topic and inlines the wizard', async () => {
  const r = await call('mdan_run_workflow', { name: 'create-prd', topic: 'Payments' });
  assert.equal(r.error, false);
  assert.match(r.text, /\*\*Topic:\*\* Payments/);
  assert.match(r.text, /_mdan\/core\/rules\.md|Mandatory rules/);
});

test('yaml workflows include the workflow engine', async () => {
  const r = await call('mdan_run_workflow', { name: 'code-review' });
  assert.match(r.text, /workflow\.xml/);
});

test('invalid arguments are errors, not crashes', async () => {
  const bad = await client.callTool({ name: 'mdan_run_workflow', arguments: { name: 'nope' } });
  assert.equal(bad.isError, true);
  assert.equal((await call('mdan_list_workflows')).error, false);
});

test('path traversal is refused', async () => {
  assert.equal((await call('mdan_ecosystem_read', { kind: 'skill', name: '../../etc' })).error, true);
  assert.equal((await call('mdan_create_decision_record', { id: '../../evil', topic: 't', decision: 'd', rationale: 'r' })).error, true);
  assert.equal((await call('mdan_graph_add_node', { id: 'x', path: '../../outside.md' })).error, true);
});

test('decision records get sequential ids and land in the graph', async () => {
  await call('mdan_graph_add_node', { id: 'arch', path: 'docs/arch.md' });
  const a = await call('mdan_create_decision_record', { topic: 'API', decision: 'REST', rationale: 'simple', impacts: ['arch', 'ghost'] });
  const b = await call('mdan_create_decision_record', { topic: 'DB', decision: 'SQL', rationale: 'acid' });
  assert.match(a.text, /DR-001/);
  assert.match(a.text, /ghost/);
  assert.match(b.text, /DR-002/);
  assert.ok(existsSync(join(project, 'mdan_output/decisions/DR-001.json')));
  const graph = JSON.parse(readFileSync(join(project, '_mdan/state/context-graph.json'), 'utf-8'));
  assert.ok(graph.edges.some(e => e.source === 'DR-001' && e.target === 'arch' && e.relation === 'impacts'));
  assert.match((await call('mdan_graph_impact', { nodeId: 'DR-001' })).text, /arch/);
});

test('ecosystem search ranks by frontmatter', async () => {
  const r = await call('mdan_ecosystem_search', { kind: 'skill', query: 'react components' });
  assert.match(r.text, /react-testing\*\* — Test React components/);
});

test('party mode validates agent names', async () => {
  assert.equal((await call('mdan_party_mode', { mode: 'debate', agents: ['nobody'] })).error, true);
  const ok = await call('mdan_party_mode', { mode: 'debate', topic: 'x', agents: ['risk-manager'] });
  assert.match(ok.text, /mdan_create_decision_record/);
});

test('without an install the bundled content is served (Glama / npx)', async () => {
  const c = await connect({ MDAN_PROJECT_ROOT: mkdtempSync(join(tmpdir(), 'mdan-empty-')) });
  const { tools } = await c.listTools();
  assert.ok(tools.find(t => t.name === 'mdan_run_workflow').inputSchema.properties.name.enum.length > 5);
  await c.close();
});

test('streamable HTTP transport', async () => {
  const http = await startServer({ transport: 'http', port: 0, projectRoot: project });
  try {
    const { port } = http.address();
    const health = await fetch(`http://127.0.0.1:${port}/health`).then(r => r.json());
    assert.equal(health.status, 'ok');
    const c = new Client({ name: 'test', version: '1' });
    await c.connect(new StreamableHTTPClientTransport(new URL(`http://127.0.0.1:${port}/mcp`)));
    assert.ok((await c.listTools()).tools.length >= 10);
    await c.close();
  } finally {
    http.close();
  }
});

test('state tools drive resume and next-step, artifacts land in the graph', async () => {
  await call('mdan_state_update', { action: 'start', workflow: 'create-prd' });
  await call('mdan_state_update', { action: 'step', workflow: 'create-prd', step: 'step-05-domain', stepFile: 'steps/step-05-domain.md' });
  const resume = await call('mdan_run_workflow', { name: 'create-prd' });
  assert.match(resume.text, /Resume:.*step-05-domain/);

  mkdirSync(join(project, 'docs'), { recursive: true });
  writeFileSync(join(project, 'docs/prd.md'), '# PRD');
  const done = await call('mdan_state_update', { action: 'complete', workflow: 'create-prd', artifacts: [{ id: 'prd', path: 'docs/prd.md' }] });
  assert.match(done.text, /completed/);
  assert.match(done.text, /Next recommended/);
  const status = JSON.parse((await call('mdan_status')).text);
  assert.equal(status.current, null);
  assert.ok(status.artifacts.some(a => a.id === 'prd'));
  const graph = JSON.parse(readFileSync(join(project, '_mdan/state/context-graph.json'), 'utf-8'));
  assert.ok(graph.nodes.prd.hash, 'artifact hash recorded');
});

test('agent memory is injected when the agent is consulted', async () => {
  await call('mdan_memory_remember', { agent: 'risk-manager', content: 'Client exige plafonds BAM niveau 3', type: 'context', confidence: 1 });
  const r = await call('mdan_consult_agent', { name: 'risk-manager', question: 'plafonds ?' });
  assert.match(r.text, /Client exige plafonds BAM niveau 3/);
  const recalled = JSON.parse((await call('mdan_memory_recall', { agent: 'risk-manager' })).text);
  assert.equal(recalled.memories.length, 1);
  assert.equal((await call('mdan_memory_remember', { agent: '../x', content: 'y' })).error, true);
});

test('quality tools: check, trace and scope are exposed', async () => {
  writeFileSync(join(project, 'docs/prd.md'), '# PRD\n\n## Functional Requirements\n- FR1: A user can log in\n\n## Non-Functional Requirements\n- NFR1: login p95 < 300 ms\n');
  const check = JSON.parse((await call('mdan_check', { paths: ['docs/prd.md'], scale: 'team' })).text);
  assert.equal(check.results[0].kind, 'prd');
  const trace = JSON.parse((await call('mdan_trace', {})).text);
  assert.equal(trace.rows[0].id, 'FR1');
  const scope = JSON.parse((await call('mdan_estimate_scope', { description: 'rename a variable', files: ['a.js'] })).text);
  assert.equal(scope.route, 'oneshot');
  assert.equal((await call('mdan_check', { paths: ['../../etc/passwd'] })).error, true);
});

test('`mdan` without a command, launched by a program, serves MCP (Glama / mcp-proxy)', async () => {
  const cli = fileURLToPath(new URL('../tools/cli/index.js', import.meta.url));
  const c = new Client({ name: 'test', version: '1' });
  await c.connect(new StdioClientTransport({ command: process.execPath, args: [cli], env: { ...process.env, MDAN_PROJECT_ROOT: project }, stderr: 'ignore' }));
  assert.ok((await c.listTools()).tools.some(t => t.name === 'mdan_run_workflow'));
  await c.close();
});
