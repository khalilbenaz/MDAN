import { test } from 'node:test';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { build } from '../tools/build/build.js';
import { findBrokenRefs } from '../tools/lib/refs.js';

const root = fileURLToPath(new URL('../', import.meta.url));

test('generated manifests and commands are up to date', () => {
  const { changed, stale, sources } = build(root, { check: true });
  assert.deepEqual([...changed, ...stale], [], 'run `npm run build`');
  assert.ok(sources.agents.length > 0 && sources.workflows.length > 0);
});

test('every file reference in the content resolves', () => {
  assert.deepEqual(findBrokenRefs(root), []);
});

test('`npx mdan-method <cmd>` resolves: a bin is named after the package', async () => {
  const { readFileSync } = await import('node:fs');
  const pkg = JSON.parse(readFileSync(new URL('../package.json', import.meta.url), 'utf-8'));
  assert.equal(pkg.bin[pkg.name], 'tools/cli/index.js');
});

test('agents: display names are unique and every party team member exists', async () => {
  const { readAgents } = await import('../tools/lib/sources.js');
  const { parseCsv } = await import('../tools/lib/csv.js');
  const { readFileSync, existsSync } = await import('node:fs');
  const { join } = await import('node:path');
  const agents = readAgents(root);
  const names = agents.map(a => a.displayName);
  assert.deepEqual(names.filter((n, i) => names.indexOf(n) !== i), [], 'duplicate persona names');
  const team = parseCsv(readFileSync(join(root, '_mdan/mdan/teams/default-party.csv'), 'utf-8'));
  assert.ok(team.length >= 5);
  for (const member of team) assert.ok(existsSync(join(root, member.path)), member.path);
});

test('no BMAD leftovers in the content', async () => {
  const { walk } = await import('../tools/lib/refs.js');
  const { readFileSync } = await import('node:fs');
  const offenders = walk(new URL('../_mdan', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'))
    .filter(f => /\b(bmm|bmad|_bmad|BMAD)\b/.test(readFileSync(f, 'utf-8')));
  assert.deepEqual(offenders, []);
});
