import { ContextGraph, graphPathFor } from '../lib/context-graph.js';
import { projectRootFromEnv } from '../../lib/paths.js';

export default async function impact(args) {
  const nodeId = args[0];
  if (!nodeId || nodeId === '--help' || nodeId === '-h') {
    console.log('Usage: mdan impact <artifact-id>\n\nAnalyzes upstream dependencies and downstream impact of an artifact in the context graph.');
    if (!nodeId) process.exitCode = 1;
    return;
  }

  const graph = ContextGraph.load(graphPathFor(projectRootFromEnv()));
  const node = graph.getNode(nodeId);
  if (!node) {
    const known = Object.values(graph.nodes).map(n => `  ${n.id} (${n.type}) → ${n.path || 'N/A'}`).join('\n');
    throw new Error(`Node '${nodeId}' not found in context graph.${known ? `\nAvailable nodes:\n${known}` : ' The graph is empty.'}`);
  }

  console.log(`\n📊 Impact Analysis: ${nodeId}`);
  console.log(`   Type: ${node.type}`);
  console.log(`   Path: ${node.path || 'N/A'}`);
  console.log(`   Created: ${node.created_at}`);

  const relations = (source, target) => graph.edges
    .filter(e => e.source === source && e.target === target).map(e => e.relation).join(', ');

  const upstream = graph.getUpstream(nodeId);
  console.log(`\n⬆️  Upstream dependencies (${upstream.length}):`);
  if (!upstream.length) console.log('   (none — this is a root artifact)');
  for (const n of upstream) {
    const rel = relations(n.id, nodeId);
    console.log(`   ${n.id} (${n.type})${rel ? ` --[${rel}]--> ${nodeId}` : ' (indirect)'}`);
  }

  const downstream = graph.getDownstream(nodeId);
  console.log(`\n⬇️  Downstream impact (${downstream.length}):`);
  if (!downstream.length) console.log('   (none — no downstream dependencies)');
  for (const n of downstream) {
    const rel = relations(nodeId, n.id);
    console.log(`   ${rel ? `${nodeId} --[${rel}]--> ` : '(indirect) '}${n.id} (${n.type})`);
  }
}
