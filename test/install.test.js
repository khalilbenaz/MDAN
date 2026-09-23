import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, writeFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { install, resolveOptions } from '../tools/cli/commands/install.js';
import { parseYamlScalars } from '../tools/lib/frontmatter.js';
import { parseCsv } from '../tools/lib/csv.js';

const tmp = () => mkdtempSync(join(tmpdir(), 'mdan-install-'));
const opts = extra => resolveOptions({ lang: 'en', user: 'tester', ide: 'claude-code,gemini', ...extra }, null);

test('fresh install copies content, configs, manifests and IDE commands', () => {
  const dir = tmp();
  const r = install(dir, opts({ modules: 'fintech', mcp: true }));
  assert.deepEqual(r.modules, ['core', 'mdan', 'fintech']);
  assert.ok(existsSync(join(dir, '_mdan/mdan/workflows/02-plan/create-prd/wizard.md')));
  assert.ok(!existsSync(join(dir, '_mdan/devops-azure')), 'unselected module not installed');

  const cfg = parseYamlScalars(readFileSync(join(dir, '_mdan/mdan/config.yaml'), 'utf-8'));
  assert.equal(cfg.communication_language, 'english');
  assert.equal(cfg.user_name, 'tester');

  const agents = parseCsv(readFileSync(join(dir, '_mdan/_config/agent-manifest.csv'), 'utf-8'));
  assert.ok(agents.every(a => ['core', 'mdan', 'fintech'].includes(a.module)));
  assert.ok(agents.some(a => a.module === 'fintech'));

  const claude = readdirSync(join(dir, '.claude/commands'));
  assert.ok(claude.includes('mdan-create-prd.md'));
  assert.ok(claude.includes('mdan-agent-fintech-risk-manager.md'));
  assert.ok(!claude.some(f => f.includes('devops-azure')));
  const toml = readFileSync(join(dir, '.gemini/commands/mdan-create-prd.toml'), 'utf-8');
  assert.match(toml, /^description = /);
  assert.match(toml, /@\{_mdan\/mdan\/workflows\/02-plan\/create-prd\/wizard\.md\}/);

  assert.equal(JSON.parse(readFileSync(join(dir, '.mcp.json'), 'utf-8')).mcpServers.mdan.command, 'npx');
  assert.ok(existsSync(join(dir, '_mdan/state/MDAN-STATE.json')));
  assert.ok(existsSync(join(dir, '_mdan/state/context-graph.json')));
});

test('reinstall keeps user-modified files and writes .mdan-new', () => {
  const dir = tmp();
  install(dir, opts());
  const wizard = join(dir, '_mdan/mdan/workflows/02-plan/create-prd/wizard.md');
  writeFileSync(wizard, 'my custom wizard');

  const r = install(dir, opts());
  assert.equal(readFileSync(wizard, 'utf-8'), 'my custom wizard');
  assert.ok(existsSync(`${wizard}.mdan-new`));
  assert.deepEqual(r.conflicts, ['_mdan/mdan/workflows/02-plan/create-prd/wizard.md']);

  install(dir, { ...opts(), force: true });
  assert.notEqual(readFileSync(wizard, 'utf-8'), 'my custom wizard');
});

test('a CRLF-only change (git autocrlf) is not treated as a user modification', () => {
  const dir = tmp();
  install(dir, opts());
  const wizard = join(dir, '_mdan/mdan/workflows/02-plan/create-prd/wizard.md');
  writeFileSync(wizard, readFileSync(wizard, 'utf-8').replace(/\r?\n/g, '\r\n'));
  assert.deepEqual(install(dir, opts()).conflicts, []);
});

test('user config edits survive reinstall; only managed keys change', () => {
  const dir = tmp();
  install(dir, opts());
  const cfgPath = join(dir, '_mdan/mdan/config.yaml');
  writeFileSync(cfgPath, readFileSync(cfgPath, 'utf-8') + 'custom_key: "keep me"\n');
  install(dir, { ...opts(), lang: 'fr' });
  const cfg = parseYamlScalars(readFileSync(cfgPath, 'utf-8'));
  assert.equal(cfg.custom_key, 'keep me');
  assert.equal(cfg.communication_language, 'français');
});

test('removing a module on reinstall removes its commands', () => {
  const dir = tmp();
  install(dir, opts({ modules: 'fintech' }));
  install(dir, opts({ modules: 'none' }));
  assert.ok(!readdirSync(join(dir, '.claude/commands')).some(f => f.includes('fintech')));
});

test('invalid options are rejected', () => {
  assert.throws(() => resolveOptions({ lang: 'klingon' }, null), /Unknown language/);
  assert.throws(() => resolveOptions({ ide: 'notepad' }, null), /Unknown IDE/);
  assert.throws(() => resolveOptions({ modules: 'nope' }, null), /Unknown module/);
});
