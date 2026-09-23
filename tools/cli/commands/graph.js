import { parseArgs } from 'node:util';
import { resolve } from 'node:path';
import { ContextGraph, graphPathFor } from '../lib/context-graph.js';
import { projectRootFromEnv } from '../../lib/paths.js';
import { writeFileAtomic } from '../../lib/fs-atomic.js';

export const help = `Usage: mdan graph [--json | --html <file>] [--since <node-id>]

Prints the context graph as Mermaid (default), raw JSON, or writes a standalone HTML page.
--since highlights a node (e.g. a decision record) and everything downstream of it.`;

export default async function graph(argv) {
  const { values } = parseArgs({
    args: argv,
    options: { json: { type: 'boolean' }, html: { type: 'string' }, since: { type: 'string' }, help: { type: 'boolean', short: 'h' } },
  });
  if (values.help) return console.log(help);

  const g = ContextGraph.load(graphPathFor(projectRootFromEnv()));
  const nodeCount = Object.keys(g.nodes).length;

  if (values.json) return console.log(JSON.stringify(g.toJSON(), null, 2));
  if (nodeCount === 0) return console.log('Context graph is empty. Run workflows to populate it.');

  let highlight = [];
  if (values.since) {
    if (!g.getNode(values.since)) throw new Error(`Node '${values.since}' not found`);
    highlight = [values.since, ...g.getDownstream(values.since).map(n => n.id)];
  }

  if (values.html) {
    const out = resolve(values.html);
    writeFileAtomic(out, g.toHtml('MDAN Context Graph', { highlight }));
    return console.log(`Wrote ${out} (${nodeCount} nodes, ${g.edges.length} edges)`);
  }
  console.log(`# MDAN Context Graph (${nodeCount} nodes, ${g.edges.length} edges)\n`);
  console.log('```mermaid');
  console.log(g.toMermaid({ highlight }));
  console.log('```');
}
