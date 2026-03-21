import { join } from 'node:path';
import { ContextGraph } from '../lib/context-graph.js';

export default async function graph(args) {
  const projectRoot = process.env.MDAN_PROJECT_ROOT || process.cwd();
  const graphPath = join(projectRoot, '_mdan/state/context-graph.json');
  const graph = ContextGraph.load(graphPath);

  const nodeCount = Object.keys(graph.nodes).length;
  const edgeCount = graph.edges.length;

  if (nodeCount === 0) {
    console.log('Context graph is empty. Run workflows to populate it.');
    return;
  }

  const format = args.includes('--json') ? 'json' : 'mermaid';

  if (format === 'json') {
    console.log(JSON.stringify(graph.toJSON(), null, 2));
  } else {
    console.log(`# MDAN Context Graph (${nodeCount} nodes, ${edgeCount} edges)\n`);
    console.log('```mermaid');
    console.log(graph.toMermaid());
    console.log('```');
  }
}
