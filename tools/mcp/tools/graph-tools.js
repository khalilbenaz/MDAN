import { z } from 'zod';
import { ContextGraph, graphPathFor, RELATIONS, NODE_TYPES } from '../../cli/lib/context-graph.js';
import { safeJoin } from '../../lib/paths.js';
import { safe, text } from '../util.js';

export function registerGraphTools(server, projectRoot) {
  const graphPath = graphPathFor(projectRoot);

  server.registerTool('mdan_graph_add_node', {
    description: 'Add or update an artifact node in the MDAN context graph (records the file hash for staleness checks)',
    inputSchema: {
      id: z.string().describe('Unique node ID (e.g., prd-001)'),
      type: z.enum(NODE_TYPES).default('artifact').describe('Node type'),
      path: z.string().optional().describe('Artifact path relative to the project root'),
      workflow: z.string().optional().describe('Workflow that created this artifact'),
      agent: z.string().optional().describe('Agent that created this artifact'),
    },
  }, safe(async ({ id, type, path, workflow, agent }) => {
    if (path) safeJoin(projectRoot, path);
    const node = ContextGraph.update(graphPath, g =>
      g.addNode({ id, type, path: path || '', created_by: { workflow, agent } }, projectRoot));
    return text(`Node '${node.id}' saved${node.hash ? ' (hash recorded)' : ''}.`);
  }));

  server.registerTool('mdan_graph_add_edge', {
    description: 'Add a relationship between two nodes of the context graph (cycles are rejected)',
    inputSchema: {
      source: z.string().describe('Source node ID'),
      target: z.string().describe('Target node ID'),
      relation: z.enum(RELATIONS).default('input_to').describe('Relation type'),
    },
  }, safe(async ({ source, target, relation }) => {
    ContextGraph.update(graphPath, g => g.addEdge({ source, target, relation }));
    return text(`Edge ${source} --${relation}--> ${target} added.`);
  }));

  server.registerTool('mdan_graph_impact', {
    description: 'Upstream dependencies and downstream impact of an artifact in the context graph',
    inputSchema: { nodeId: z.string().describe('Node ID to analyze') },
    annotations: { readOnlyHint: true },
  }, safe(async ({ nodeId }) => {
    const graph = ContextGraph.load(graphPath);
    if (!graph.getNode(nodeId)) throw new Error(`Node '${nodeId}' not found. Known: ${Object.keys(graph.nodes).join(', ') || '(empty graph)'}`);
    const fmt = list => list.length ? list.map(n => `- ${n.id} (${n.type}) → ${n.path || 'N/A'}`).join('\n') : '(none)';
    return text(`# Impact Analysis: ${nodeId}\n\n## Upstream\n${fmt(graph.getUpstream(nodeId))}\n\n## Downstream\n${fmt(graph.getDownstream(nodeId))}`);
  }));

  server.registerTool('mdan_graph_stale', {
    description: 'List artifacts modified since registration and the downstream artifacts that must be reviewed',
    annotations: { readOnlyHint: true },
  }, safe(async () => {
    const { changed, stale } = ContextGraph.load(graphPath).getStale(projectRoot);
    if (!changed.length) return text('No artifact changed since registration.');
    return text(`## Changed\n${changed.map(n => `- ${n.id} → ${n.path}`).join('\n')}\n\n## To review\n` +
      (stale.map(s => `- ${s.node.id} (because ${s.because} changed)`).join('\n') || '(none)'));
  }));

  server.registerTool('mdan_graph_visualize', {
    description: 'Mermaid diagram of the context graph',
    annotations: { readOnlyHint: true },
  }, safe(async () => text(ContextGraph.load(graphPath).toMermaid())));
}
