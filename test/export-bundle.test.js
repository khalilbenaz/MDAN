import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { buildBacklog, toCsvExport, exportBacklog } from '../tools/lib/export.js';
import { bundleAgent, writeBundles } from '../tools/lib/bundle.js';
import { parseCsv } from '../tools/lib/csv.js';

const EPICS = `# Shop - Epic Breakdown

## Epic 1: Checkout
Let customers pay.

### Story 1.1: Pay by card
Covers FR1.
**Given** a cart **When** I pay **Then** the order is confirmed

### Story 1.2: Pay by wallet
Covers FR2.
**Given** a wallet **When** I pay **Then** it is debited
`;

function project() {
  const root = mkdtempSync(join(tmpdir(), 'mdan-export-'));
  mkdirSync(join(root, 'docs'));
  writeFileSync(join(root, 'docs/epics.md'), EPICS);
  return root;
}

test('backlog and CSV export', () => {
  const root = project();
  const b = buildBacklog(root);
  assert.equal(b.epics[0].description, 'Let customers pay.');
  assert.deepEqual(b.epics[0].stories.map(s => s.key), ['S1.1', 'S1.2']);
  const rows = parseCsv(toCsvExport(b));
  assert.deepEqual(rows.map(r => `${r.type}:${r.key}:${r.parent}`), ['Epic:E1:', 'Story:S1.1:E1', 'Story:S1.2:E1']);
});

test('dry run plans requests without network; missing options are reported', async () => {
  const root = project();
  await assert.rejects(exportBacklog(root, 'github', {}), /--repo/);
  const r = await exportBacklog(root, 'ado', { options: { org: 'b3g', project: 'Wallet' }, fetchImpl: () => { throw new Error('no network in dry run'); } });
  assert.equal(r.operations.length, 3);
  assert.match(r.operations[0].url, /\/\$Epic\?api-version=7\.1$/);
  assert.equal(r.operations[1].body.at(-1).value.rel, 'System.LinkTypes.Hierarchy-Reverse');
});

test('apply is idempotent: second run updates instead of creating', async () => {
  const root = project();
  process.env.GITHUB_TOKEN = 'test-token';
  const calls = [];
  let next = 10;
  const fetchImpl = async (url, init) => {
    calls.push({ url, method: init.method, body: JSON.parse(init.body) });
    return { ok: true, status: 201, text: async () => JSON.stringify({ number: next++ }) };
  };
  const first = await exportBacklog(root, 'github', { apply: true, options: { repo: 'me/shop' }, fetchImpl });
  assert.deepEqual([first.created, first.updated], [3, 0]);
  assert.match(calls[1].body.body, /Part of #10/);
  assert.deepEqual(JSON.parse(readFileSync(join(root, '_mdan/state/export-github.json'), 'utf-8')), { E1: 10, 'S1.1': 11, 'S1.2': 12 });

  const second = await exportBacklog(root, 'github', { apply: true, options: { repo: 'me/shop' }, fetchImpl });
  assert.deepEqual([second.created, second.updated], [0, 3]);
  assert.equal(calls.at(-1).method, 'PATCH');
  assert.match(calls.at(-1).url, /issues\/12$/);
  delete process.env.GITHUB_TOKEN;
});

test('jira payload uses ADF and parent keys', async () => {
  const r = await exportBacklog(project(), 'jira', { options: { url: 'https://x.atlassian.net/', project: 'SHOP' } });
  const story = r.operations[1].body.fields;
  assert.equal(story.issuetype.name, 'Story');
  assert.equal(story.parent.key, '<E1>');
  assert.equal(story.description.type, 'doc');
});

test('web bundle: instructions fit the limit, knowledge embeds the agent workflows', () => {
  const root = fileURLToPath(new URL('../', import.meta.url));
  const b = bundleAgent(root, 'mdan-master');
  assert.ok(b.instructions.length <= 8000);
  assert.match(b.knowledge, /## FILE: _mdan\/core\/rules\.md/);
  assert.match(b.knowledge, /## FILE: _mdan\/core\/agents\/mdan-master\.md/);
  assert.ok(b.files > 5);
  const out = mkdtempSync(join(tmpdir(), 'mdan-bundle-'));
  writeBundles(root, ['mdan-master'], out);
  assert.ok(existsSync(join(out, 'mdan-master.knowledge.md')));
  assert.ok(existsSync(join(out, 'README.md')));
  assert.throws(() => bundleAgent(root, 'nobody'), /Unknown agent/);
});
