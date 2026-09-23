import { ContextGraph, graphPathFor } from '../lib/context-graph.js';
import { projectRootFromEnv } from '../../lib/paths.js';

export default async function stale(args) {
  if (args.includes('--help') || args.includes('-h')) {
    return console.log('Usage: mdan stale [--touch <id>]\n\nLists artifacts modified since they were registered and the downstream artifacts to review.\n--touch <id> marks an artifact as reviewed (records its current hash).');
  }
  const root = projectRootFromEnv();
  const graphPath = graphPathFor(root);

  const touchIdx = args.indexOf('--touch');
  if (touchIdx !== -1) {
    const id = args[touchIdx + 1];
    if (!id) throw new Error('--touch requires a node id');
    ContextGraph.update(graphPath, g => g.touch(id, root));
    return console.log(`Marked '${id}' as up to date.`);
  }

  const { changed, stale: toReview } = ContextGraph.load(graphPath).getStale(root);
  if (!changed.length) return console.log('No artifact changed since registration.');
  console.log('Changed since registration:');
  for (const n of changed) console.log(`  ✎ ${n.id} → ${n.path}`);
  console.log(`\nTo review (${toReview.length}):`);
  for (const s of toReview) console.log(`  ⚠ ${s.node.id} (because ${s.because} changed)`);
  process.exitCode = toReview.length ? 2 : 0;
}
