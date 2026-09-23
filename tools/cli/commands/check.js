import { parseArgs } from 'node:util';
import { checkProject, detectScale, SCALES } from '../../lib/quality.js';
import { projectRootFromEnv } from '../../lib/paths.js';

const ICON = { PASS: '✅', CONCERNS: '⚠️ ', FAIL: '❌', error: '❌', warning: '⚠️ ', info: 'ℹ️ ' };

export default async function check(argv) {
  const { values, positionals } = parseArgs({
    args: argv,
    allowPositionals: true,
    options: { scale: { type: 'string' }, json: { type: 'boolean' }, help: { type: 'boolean', short: 'h' } },
  });
  if (values.help) {
    return console.log(`Usage: mdan check [artifact.md ...] [--scale ${SCALES.join('|')}] [--json]\n\nQuality gate on planning artifacts. Exit code 1 on FAIL (usable in CI).`);
  }
  const root = projectRootFromEnv();
  if (values.scale && !SCALES.includes(values.scale)) throw new Error(`Invalid scale '${values.scale}'`);
  const { scale, source } = values.scale ? { scale: values.scale, source: 'flag' } : detectScale(root);
  const report = checkProject(root, { scale, paths: positionals.length ? positionals : null });

  if (values.json) console.log(JSON.stringify(report, null, 2));
  else {
    console.log(`Scale: ${scale} (${source})\n`);
    if (!report.results.length) console.log('No artifact found (register them with mdan_state_update or pass paths).');
    for (const r of report.results) {
      console.log(`${ICON[r.decision]} ${r.path} [${r.kind}] — ${r.decision}, score ${r.score}`);
      for (const i of r.issues) console.log(`     ${ICON[i.level]} ${i.rule}: ${i.message}`);
    }
    console.log(`\nGate: ${ICON[report.decision]} ${report.decision}`);
  }
  if (report.decision === 'FAIL') process.exitCode = 1;
}
