#!/usr/bin/env node
// Generates every derived artifact from the content files (single source of truth):
//   _mdan/_config/{agent,workflow,task}-manifest.csv, _mdan/_config/files-manifest.csv, .claude/commands/mdan-*.md,
//   and the <!-- generated:* --> sections of README.md
// `--check` writes nothing and exits 1 when a generated file is out of date (used in CI).
import { readFileSync, existsSync, readdirSync, rmSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, relative, sep, dirname, extname, basename } from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { readSources } from '../lib/sources.js';
import { toCsv } from '../lib/csv.js';
import { buildCommands, IDE_TARGETS, agentSlug } from '../lib/commands.js';
import { walk } from '../lib/refs.js';

const AGENT_HEADERS = ['name', 'displayName', 'title', 'icon', 'capabilities', 'role', 'identity', 'communicationStyle', 'principles', 'module', 'path'];
const WORKFLOW_HEADERS = ['name', 'description', 'module', 'path'];
const TASK_HEADERS = ['name', 'displayName', 'description', 'module', 'path', 'standalone'];

// Not shipped as package content: generated at install time or at runtime.
const UNHASHED = [/^_mdan\/_config\/files-manifest\.csv$/, /^_mdan\/_config\/manifest\.yaml$/, /^_mdan\/state\/(?!.*\.template\.json$)/];

// Line endings are normalized so a CRLF checkout (Windows autocrlf) hashes like the LF original.
export const sha256 = data => createHash('sha256')
  .update(Buffer.isBuffer(data) && data.includes(0) ? data : String(data).replace(/\r\n/g, '\n'))
  .digest('hex');

const MODULE_LABELS = {
  core: 'Cœur',
  mdan: 'Module principal',
  fintech: 'Pack FinTech',
  'devops-azure': 'Pack DevOps & Azure',
  'db-optimization': 'Pack Database Optimization',
  ecosystem: 'Pack Ecosystem',
  qa: 'Pack Test Architect (QA)',
  'payments-ma': 'Pack Paiements Maroc',
};

const cell = s => String(s || '').replace(/\|/g, '\\|').replace(/\s+/g, ' ').trim();

function readmeSections({ agents, workflows }) {
  const modules = [...new Set(agents.map(a => a.module))];
  const packs = modules.filter(m => m !== 'core' && m !== 'mdan').length;
  const tables = modules.map(m => [
    `### ${MODULE_LABELS[m] || m}`,
    '',
    '| Commande | Agent | Rôle |',
    '|----------|-------|------|',
    ...agents.filter(a => a.module === m).map(a =>
      `| \`/mdan-${agentSlug(a)}\` | ${cell(a.icon)} ${cell(a.displayName)} | **${cell(a.title)}** — ${cell(a.role)} |`),
  ].join('\n')).join('\n\n');
  return {
    badges: [
      `[![Wizards](https://img.shields.io/badge/wizards-${workflows.length}-purple)](#commandes-disponibles)`,
      `[![Agents](https://img.shields.io/badge/agents-${agents.length}-blue)](#les-agents)`,
      `[![Packs](https://img.shields.io/badge/packs-${packs}-orange)](#les-agents)`,
    ].join('\n'),
    agents: tables,
    footer: `  <strong>${workflows.length} wizards · ${agents.length} agents · ${packs} packs · Serveur MCP · Context Graph · Débat/Consensus</strong><br>`,
  };
}

// Replaces the content between <!-- generated:NAME --> and <!-- /generated:NAME --> markers.
function renderReadme(text, sections) {
  return text.replace(/(<!-- generated:(\w+) -->\r?\n)[\s\S]*?(<!-- \/generated:\2 -->)/g,
    (match, open, name, close) => (name in sections ? `${open}${sections[name]}\n${close}` : match));
}

export function generate(root) {
  const sources = readSources(root);
  const outputs = new Map();

  outputs.set('_mdan/_config/agent-manifest.csv', toCsv(AGENT_HEADERS, sources.agents));
  outputs.set('_mdan/_config/workflow-manifest.csv', toCsv(WORKFLOW_HEADERS, sources.workflows));
  outputs.set('_mdan/_config/task-manifest.csv', toCsv(TASK_HEADERS, sources.tasks));

  const claude = IDE_TARGETS['claude-code'];
  for (const c of buildCommands(sources)) outputs.set(`${claude.dir}/${claude.file(c)}`, claude.render(c));

  const readmePath = join(root, 'README.md');
  if (existsSync(readmePath)) outputs.set('README.md', renderReadme(readFileSync(readmePath, 'utf-8'), readmeSections(sources)));

  const files = [];
  for (const full of walk(join(root, '_mdan'))) {
    const rel = relative(root, full).split(sep).join('/');
    if (UNHASHED.some(re => re.test(rel)) || rel.endsWith('.lock') || rel.endsWith('.tmp')) continue;
    const data = outputs.get(rel) ?? readFileSync(full);
    files.push({
      type: extname(rel).slice(1),
      name: basename(rel, extname(rel)),
      module: rel.split('/')[1],
      path: rel,
      hash: sha256(data),
    });
  }
  files.sort((a, b) => a.path.localeCompare(b.path));
  outputs.set('_mdan/_config/files-manifest.csv', toCsv(['type', 'name', 'module', 'path', 'hash'], files));

  return { sources, outputs };
}

function staleCommandFiles(root, outputs) {
  const dir = join(root, IDE_TARGETS['claude-code'].dir);
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter(f => f.startsWith('mdan-') && f.endsWith('.md'))
    .map(f => `${IDE_TARGETS['claude-code'].dir}/${f}`)
    .filter(p => !outputs.has(p));
}

export function build(root, { check = false } = {}) {
  const { sources, outputs } = generate(root);
  const changed = [];
  for (const [rel, content] of outputs) {
    const full = join(root, rel);
    const current = existsSync(full) ? readFileSync(full, 'utf-8') : null;
    if (current === content) continue;
    changed.push(rel);
    if (!check) {
      mkdirSync(dirname(full), { recursive: true });
      writeFileSync(full, content);
    }
  }
  const stale = staleCommandFiles(root, outputs);
  if (!check) for (const rel of stale) rmSync(join(root, rel));
  return { sources, changed, stale };
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const check = process.argv.includes('--check');
  const root = fileURLToPath(new URL('../../', import.meta.url));
  const { sources, changed, stale } = build(root, { check });
  const summary = `${sources.agents.length} agents, ${sources.workflows.length} workflows, ${sources.tasks.length} tasks`;
  if (check) {
    for (const f of [...changed, ...stale]) console.log(`out of date: ${f}`);
    if (changed.length || stale.length) {
      console.error('\nGenerated files are out of date. Run `npm run build` and commit the result.');
      process.exit(1);
    }
    console.log(`Generated files up to date (${summary}).`);
  } else {
    console.log(`Built ${summary}: ${changed.length} file(s) written, ${stale.length} stale command(s) removed.`);
  }
}
