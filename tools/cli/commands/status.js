import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { loadState, summarize } from '../../lib/state.js';
import { parseCsv } from '../../lib/csv.js';
import { projectRootFromEnv } from '../../lib/paths.js';
import { ContextGraph, graphPathFor } from '../lib/context-graph.js';

export default async function status(args) {
  if (args.includes('--help') || args.includes('-h')) {
    return console.log('Usage: mdan status [--json]\n\nWhere the project is in the method: current workflow and step, completed phases, artifacts, decisions, next step.');
  }
  const root = projectRootFromEnv();
  const manifest = join(root, '_mdan/_config/workflow-manifest.csv');
  const installed = existsSync(manifest) ? parseCsv(readFileSync(manifest, 'utf-8')).map(w => w.name) : null;
  const s = summarize(loadState(root), installed);
  const stale = ContextGraph.load(graphPathFor(root)).getStale(root).stale;

  if (args.includes('--json')) return console.log(JSON.stringify({ ...s, stale: stale.map(x => x.node.id) }, null, 2));

  console.log(`\n📁 ${s.project}\n`);
  if (s.current) console.log(`⏯️  En cours : ${s.current.name}${s.current.step ? ` — étape ${s.current.step}` : ''}\n`);
  for (const p of s.phases) {
    if (!p.workflows.length) continue;
    console.log(`  ${p.phase.padEnd(12)} ${p.workflows.map(w => `${w.done ? '✅' : '⬜'} ${w.name}`).join('   ')}`);
  }
  if (s.artifacts.length) {
    console.log('\n📄 Artifacts :');
    for (const a of s.artifacts) console.log(`   ${a.id} → ${a.path}`);
  }
  if (s.decisions.length) {
    console.log('\n⚖️  Décisions :');
    for (const d of s.decisions) console.log(`   ${d.id} — ${d.topic}`);
  }
  if (stale.length) console.log(`\n⚠️  ${stale.length} artifact(s) à revoir (mdan stale)`);
  if (s.next) {
    console.log(`\n👉 Prochaine étape : /mdan-${s.next.workflow}${s.next.reason === 'resume' ? ' (reprise)' : ''}`);
  } else {
    console.log('\n🎉 Toutes les étapes requises sont terminées.');
  }
}
