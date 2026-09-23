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

test('README.en.md generated sections stay in sync with README.md', async () => {
  const { existsSync, readFileSync } = await import('node:fs');
  const enPath = new URL('../README.en.md', import.meta.url);
  assert.ok(existsSync(enPath), 'README.en.md must exist');
  const en = readFileSync(enPath, 'utf-8');
  for (const name of ['badges', 'agents', 'footer']) {
    assert.match(en, new RegExp(`<!-- generated:${name} -->[\\s\\S]*?<!-- /generated:${name} -->`), `missing marker pair ${name}`);
  }
  // Same agent/workflow counts as the French README (build() already asserted both are up to date).
  const fr = readFileSync(new URL('../README.md', import.meta.url), 'utf-8');
  const countRows = s => (s.match(/^\| `\/mdan-agent-/gm) || []).length;
  assert.equal(countRows(en), countRows(fr), 'README.en.md and README.md must list the same agents');
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

