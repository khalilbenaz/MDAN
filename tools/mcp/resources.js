import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { ContextGraph, graphPathFor } from '../cli/lib/context-graph.js';

const json = (uri, value) => ({ contents: [{ uri, mimeType: 'application/json', text: typeof value === 'string' ? value : JSON.stringify(value, null, 2) }] });

export function registerResources(server, discovery, projectRoot) {
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
}
