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
