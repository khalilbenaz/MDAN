import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { ResourceTemplate } from '@modelcontextprotocol/sdk/server/mcp.js';
import { ContextGraph, graphPathFor } from '../cli/lib/context-graph.js';
import { safeJoin, VERSION } from '../lib/paths.js';
import { loadState, summarize } from '../lib/state.js';
import { checkProject } from '../lib/quality.js';
import { listSidecars } from '../lib/memory.js';

const json = (uri, value) => ({ contents: [{ uri, mimeType: 'application/json', text: typeof value === 'string' ? value : JSON.stringify(value, null, 2) }] });

export function registerResources(server, discovery, projectRoot, contentRoot = projectRoot) {
  server.registerResource('state', 'mdan://state', {
    title: 'MDAN project state',
    description: 'MDAN-STATE.json: completed workflows, artifacts, decisions',
    mimeType: 'application/json',
  }, async uri => {
    const statePath = join(projectRoot, '_mdan/state/MDAN-STATE.json');
    return json(uri.href, existsSync(statePath) ? await readFile(statePath, 'utf-8') : '{}');
  });

  server.registerResource('config', 'mdan://config', {
    title: 'MDAN configuration',
    description: 'Installed modules, their config.yaml and counts',
    mimeType: 'application/json',
  }, async uri => {
    const configs = {};
    for (const mod of discovery.modules) {
      const configPath = join(projectRoot, '_mdan', mod, 'config.yaml');
      if (existsSync(configPath)) configs[mod] = await readFile(configPath, 'utf-8');
    }
    return json(uri.href, {
      projectRoot,
      manifest: discovery.manifest,
      modules: discovery.modules,
      configs,
      workflowCount: discovery.workflows.length,
      agentCount: discovery.agents.length,
    });
  });

  server.registerResource('graph', 'mdan://graph', {
    title: 'MDAN context graph',
    description: 'Artifacts and decisions with their relationships',
    mimeType: 'application/json',
  }, async uri => json(uri.href, ContextGraph.load(graphPathFor(projectRoot)).toJSON()));

  const markdown = (uri, textValue) => ({ contents: [{ uri, mimeType: 'text/markdown', text: textValue }] });

  server.registerResource('workflow', new ResourceTemplate('mdan://workflow/{name}', {
    list: async () => ({ resources: discovery.workflows.map(w => ({ uri: `mdan://workflow/${w.name}`, name: w.name, description: w.description, mimeType: 'text/markdown' })) }),
  }), { title: 'MDAN workflow', description: 'Wizard / workflow definition' }, async (uri, { name }) => {
    const wf = discovery.workflows.find(w => w.name === name);
    if (!wf) throw new Error(`Unknown workflow '${name}'`);
    return markdown(uri.href, await readFile(safeJoin(contentRoot, wf.path), 'utf-8'));
  });

  server.registerResource('agent', new ResourceTemplate('mdan://agent/{name}', {
    list: async () => ({ resources: discovery.agents.map(a => ({ uri: `mdan://agent/${a.name}`, name: `${a.icon} ${a.displayName}`, description: a.title, mimeType: 'text/markdown' })) }),
  }), { title: 'MDAN agent', description: 'Agent persona definition' }, async (uri, { name }) => {
    const agent = discovery.agents.find(a => a.name === name);
    if (!agent) throw new Error(`Unknown agent '${name}'`);
    return markdown(uri.href, await readFile(safeJoin(contentRoot, agent.path), 'utf-8'));
  });

  server.registerResource('health', 'mdan://health', {
    title: 'MDAN project health',
    description: 'One-call health report: progress, next step, quality gate, stale artifacts, agent memories',
    mimeType: 'application/json',
  }, async uri => {
    const installed = discovery.workflows.map(w => w.name);
    const status = summarize(loadState(projectRoot), installed);
    const graph = ContextGraph.load(graphPathFor(projectRoot));
    let quality;
    try {
      const q = checkProject(projectRoot);
      quality = { decision: q.decision, scale: q.scale, artifacts: q.results.map(r => ({ path: r.path, decision: r.decision, score: r.score })) };
    } catch (err) {
      quality = { error: err.message };
    }
    return json(uri.href, {
      version: VERSION,
      current: status.current,
      next: status.next,
      completed: status.phases.flatMap(p => p.workflows.filter(w => w.done).map(w => w.name)),
      quality,
      graph: { nodes: Object.keys(graph.nodes).length, edges: graph.edges.length, stale: graph.getStale(projectRoot).stale.map(s => s.node.id) },
      agentsWithMemory: listSidecars(projectRoot),
    });
  });
}
