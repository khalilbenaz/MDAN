// Quality gates and traceability for MDAN artifacts (brief, PRD, architecture, epics, tech spec).
// Pure text analysis: no LLM, deterministic, usable in CI.
import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join, relative, sep, basename } from 'node:path';
import { parseYamlScalars } from './frontmatter.js';
import { loadState } from './state.js';

export const SCALES = ['solo', 'team', 'enterprise'];

// ---------- parsing ----------

const REQ = /\b(N?FR)-?(\d{1,4})\b/g;

export function requirementIds(text) {
  return [...new Set([...text.matchAll(REQ)].map(m => `${m[1]}${Number(m[2])}`))];
}

// Requirements *defined* in a PRD: an id at the start of a list item / line ("- FR3: ...", "**NFR2** ...").
export function definedRequirements(text) {
  const out = new Map();
  for (const line of text.split(/\r?\n/)) {
    const m = line.match(/^\s*(?:[-*]|\d+\.)?\s*\**\s*(N?FR)-?(\d{1,4})\b\**\s*[:.)—-]?\s*(.*)$/);
    if (m) out.set(`${m[1]}${Number(m[2])}`, m[3].replace(/\*+/g, '').trim());
  }
  return out;
}

export function sections(text) {
  const lines = text.split(/\r?\n/);
  const result = [];
  let current = null;
  let inCode = false;
  for (const line of lines) {
    if (/^```/.test(line)) inCode = !inCode;
    const m = !inCode && line.match(/^(#{1,6})\s+(.*)$/);
    if (m) {
      current = { level: m[1].length, title: m[2].trim(), body: [] };
      result.push(current);
    } else if (current) current.body.push(line);
  }
  return result.map(s => ({ ...s, body: s.body.join('\n') }));
}

// "## Epic 1: Title" / "### Story 1.2: Title"
export function parseEpics(text) {
  const epics = [];
  let epic = null;
  let story = null;
  for (const s of sections(text)) {
    const e = s.title.match(/^Epic\s+(\d+)\s*[:.—-]\s*(.*)$/i);
    const st = s.title.match(/^Story\s+(\d+)[.-](\d+)\s*[:.—-]\s*(.*)$/i);
    if (e) {
      epic = { id: Number(e[1]), title: e[2].trim(), stories: [] };
      epics.push(epic);
      story = null;
    } else if (st) {
      story = {
        id: `${Number(st[1])}.${Number(st[2])}`,
        title: st[3].trim(),
        requirements: requirementIds(s.body),
        hasCriteria: /\bGiven\b[\s\S]*\bThen\b/i.test(s.body) || /acceptance criteria/i.test(s.body),
        body: s.body,
      };
      if (!epic) {
        epic = { id: Number(st[1]), title: '', stories: [] };
        epics.push(epic);
      }
      epic.stories.push(story);
    } else if (story && s.level > 3) {
      story.requirements = [...new Set([...story.requirements, ...requirementIds(s.body + s.title)])];
      story.hasCriteria ||= /\bGiven\b[\s\S]*\bThen\b/i.test(s.body);
    }
  }
  return epics;
}

// ---------- artifact kinds ----------

const KIND_RULES = [
  { kind: 'epics', test: (name, text) => /epic/i.test(name) || /^#\s.*epic/im.test(text) },
  { kind: 'prd', test: (name, text) => /prd|requirements/i.test(name) || /^#\s.*(product requirements|PRD)/im.test(text) },
  { kind: 'architecture', test: (name, text) => /archi/i.test(name) || /^#\s.*architecture/im.test(text) },
  { kind: 'brief', test: (name, text) => /brief/i.test(name) || /^#\s.*product brief/im.test(text) },
  { kind: 'tech-spec', test: (name, text) => /spec/i.test(name) || /^#\s.*tech-?spec/im.test(text) },
  { kind: 'ux', test: (name, text) => /ux/i.test(name) || /^#\s.*UX/m.test(text) },
];

export function detectKind(path, text) {
  return KIND_RULES.find(r => r.test(basename(path), text))?.kind || 'generic';
}

const REQUIRED_HEADINGS = {
  brief: [/vision/i, /utilisateurs|users/i, /p[ée]rim[èe]tre|scope/i, /m[ée]triques|metrics|success/i],
  'tech-spec': [/problem/i, /solution/i, /tasks|t[âa]ches/i, /acceptance criteria|crit[èe]res/i],
  architecture: [/decision|d[ée]cision/i, /pattern|structure/i],
};

// ---------- scale ----------

export function detectScale(projectRoot) {
  const cfgPath = join(projectRoot, '_mdan/mdan/config.yaml');
  const cfg = existsSync(cfgPath) ? parseYamlScalars(readFileSync(cfgPath, 'utf-8')) : {};
  if (SCALES.includes(cfg.project_scale)) return { scale: cfg.project_scale, source: 'config' };

  const epicsArtifact = loadState(projectRoot).artifacts.find(a => /epic/i.test(a.id) || /epic/i.test(a.path));
  const epicsPath = epicsArtifact && join(projectRoot, epicsArtifact.path);
  if (epicsPath && existsSync(epicsPath)) {
    const stories = parseEpics(readFileSync(epicsPath, 'utf-8')).reduce((n, e) => n + e.stories.length, 0);
    const scale = stories < 5 ? 'solo' : stories <= 50 ? 'team' : 'enterprise';
    return { scale, source: `${stories} stories in ${epicsArtifact.path}` };
  }
  return { scale: 'team', source: 'default' };
}

// ---------- quality gate ----------

function gate(issues, scale) {
  const errors = issues.filter(i => i.level === 'error').length;
  const warnings = issues.filter(i => i.level === 'warning').length;
  const score = Math.max(0, 100 - errors * 20 - warnings * 5);
  let decision = 'PASS';
  if (errors) decision = 'FAIL';
  else if (warnings && scale === 'enterprise') decision = 'FAIL';
  else if (warnings && scale === 'team') decision = 'CONCERNS';
  return { decision, score, errors, warnings };
}

/**
 * Checks one artifact. `related` may hold other artifact texts ({ prd, architecture, epics }) for
 * cross-document coverage checks.
 */
export function checkArtifact(path, text, { kind = detectKind(path, text), scale = 'team', related = {} } = {}) {
  const issues = [];
  const add = (level, rule, message) => issues.push({ level, rule, message });

  const placeholders = [...new Set(text.match(/\{\{[^}\n]+\}\}/g) || [])];
  if (placeholders.length) add('error', 'placeholders', `Unfilled template placeholders: ${placeholders.slice(0, 8).join(', ')}`);
  const todos = (text.match(/\b(TODO|TBD|FIXME|XXX)\b|\[TBD\]|\?\?\?/g) || []).length;
  if (todos) add('warning', 'todo', `${todos} TODO/TBD marker(s) left`);

  const secs = sections(text);
  const empty = secs.filter((s, i) => !s.body.trim() && !(secs[i + 1] && secs[i + 1].level > s.level)).map(s => s.title);
  if (empty.length) add('warning', 'empty-sections', `Empty section(s): ${empty.slice(0, 8).join(' · ')}`);

  for (const re of REQUIRED_HEADINGS[kind] || []) {
    if (!secs.some(s => re.test(s.title))) add('error', 'required-section', `Missing required section matching ${re}`);
  }

  if (kind === 'prd') {
    const reqs = definedRequirements(text);
    const frs = [...reqs.keys()].filter(r => r.startsWith('FR'));
    const nfrs = [...reqs.keys()].filter(r => r.startsWith('NFR'));
    if (!frs.length) add('error', 'functional-requirements', 'No functional requirement (FR1, FR2…) defined');
    if (!nfrs.length) add(scale === 'solo' ? 'info' : 'warning', 'nfr', 'No non-functional requirement (NFR1…) defined');
    const vague = [...reqs].filter(([, t]) => /\b(fast|easy|user-friendly|intuitive|rapide|simple|facile|etc\.?)\b/i.test(t) && !/\d/.test(t));
    if (vague.length) add('warning', 'measurable', `Vague, non-measurable requirement(s): ${vague.slice(0, 6).map(([id]) => id).join(', ')}`);
  }

  if (kind === 'epics') {
    const epics = parseEpics(text);
    const stories = epics.flatMap(e => e.stories);
    if (!stories.length) add('error', 'stories', 'No "### Story N.M: …" found');
    const noCriteria = stories.filter(s => !s.hasCriteria).map(s => s.id);
    if (noCriteria.length) add('error', 'acceptance-criteria', `Stories without Given/When/Then acceptance criteria: ${noCriteria.join(', ')}`);
    const noReq = stories.filter(s => !s.requirements.length).map(s => s.id);
    if (noReq.length) add('warning', 'story-traceability', `Stories not linked to any FR/NFR: ${noReq.join(', ')}`);
    if (related.prd) {
      const defined = [...definedRequirements(related.prd).keys()].filter(r => r.startsWith('FR'));
      const covered = new Set(stories.flatMap(s => s.requirements));
      const uncovered = defined.filter(r => !covered.has(r));
      if (uncovered.length) add('error', 'fr-coverage', `PRD requirements not covered by any story: ${uncovered.join(', ')}`);
    }
  }

  if (kind === 'architecture' && related.prd) {
    const nfrs = [...definedRequirements(related.prd).keys()].filter(r => r.startsWith('NFR'));
    const mentioned = new Set(requirementIds(text));
    const missing = nfrs.filter(r => !mentioned.has(r));
    if (missing.length) add('warning', 'nfr-coverage', `NFRs from the PRD not addressed in the architecture: ${missing.join(', ')}`);
  }

  return { path, kind, scale, issues, ...gate(issues.filter(i => i.level !== 'info'), scale) };
}

// Finds the project's artifacts from the state (falls back to well-known file names under docs/ and mdan_output/).
export function projectArtifacts(projectRoot) {
  const found = {};
  for (const a of loadState(projectRoot).artifacts) {
    const full = join(projectRoot, a.path);
    if (!existsSync(full)) continue;
    const kind = detectKind(a.path, readFileSync(full, 'utf-8'));
    if (!found[kind]) found[kind] = a.path;
  }
  for (const dir of ['docs', 'mdan_output/planning-artifacts', 'mdan_output']) {
    const base = join(projectRoot, dir);
    if (!existsSync(base)) continue;
    for (const f of readdirSync(base).filter(f => f.endsWith('.md'))) {
      const rel = `${dir}/${f}`;
      const kind = detectKind(rel, readFileSync(join(base, f), 'utf-8'));
      if (!found[kind]) found[kind] = rel;
    }
  }
  return found;
}

export function checkProject(projectRoot, { scale = detectScale(projectRoot).scale, paths = null } = {}) {
  const artifacts = paths ? Object.fromEntries(paths.map(p => [detectKind(p, readFileSync(join(projectRoot, p), 'utf-8')), p])) : projectArtifacts(projectRoot);
  const texts = Object.fromEntries(Object.entries(artifacts).map(([k, p]) => [k, readFileSync(join(projectRoot, p), 'utf-8')]));
  const related = { prd: texts.prd, architecture: texts.architecture, epics: texts.epics };
  const results = Object.entries(artifacts).map(([kind, p]) => checkArtifact(p, texts[kind], { kind, scale, related }));
  const decision = results.some(r => r.decision === 'FAIL') ? 'FAIL' : results.some(r => r.decision === 'CONCERNS') ? 'CONCERNS' : 'PASS';
  return { scale, decision, results };
}

// ---------- traceability ----------

const TEST_FILE = /\.(test|spec)\.[cm]?[jt]sx?$|_test\.(go|py)$|^test_.*\.py$|Tests?\.cs$|\.feature$/;
const IGNORED_DIRS = new Set(['node_modules', '.git', 'dist', 'build', 'bin', 'obj', '_mdan', 'mdan_output', '.claude', 'coverage']);

function testFiles(root, dir = root, out = []) {
  let entries;
  try { entries = readdirSync(dir); } catch { return out; }
  for (const name of entries) {
    if (IGNORED_DIRS.has(name)) continue;
    const full = join(dir, name);
    let st;
    try { st = statSync(full); } catch { continue; }
    if (st.isDirectory()) testFiles(root, full, out);
    else if (TEST_FILE.test(name) && st.size < 2_000_000) out.push(full);
  }
  return out;
}

const STORY_REF = /\bstory[\s_-]?(\d+)[._-](\d+)\b/gi;

/**
 * Requirement → stories → tests matrix. Tests reference requirements by id (FR3, NFR-2) or stories by
 * "Story 1.2" / "story-1-2" in their name or content.
 */
export function traceability(projectRoot, { scale = detectScale(projectRoot).scale } = {}) {
  const artifacts = projectArtifacts(projectRoot);
  if (!artifacts.prd) throw new Error('No PRD found (register it with mdan_state_update or put it under docs/).');
  const prd = readFileSync(join(projectRoot, artifacts.prd), 'utf-8');
  const requirements = definedRequirements(prd);
  const epics = artifacts.epics ? parseEpics(readFileSync(join(projectRoot, artifacts.epics), 'utf-8')) : [];
  const stories = epics.flatMap(e => e.stories);

  const tests = testFiles(projectRoot).map(f => {
    const content = readFileSync(f, 'utf-8');
    const hay = `${basename(f)}\n${content}`;
    return {
      file: relative(projectRoot, f).split(sep).join('/'),
      requirements: requirementIds(hay),
      stories: [...new Set([...hay.matchAll(STORY_REF)].map(m => `${Number(m[1])}.${Number(m[2])}`))],
    };
  });

  const rows = [...requirements].map(([id, text]) => {
    const coveringStories = stories.filter(s => s.requirements.includes(id)).map(s => s.id);
    const coveringTests = tests.filter(t => t.requirements.includes(id) || t.stories.some(s => coveringStories.includes(s))).map(t => t.file);
    return { id, text, stories: coveringStories, tests: coveringTests };
  });

  const frRows = rows.filter(r => r.id.startsWith('FR'));
  const withStories = frRows.filter(r => r.stories.length).length;
  const withTests = rows.filter(r => r.tests.length).length;
  const storyCoverage = frRows.length ? withStories / frRows.length : 1;
  const testCoverage = rows.length ? withTests / rows.length : 1;
  const threshold = { solo: 0, team: 0.8, enterprise: 1 }[scale];

  let decision = 'PASS';
  if (storyCoverage < 1) decision = 'FAIL';
  else if (testCoverage < threshold) decision = scale === 'enterprise' ? 'FAIL' : 'CONCERNS';

  return {
    scale,
    prd: artifacts.prd,
    epics: artifacts.epics || null,
    rows,
    untestedStories: stories.filter(s => !tests.some(t => t.stories.includes(s.id) || s.requirements.some(r => t.requirements.includes(r)))).map(s => s.id),
    coverage: { stories: storyCoverage, tests: testCoverage, threshold },
    decision,
  };
}

const slug = s => s.replace(/[^A-Za-z0-9_.-]+/g, '-').replace(/^[-.]+/, '').slice(0, 100);

// Writes the traceability matrix into the context graph: requirement → story → test (relation input_to),
// so `mdan impact FR3` answers "which stories and tests depend on this requirement".
export function registerTrace(projectRoot, trace, ContextGraph, graphPath) {
  let added = 0;
  ContextGraph.update(graphPath, g => {
    const ensure = (id, path, metadata) => {
      if (!g.getNode(id)) { g.addNode({ id, path, metadata }, null); added++; }
    };
    const link = (source, target) => {
      try { g.addEdge({ source, target, relation: 'input_to' }); } catch { /* duplicate or cycle: ignore */ }
    };
    for (const row of trace.rows) {
      ensure(row.id, trace.prd, { kind: 'requirement', text: row.text });
      for (const s of row.stories) {
        ensure(`story-${s}`, trace.epics, { kind: 'story' });
        link(row.id, `story-${s}`);
      }
      for (const file of row.tests) {
        const testId = `test-${slug(file)}`;
        ensure(testId, file, { kind: 'test' });
        const viaStory = row.stories.find(s => g.getNode(`story-${s}`));
        link(viaStory ? `story-${viaStory}` : row.id, testId);
      }
    }
  });
  return added;
}
