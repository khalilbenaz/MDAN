import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';
import { mergeLayers, customize, resolveCustomization, renderCustomization } from '../tools/lib/customize.js';
import { install, resolveOptions } from '../tools/cli/commands/install.js';
import { startServer } from '../tools/mcp/server.js';
import { ContextGraph } from '../tools/cli/lib/context-graph.js';

const tmp = () => mkdtempSync(join(tmpdir(), 'mdan-cust-'));

test('layers merge: empty values never override, arrays accumulate, later layer wins', () => {
  const merged = mergeLayers(
    { persona: { role: 'Architect', principles: ['KISS'] }, memories: [] },
    { persona: { role: '', principles: ['Boring tech'] }, memories: ['Uses .NET 10'] },
    { persona: { communication_style: 'Terse' }, memories: ['Uses .NET 10'] },
  );
  assert.deepEqual(merged, {
    persona: { role: 'Architect', principles: ['KISS', 'Boring tech'], communication_style: 'Terse' },
    memories: ['Uses .NET 10'],
  });
});

test('team and user layers are written, git-ignored for user, and rendered for the agent', () => {
  const root = tmp();
  install(root, resolveOptions({ lang: 'en', user: 't', modules: 'fintech' }, null));
  customize(root, 'risk-manager', 'team', { memories: ['BAM tier limits apply'] });
  customize(root, 'risk-manager', 'user', { persona: { communication_style: 'Bullet points only' } });
  assert.match(readFileSync(join(root, '_mdan/custom/.gitignore'), 'utf-8'), /\*\.user\.yaml/);

  const resolved = resolveCustomization(root, root, 'risk-manager', 'fintech');
  assert.deepEqual(resolved.layers, { shipped: true, team: true, user: true });
  assert.deepEqual(resolved.merged.memories, ['BAM tier limits apply']);
  assert.match(renderCustomization(resolved), /shipped < team < user/);
  assert.throws(() => customize(root, '../x', 'team', {}), /Invalid agent name/);

  // Reinstalling never touches _mdan/custom.
  install(root, resolveOptions({ lang: 'en', user: 't', modules: 'fintech' }, null));
  assert.ok(existsSync(join(root, '_mdan/custom/risk-manager.user.yaml')));
});

test('graph highlight marks a decision and its downstream nodes', () => {
  const g = new ContextGraph();
  for (const id of ['DR-001', 'arch', 'epics', 'other']) g.addNode({ id });
  g.addEdge({ source: 'DR-001', target: 'arch', relation: 'impacts' });
  g.addEdge({ source: 'arch', target: 'epics', relation: 'input_to' });
  const m = g.toMermaid({ highlight: ['DR-001', ...g.getDownstream('DR-001').map(n => n.id)] });
  assert.match(m, /class DR-001,arch,epics impacted/);
});

test('HTTP: token required off loopback, bearer enforced, resources and health served', async () => {
  const root = tmp();
  install(root, resolveOptions({ lang: 'en', user: 't' }, null));
  await assert.rejects(startServer({ transport: 'http', port: 0, host: '0.0.0.0', projectRoot: root, token: '' }), /Refusing to expose/);

  const http = await startServer({ transport: 'http', port: 0, projectRoot: root, token: 's3cret' });
  try {
    const url = new URL(`http://127.0.0.1:${http.address().port}/mcp`);
    const denied = await fetch(url, { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{}' });
    assert.equal(denied.status, 401);

    const c = new Client({ name: 't', version: '1' });
    await c.connect(new StreamableHTTPClientTransport(url, { requestInit: { headers: { authorization: 'Bearer s3cret' } } }));
    const { resources } = await c.listResources();
    assert.ok(resources.some(r => r.uri === 'mdan://workflow/create-prd'));
    assert.ok(resources.some(r => r.uri === 'mdan://agent/mdan-master'));
    const wf = await c.readResource({ uri: 'mdan://workflow/create-prd' });
    assert.match(wf.contents[0].text, /create-prd/);
    const health = JSON.parse((await c.readResource({ uri: 'mdan://health' })).contents[0].text);
    assert.equal(health.next.workflow, 'create-product-brief');
    await c.close();
  } finally {
    http.close();
  }
});
