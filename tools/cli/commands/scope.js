import { parseArgs } from 'node:util';
import { estimateScope } from '../../lib/scope.js';
import { projectRootFromEnv } from '../../lib/paths.js';

export default async function scope(argv) {
  const { values, positionals } = parseArgs({
    args: argv,
    allowPositionals: true,
    options: { files: { type: 'string' }, artifacts: { type: 'string' }, json: { type: 'boolean' }, help: { type: 'boolean', short: 'h' } },
  });
  if (values.help || !positionals.length) {
    console.log('Usage: mdan scope "<change description>" [--files a.js,b.js] [--artifacts prd,architecture] [--json]\n\nRecommends oneshot (quick-dev), spec (quick-spec) or full planning.');
    if (!values.help) process.exitCode = 1;
    return;
  }
  const r = estimateScope(projectRootFromEnv(), {
    description: positionals.join(' '),
    files: values.files ? values.files.split(',') : [],
    artifacts: values.artifacts ? values.artifacts.split(',') : [],
  });
  if (values.json) return console.log(JSON.stringify(r, null, 2));
  console.log(`Route: ${r.route.toUpperCase()} — ${r.label}\nScale: ${r.scale} · points: ${r.points}`);
  for (const reason of r.reasons) console.log(`  - ${reason}`);
  console.log(`\n👉 /mdan-${r.workflow}`);
}
