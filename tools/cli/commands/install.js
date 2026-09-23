import { parseArgs } from 'node:util';
import { existsSync, readFileSync, mkdirSync, writeFileSync, readdirSync, rmSync } from 'node:fs';
import { join, resolve, relative, sep, dirname, basename } from 'node:path';
import { createInterface } from 'node:readline/promises';
import { userInfo } from 'node:os';
import { PACKAGE_ROOT, VERSION } from '../../lib/paths.js';
import { readSources, modulesOf } from '../../lib/sources.js';
import { buildCommands, IDE_TARGETS } from '../../lib/commands.js';
import { parseCsv, toCsv } from '../../lib/csv.js';
import { setYamlScalars, parseYamlScalars } from '../../lib/frontmatter.js';
import { walk } from '../../lib/refs.js';
import { sha256 } from '../../build/build.js';

export const LANGUAGES = {
  'fr-darija': 'français-darija',
  fr: 'français',
  en: 'english',
  darija: 'darija',
};
const REQUIRED_MODULES = ['core', 'mdan'];
const SCALE_VALUES = ['auto', 'solo', 'team', 'enterprise'];
const AGENT_HEADERS = ['name', 'displayName', 'title', 'icon', 'capabilities', 'role', 'identity', 'communicationStyle', 'principles', 'module', 'path'];
const WORKFLOW_HEADERS = ['name', 'description', 'module', 'path'];
const TASK_HEADERS = ['name', 'displayName', 'description', 'module', 'path', 'standalone'];

export const help = `Usage: mdan install [dir] [options]
       mdan update [dir]          Re-install with the options of the existing install

Installs MDAN (agents, wizards, IDE commands) into a project (default: current directory).
  --lang <l>        ${Object.keys(LANGUAGES).join(' | ')} (default fr-darija)
  --ide <list>      ${Object.keys(IDE_TARGETS).join(',')} (default claude-code)
  --modules <list>  optional packs: ${optionalModules().join(',')} | all | none (default none)
  --user <name>     your name, used by the agents (default: OS user)
  --scale <s>       auto | solo | team | enterprise (default auto): quality-gate strictness
  --mcp             add the MDAN MCP server to .mcp.json
  --force           overwrite files you modified (default: write <file>.mdan-new next to them)
  -y, --yes         non-interactive, accept defaults`;

function optionalModules() {
  return modulesOf(PACKAGE_ROOT).filter(m => !REQUIRED_MODULES.includes(m));
}

const toPosix = p => p.split(sep).join('/');
const list = v => (v ? v.split(',').map(s => s.trim()).filter(Boolean) : null);

function readExisting(target) {
  const manifestPath = join(target, '_mdan/_config/manifest.yaml');
  if (!existsSync(manifestPath)) return null;
  const manifest = readFileSync(manifestPath, 'utf-8');
  const section = name => {
    const m = manifest.match(new RegExp(`^${name}:\\n((?:\\s+- .*\\n?)*)`, 'm'));
    return m ? [...m[1].matchAll(/- (?:name: )?(\S+)/g)].map(x => x[1]) : [];
  };
  const configPath = join(target, '_mdan/mdan/config.yaml');
  const config = existsSync(configPath) ? parseYamlScalars(readFileSync(configPath, 'utf-8')) : {};
  const lang = Object.entries(LANGUAGES).find(([, v]) => v === config.communication_language)?.[0];
  return {
    modules: section('modules').filter(m => !REQUIRED_MODULES.includes(m)),
    ides: section('ides'),
    lang,
    user: config.user_name,
    scale: config.project_scale,
  };
}

async function ask(rl, question, choices, fallback) {
  const lines = choices.map((c, i) => `  ${i + 1}. ${c.label}`).join('\n');
  const answer = (await rl.question(`${question}\n${lines}\n> [${fallback}] `)).trim();
  return answer || String(fallback);
}

async function promptOptions(opts, target) {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  try {
    console.log(`\nMDAN v${VERSION} — installation dans ${target}\n`);
    const langs = [
      { key: 'fr-darija', label: 'Français + Darija marocaine' },
      { key: 'fr', label: 'Français' },
      { key: 'en', label: 'English' },
      { key: 'darija', label: 'Darija marocaine' },
    ];
    const langIdx = Number(await ask(rl, 'Langue de communication :', langs, langs.findIndex(l => l.key === opts.lang) + 1));
    opts.lang = langs[langIdx - 1]?.key || opts.lang;

    const mods = optionalModules();
    const modAnswer = await ask(rl, 'Packs optionnels (numéros séparés par des virgules, "all" ou vide) :',
      mods.map(m => ({ label: m })), opts.modules.join(',') || 'aucun');
    if (modAnswer === 'all') opts.modules = mods;
    else if (modAnswer !== 'aucun') opts.modules = list(modAnswer).map(x => mods[Number(x) - 1] || x).filter(m => mods.includes(m));

    const ides = Object.keys(IDE_TARGETS);
    const ideAnswer = await ask(rl, 'IDE(s) (numéros séparés par des virgules) :', ides.map(i => ({ label: i })),
      opts.ides.map(i => ides.indexOf(i) + 1).join(','));
    opts.ides = list(ideAnswer).map(x => ides[Number(x) - 1] || x).filter(i => ides.includes(i));

    opts.user = (await rl.question(`Ton nom (utilisé par les agents) > [${opts.user}] `)).trim() || opts.user;
    const mcp = (await rl.question(`Ajouter le serveur MCP MDAN à .mcp.json ? (o/N) > `)).trim().toLowerCase();
    opts.mcp = opts.mcp || mcp === 'o' || mcp === 'y';
  } finally {
    rl.close();
  }
  return opts;
}

export function resolveOptions(values, existing) {
  const opts = {
    lang: values.lang ?? existing?.lang ?? 'fr-darija',
    ides: list(values.ide) ?? (existing?.ides.length ? existing.ides : ['claude-code']),
    modules: list(values.modules) ?? existing?.modules ?? [],
    user: values.user ?? existing?.user ?? userInfo().username,
    scale: values.scale ?? existing?.scale ?? 'auto',
    mcp: Boolean(values.mcp),
    force: Boolean(values.force),
  };
  if (opts.modules.includes('all')) opts.modules = optionalModules();
  if (opts.modules.includes('none')) opts.modules = [];
  validate(opts);
  return opts;
}

function validate(opts) {
  if (!SCALE_VALUES.includes(opts.scale)) throw new Error(`Unknown scale '${opts.scale}' (expected ${SCALE_VALUES.join(', ')})`);
  if (!LANGUAGES[opts.lang]) throw new Error(`Unknown language '${opts.lang}' (expected ${Object.keys(LANGUAGES).join(', ')})`);
  const badIde = opts.ides.filter(i => !IDE_TARGETS[i]);
  if (badIde.length) throw new Error(`Unknown IDE(s): ${badIde.join(', ')} (expected ${Object.keys(IDE_TARGETS).join(', ')})`);
  const badMod = opts.modules.filter(m => !optionalModules().includes(m));
  if (badMod.length) throw new Error(`Unknown module(s): ${badMod.join(', ')} (expected ${optionalModules().join(', ')})`);
}

function isShipped(rel, modules) {
  const [, top, ...rest] = rel.split('/');
  if (modules.includes(top)) return true;
  if (top === 'state') return rel.endsWith('.template.json');
  if (top === '_config') {
    if (rest[0] === 'agents') return modules.some(m => rest[1]?.startsWith(`${m}-`));
    return ['mdan-help.csv', 'tool-manifest.csv'].includes(rest[0]);
  }
  return false;
}

function writeTracked(target, rel, content, ctx) {
  const full = join(target, rel);
  const next = sha256(content);
  ctx.installed.set(rel, next);
  if (!existsSync(full)) {
    mkdirSync(dirname(full), { recursive: true });
    writeFileSync(full, content);
    ctx.stats.added++;
    return;
  }
  const current = sha256(readFileSync(full));
  if (current === next) return;
  const recorded = ctx.previous.get(rel);
  if (ctx.force || current === recorded) {
    writeFileSync(full, content);
    ctx.stats.updated++;
  } else {
    writeFileSync(`${full}.mdan-new`, content);
    ctx.stats.conflicts.push(rel);
  }
}

function writeConfig(target, module, opts) {
  const full = join(target, '_mdan', module, 'config.yaml');
  const src = join(PACKAGE_ROOT, '_mdan', module, 'config.yaml');
  const base = existsSync(full) ? readFileSync(full, 'utf-8') : existsSync(src) ? readFileSync(src, 'utf-8') : '';
  const values = { user_name: opts.user, communication_language: LANGUAGES[opts.lang] };
  if (module === 'mdan') Object.assign(values, { project_name: basename(target), project_scale: opts.scale });
  mkdirSync(dirname(full), { recursive: true });
  writeFileSync(full, setYamlScalars(base, values));
}

function writeIdeCommands(target, ide, commands) {
  const t = IDE_TARGETS[ide];
  const dir = join(target, t.dir);
  mkdirSync(dir, { recursive: true });
  const wanted = new Set(commands.map(c => t.file(c)));
  for (const f of readdirSync(dir)) {
    if (f.startsWith('mdan-') && !wanted.has(f)) rmSync(join(dir, f));
  }
  for (const c of commands) writeFileSync(join(dir, t.file(c)), t.render(c));
  return commands.length;
}

function writeMcpJson(target) {
  const full = join(target, '.mcp.json');
  let config = {};
  if (existsSync(full)) {
    try { config = JSON.parse(readFileSync(full, 'utf-8')); } catch { throw new Error(`${full} is not valid JSON; fix it or rerun without --mcp`); }
  }
  config.mcpServers = config.mcpServers || {};
  config.mcpServers.mdan = { command: 'npx', args: ['-y', `mdan-method@${VERSION}`, 'serve'], env: { MDAN_PROJECT_ROOT: '.' } };
  writeFileSync(full, JSON.stringify(config, null, 2) + '\n');
}

function initState(target) {
  const state = join(target, '_mdan/state/MDAN-STATE.json');
  if (!existsSync(state)) {
    const tpl = JSON.parse(readFileSync(join(PACKAGE_ROOT, '_mdan/state/MDAN-STATE.template.json'), 'utf-8'));
    const now = new Date().toISOString();
    tpl.project = { ...tpl.project, name: basename(target), created_at: now, last_updated: now };
    writeFileSync(state, JSON.stringify(tpl, null, 2) + '\n');
  }
  const graph = join(target, '_mdan/state/context-graph.json');
  if (!existsSync(graph)) writeFileSync(graph, JSON.stringify({ version: '1.1.0', nodes: {}, edges: [] }, null, 2) + '\n');
}

function manifestYaml(modules, ides, previousInstallDate) {
  const now = new Date().toISOString();
  return [
    'installation:',
    `  version: ${VERSION}`,
    `  installDate: ${previousInstallDate || now}`,
    `  lastUpdated: ${now}`,
    'modules:',
    ...modules.map(m => `  - name: ${m}\n    version: ${VERSION}\n    source: mdan-method`),
    'ides:',
    ...ides.map(i => `  - ${i}`),
    '',
  ].join('\n');
}

export function install(target, opts) {
  target = resolve(target);
  if (target === resolve(PACKAGE_ROOT)) throw new Error('Refusing to install MDAN into its own package directory.');
  const modules = [...REQUIRED_MODULES, ...opts.modules];

  const filesManifest = join(target, '_mdan/_config/files-manifest.csv');
  const previous = new Map(existsSync(filesManifest)
    ? parseCsv(readFileSync(filesManifest, 'utf-8')).map(r => [r.path, r.hash]) : []);
  const oldManifest = join(target, '_mdan/_config/manifest.yaml');
  const previousInstallDate = existsSync(oldManifest)
    ? readFileSync(oldManifest, 'utf-8').match(/installDate: (\S+)/)?.[1] : null;

  const ctx = { previous, installed: new Map(), force: opts.force, stats: { added: 0, updated: 0, conflicts: [] } };

  for (const full of walk(join(PACKAGE_ROOT, '_mdan'))) {
    const rel = toPosix(relative(PACKAGE_ROOT, full));
    if (!isShipped(rel, modules)) continue;
    if (/^_mdan\/[^/]+\/config\.yaml$/.test(rel)) continue;
    writeTracked(target, rel, readFileSync(full), ctx);
  }
  for (const m of modules) writeConfig(target, m, opts);

  const all = readSources(PACKAGE_ROOT);
  const sources = {
    agents: all.agents.filter(a => modules.includes(a.module)),
    workflows: all.workflows.filter(w => modules.includes(w.module)),
    tasks: all.tasks.filter(t => modules.includes(t.module)),
  };
  const configDir = join(target, '_mdan/_config');
  mkdirSync(configDir, { recursive: true });
  writeFileSync(join(configDir, 'agent-manifest.csv'), toCsv(AGENT_HEADERS, sources.agents));
  writeFileSync(join(configDir, 'workflow-manifest.csv'), toCsv(WORKFLOW_HEADERS, sources.workflows));
  writeFileSync(join(configDir, 'task-manifest.csv'), toCsv(TASK_HEADERS, sources.tasks));
  writeFileSync(join(configDir, 'manifest.yaml'), manifestYaml(modules, opts.ides, previousInstallDate));
  const tracked = [...ctx.installed].sort(([a], [b]) => a.localeCompare(b))
    .map(([path, hash]) => ({ type: path.split('.').pop(), name: basename(path).replace(/\.[^.]+$/, ''), module: path.split('/')[1], path, hash }));
  writeFileSync(filesManifest, toCsv(['type', 'name', 'module', 'path', 'hash'], tracked));

  initState(target);
  const commands = buildCommands(sources);
  const ideCounts = Object.fromEntries(opts.ides.map(ide => [ide, writeIdeCommands(target, ide, commands)]));
  if (opts.mcp) writeMcpJson(target);

  return { target, modules, sources, ideCounts, ...ctx.stats };
}

export default async function installCommand(argv, { update = false } = {}) {
  const { values, positionals } = parseArgs({
    args: argv,
    allowPositionals: true,
    options: {
      lang: { type: 'string' },
      ide: { type: 'string' },
      modules: { type: 'string' },
      user: { type: 'string' },
      scale: { type: 'string' },
      mcp: { type: 'boolean' },
      force: { type: 'boolean' },
      yes: { type: 'boolean', short: 'y' },
      help: { type: 'boolean', short: 'h' },
    },
  });
  if (values.help) return console.log(help);

  const target = resolve(positionals[0] || process.cwd());
  const existing = readExisting(target);
  if (update && !existing) throw new Error(`No MDAN install found in ${target}. Run \`mdan install\` first.`);

  let opts = resolveOptions(values, existing);
  if (!update && !values.yes && process.stdin.isTTY) {
    opts = await promptOptions(opts, target);
    validate(opts);
  }

  const r = install(target, opts);
  console.log(`\n✔ MDAN v${VERSION} ${update ? 'mis à jour' : 'installé'} dans ${r.target}`);
  console.log(`  Modules : ${r.modules.join(', ')}`);
  console.log(`  ${r.sources.agents.length} agents, ${r.sources.workflows.length} workflows, ${r.sources.tasks.length} tâches`);
  console.log(`  Fichiers : ${r.added} ajoutés, ${r.updated} mis à jour`);
  for (const [ide, n] of Object.entries(r.ideCounts)) console.log(`  ${ide} : ${n} commandes dans ${IDE_TARGETS[ide].dir}/`);
  if (opts.mcp) console.log('  Serveur MCP ajouté à .mcp.json');
  if (r.conflicts.length) {
    console.log(`\n⚠ ${r.conflicts.length} fichier(s) modifié(s) par toi conservé(s) ; nouvelle version écrite en .mdan-new :`);
    for (const c of r.conflicts) console.log(`  - ${c}`);
    console.log('  (relance avec --force pour écraser)');
  }
  console.log('\nDans ton IDE, tape /mdan- pour voir les commandes. Conseil : ajoute mdan_output/ et _mdan/state/ à ton .gitignore si besoin.');
}

