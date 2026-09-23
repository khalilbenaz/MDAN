import { parseArgs } from 'node:util';
import { writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { buildBacklog, toCsvExport, exportBacklog, TARGETS } from '../../lib/export.js';
import { projectRootFromEnv } from '../../lib/paths.js';

export const help = `Usage: mdan export --to <${TARGETS.join('|')}> [options] [--apply]

Exports the epics/stories document. Dry run by default: prints the planned requests; --apply sends them.
Re-runs update the items already exported (ids kept in _mdan/state/export-<target>.json).

  --file <epics.md>        epics document (default: from the project state / docs/)
  --out <file.csv>         csv target: output file (default: stdout)
  --repo <owner/name>      github  (token: GITHUB_TOKEN or GH_TOKEN)
  --org <org> --project <p> ado    (token: AZURE_DEVOPS_PAT)
  --url <https://x.atlassian.net> --project <KEY>  jira (JIRA_EMAIL + JIRA_API_TOKEN)`;

export default async function exportCommand(argv) {
  const { values } = parseArgs({
    args: argv,
    options: {
      to: { type: 'string' }, file: { type: 'string' }, out: { type: 'string' }, apply: { type: 'boolean' },
      repo: { type: 'string' }, org: { type: 'string' }, project: { type: 'string' }, url: { type: 'string' },
      json: { type: 'boolean' }, help: { type: 'boolean', short: 'h' },
    },
  });
  if (values.help || !values.to) {
    console.log(help);
    if (!values.help) process.exitCode = 1;
    return;
  }
  const root = projectRootFromEnv();
  if (values.to === 'csv') {
    const csv = toCsvExport(buildBacklog(root, values.file));
    if (values.out) {
      writeFileSync(resolve(values.out), csv);
      return console.log(`Wrote ${resolve(values.out)}`);
    }
    return process.stdout.write(csv);
  }

  const r = await exportBacklog(root, values.to, {
    apply: Boolean(values.apply),
    file: values.file,
    options: { repo: values.repo, org: values.org, project: values.project, url: values.url },
  });
  if (values.json) return console.log(JSON.stringify(r, null, 2));
  for (const op of r.operations) console.log(`${op.method.padEnd(5)} ${op.key.padEnd(6)} ${op.url}`);
  console.log(r.apply
    ? `\n✔ ${r.created} created, ${r.updated} updated on ${r.target}.`
    : `\nDry run: ${r.operations.length} request(s) planned from ${r.source}. Add --apply to send them.`);
}
