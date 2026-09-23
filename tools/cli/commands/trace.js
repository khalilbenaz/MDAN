import { traceability, registerTrace } from '../../lib/quality.js';
import { projectRootFromEnv } from '../../lib/paths.js';
import { ContextGraph, graphPathFor } from '../lib/context-graph.js';

const pct = n => `${Math.round(n * 100)}%`;

export default async function trace(args) {
  if (args.includes('--help') || args.includes('-h')) {
    return console.log('Usage: mdan trace [--graph] [--json]\n\nRequirement (FR/NFR) → stories → tests matrix. --graph writes it into the context graph. Exit 1 on FAIL.');
  }
  const root = projectRootFromEnv();
  const t = traceability(root);
  const added = args.includes('--graph') ? registerTrace(root, t, ContextGraph, graphPathFor(root)) : 0;

  if (args.includes('--json')) console.log(JSON.stringify({ ...t, graphNodesAdded: added }, null, 2));
  else {
    console.log(`PRD: ${t.prd}${t.epics ? ` · Epics: ${t.epics}` : ''} · scale ${t.scale}\n`);
    console.log('| Req | Stories | Tests |\n|-----|---------|-------|');
    for (const r of t.rows) console.log(`| ${r.id} | ${r.stories.join(', ') || '❌'} | ${r.tests.length ? r.tests.length : '—'} |`);
    console.log(`\nFR → story coverage: ${pct(t.coverage.stories)} · requirement → test coverage: ${pct(t.coverage.tests)} (threshold ${pct(t.coverage.threshold)})`);
    if (t.untestedStories.length) console.log(`Untested stories: ${t.untestedStories.join(', ')}`);
    if (added) console.log(`${added} node(s) added to the context graph.`);
    console.log(`Gate: ${t.decision}`);
  }
  if (t.decision === 'FAIL') process.exitCode = 1;
}
