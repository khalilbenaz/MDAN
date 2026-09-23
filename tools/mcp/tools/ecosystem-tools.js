import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { readFile } from 'node:fs/promises';
import { join, relative, sep } from 'node:path';
import { homedir } from 'node:os';
import { z } from 'zod';
import { parseFrontmatter } from '../../lib/frontmatter.js';
import { safeJoin } from '../../lib/paths.js';
import { safe, text } from '../util.js';

const KINDS = {
  skill: { dir: 'skills', label: 'skills' },
  agent: { dir: 'agents', label: 'agents' },
  command: { dir: 'commands', label: 'commands' },
};

export const claudeDir = () => process.env.MDAN_CLAUDE_DIR || join(homedir(), '.claude');

function listMarkdown(dir, out = []) {
  if (!existsSync(dir)) return out;
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    let st;
    try { st = statSync(full); } catch { continue; }
    if (st.isDirectory()) listMarkdown(full, out);
    else if (name.endsWith('.md')) out.push(full);
  }
  return out;
}

// One entry per component: skills are folders with SKILL.md, agents/commands are .md files (optionally in categories).
function listComponents(kind) {
  const base = join(claudeDir(), KINDS[kind].dir);
  const files = listMarkdown(base).filter(f => kind !== 'skill' || f.endsWith(`${sep}SKILL.md`));
  return files.map(file => {
    const rel = relative(base, file).split(sep).join('/');
    const id = kind === 'skill' ? rel.replace(/\/SKILL\.md$/, '') : rel.replace(/\.md$/, '');
    return { id, file };
  });
}

function score(entry, terms) {
  let head;
  try { head = readFileSync(entry.file, 'utf-8').slice(0, 4000); } catch { return 0; }
  const fm = parseFrontmatter(head);
  const fields = [
    [entry.id.toLowerCase(), 5],
    [(fm.name || '').toLowerCase(), 4],
    [(fm.description || '').toLowerCase(), 3],
    [head.toLowerCase(), 1],
  ];
  let total = 0;
  for (const t of terms) {
    const hit = fields.find(([value]) => value.includes(t));
    if (!hit) return 0;
    total += hit[1];
  }
  entry.description = fm.description || '';
  return total;
}

function resolveComponent(kind, name) {
  const base = join(claudeDir(), KINDS[kind].dir);
  const file = kind === 'skill' ? safeJoin(base, name, 'SKILL.md') : safeJoin(base, `${name}.md`);
  if (!existsSync(file)) throw new Error(`${kind} "${name}" not found under ${base}`);
  return file;
}

export function registerEcosystemTools(server, projectRoot) {
  server.registerTool('mdan_ecosystem_search', {
    description: 'Search installed Claude Code skills, agents or commands (~/.claude) by keywords, ranked by name/description match',
    inputSchema: {
      kind: z.enum(['skill', 'agent', 'command']).describe('Component type'),
      query: z.string().min(1).describe('Keywords, e.g. "react testing"'),
      limit: z.number().int().min(1).max(100).default(20),
    },
    annotations: { readOnlyHint: true },
  }, safe(async ({ kind, query, limit }) => {
    const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    const results = listComponents(kind)
      .map(e => { const s = score(e, terms); return { ...e, score: s }; })
      .filter(e => e.score > 0)
      .sort((a, b) => b.score - a.score || a.id.localeCompare(b.id))
      .slice(0, limit);
    if (!results.length) return text(`No ${KINDS[kind].label} matching "${query}" in ${join(claudeDir(), KINDS[kind].dir)}.`);
    return text(`${results.length} ${KINDS[kind].label} matching "${query}":\n\n` +
      results.map(r => `- **${r.id}**${r.description ? ` — ${r.description}` : ''}`).join('\n') +
      `\n\nRead one with mdan_ecosystem_read { kind: "${kind}", name: "${results[0].id}" }.`);
  }));

  server.registerTool('mdan_ecosystem_read', {
    description: 'Read the full content of an installed skill, agent or command',
    inputSchema: {
      kind: z.enum(['skill', 'agent', 'command']),
      name: z.string().describe('Skill folder name, or agent/command path "category/name"'),
    },
    annotations: { readOnlyHint: true },
  }, safe(async ({ kind, name }) => text(await readFile(resolveComponent(kind, name), 'utf-8'))));

  server.registerTool('mdan_ecosystem_catalog', {
    description: 'Page through the MDAN ecosystem catalog (categorized list of known components)',
    inputSchema: {
      offset: z.number().int().min(0).default(0).describe('Character offset'),
      length: z.number().int().min(1000).max(50000).default(15000),
    },
    annotations: { readOnlyHint: true },
  }, safe(async ({ offset, length }) => {
    const catalogPath = join(projectRoot, '_mdan', 'ecosystem', 'catalog', 'CATALOG.md');
    if (!existsSync(catalogPath)) throw new Error('Catalog not found: install the ecosystem module (mdan install --modules ecosystem).');
    const catalog = await readFile(catalogPath, 'utf-8');
    const chunk = catalog.slice(offset, offset + length);
    const end = offset + chunk.length;
    return text(chunk + (end < catalog.length ? `\n\n[… ${catalog.length - end} more characters — call again with offset=${end}]` : ''));
  }));

  server.registerTool('mdan_ecosystem_stats', {
    description: 'Count installed Claude Code components (skills, agents, commands) in ~/.claude',
    annotations: { readOnlyHint: true },
  }, safe(async () => {
    const lines = Object.keys(KINDS).map(kind => {
      const n = listComponents(kind).length;
      return `- **${KINDS[kind].label}**: ${n ? `${n} installed` : 'none found'}`;
    });
    return text(`# Ecosystem status (${claudeDir()})\n\n${lines.join('\n')}\n\nSources:\n- khalilbenaz/claude-skills-collection\n- davila7/claude-code-templates (aitmpl.com)`);
  }));
}
