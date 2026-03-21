import { join } from 'node:path';
import { ContextGraph } from '../lib/context-graph.js';

export default async function impact(args) {
  const nodeId = args[0];
  if (!nodeId) {
    console.log('Usage: mdan impact <artifact-id>');
    console.log('\nAnalyzes downstream impact of an artifact in the context graph.');
    process.exit(1);
  }

  const projectRoot = process.env.MDAN_PROJECT_ROOT || process.cwd();
  const graphPath = join(projectRoot, '_mdan/state/context-graph.json');
  const graph = ContextGraph.load(graphPath);

  const node = graph.getNode(nodeId);
  if (!node) {
    console.error(`Node '${nodeId}' not found in context graph.`);
    console.log('\nAvailable nodes:');
    for (const [id, n] of Object.entries(graph.nodes)) {
      console.log(`  ${id} (${n.type}) → ${n.path || 'N/A'}`);
    }
    process.exit(1);
  }

  console.log(`\n📊 Impact Analysis: ${nodeId}`);
  console.log(`   Type: ${node.type}`);
  console.log(`   Path: ${node.path || 'N/A'}`);
  console.log(`   Created: ${node.created_at}`);

  // Upstream
  const upstream = graph.getUpstream(nodeId);
  console.log(`\n⬆️  Upstream dependencies (${upstream.length}):`);
  if (upstream.length === 0) {
    console.log('   (none — this is a root artifact)');
  } else {
    for (const n of upstream) {
      const edges = graph.edges.filter(e => e.target === nodeId && e.source === n.id);
      const relations = edges.map(e => e.relation).join(', ');
      console.log(`   ${n.id} (${n.type}) --[${relations}]--> ${nodeId}`);
    }
  }

  // Downstream
  const downstream = graph.getDownstream(nodeId);
  console.log(`\n⬇️  Downstream impact (${downstream.length}):`);
  if (downstream.length === 0) {
    console.log('   (none — no downstream dependencies)');
  } else {
    for (const n of downstream) {
      const edges = graph.edges.filter(e => e.source === nodeId && e.target === n.id);
      const relations = edges.map(e => e.relation).join(', ');
      console.log(`   ${nodeId} --[${relations}]--> ${n.id} (${n.type})`);
    }
  }

  // Direct edges
  const allEdges = graph.getEdgesFor(nodeId);
  console.log(`\n🔗 All relationships (${allEdges.length}):`);
  for (const e of allEdges) {
    const direction = e.source === nodeId ? '→' : '←';
    const other = e.source === nodeId ? e.target : e.source;
    console.log(`   ${direction} ${other} (${e.relation})`);
  }
}
