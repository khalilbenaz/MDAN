// Export the epics/stories document to a tracker: CSV, GitHub Issues, Azure DevOps Boards or Jira.
// Idempotent: created ids are stored in _mdan/state/export-<target>.json and re-runs update instead of duplicating.
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { parseEpics, sections, projectArtifacts } from './quality.js';
import { toCsv } from './csv.js';
import { writeFileAtomic } from './fs-atomic.js';

export const TARGETS = ['csv', 'github', 'ado', 'jira'];

export function buildBacklog(projectRoot, epicsPath = projectArtifacts(projectRoot).epics) {
  if (!epicsPath) throw new Error('No epics document found (run /mdan-create-epics-and-stories or pass --file).');
  const text = readFileSync(join(projectRoot, epicsPath), 'utf-8');
  const goals = Object.fromEntries(sections(text)
    .map(s => [s.title.match(/^Epic\s+(\d+)/i)?.[1], s.body.split(/\n(?=#{3,}\s)/)[0].trim()])
    .filter(([id]) => id));
  const epics = parseEpics(text).map(e => ({
    key: `E${e.id}`,
    title: e.title || `Epic ${e.id}`,
    description: goals[e.id] || '',
    stories: e.stories.map(s => ({
      key: `S${s.id}`,
      title: s.title,
      description: s.body.trim(),
      requirements: s.requirements,
    })),
  }));
  if (!epics.length) throw new Error(`No "## Epic N:" / "### Story N.M:" found in ${epicsPath}`);
  return { source: epicsPath, epics };
}

const mappingPath = (root, target) => join(root, `_mdan/state/export-${target}.json`);
const loadMapping = (root, target) => (existsSync(mappingPath(root, target)) ? JSON.parse(readFileSync(mappingPath(root, target), 'utf-8')) : {});

export function toCsvExport(backlog) {
  const rows = backlog.epics.flatMap(e => [
    { type: 'Epic', key: e.key, parent: '', title: e.title, description: e.description, requirements: '' },
    ...e.stories.map(s => ({ type: 'Story', key: s.key, parent: e.key, title: s.title, description: s.description, requirements: s.requirements.join(' ') })),
  ]);
  return toCsv(['type', 'key', 'parent', 'title', 'description', 'requirements'], rows);
}

// ---------- adapters: each turns an item into an HTTP request, and a response into an external id ----------

const adf = textValue => ({
  type: 'doc',
  version: 1,
  content: textValue.split(/\n{2,}/).filter(Boolean).map(p => ({ type: 'paragraph', content: [{ type: 'text', text: p }] })),
});

export const ADAPTERS = {
  github: {
    env: ['GITHUB_TOKEN|GH_TOKEN'],
    options: ['repo'],
    request(item, { repo, token, parentRef, existing }) {
      const body = `${item.description}${parentRef ? `\n\nPart of #${parentRef}` : ''}${item.requirements?.length ? `\n\nRequirements: ${item.requirements.join(', ')}` : ''}\n\n<!-- mdan:${item.key} -->`;
      return {
        method: existing ? 'PATCH' : 'POST',
        url: `https://api.github.com/repos/${repo}/issues${existing ? `/${existing}` : ''}`,
        headers: { authorization: `Bearer ${token}`, accept: 'application/vnd.github+json', 'content-type': 'application/json' },
        body: { title: `${item.key} ${item.title}`, body, labels: [item.kind === 'epic' ? 'epic' : 'story'] },
      };
    },
    id: json => json.number,
  },
  ado: {
    env: ['AZURE_DEVOPS_PAT|AZURE_DEVOPS_EXT_PAT'],
    options: ['org', 'project'],
    request(item, { org, project, token, parentRef, existing }) {
      const base = `https://dev.azure.com/${encodeURIComponent(org)}/${encodeURIComponent(project)}/_apis/wit/workitems`;
      const ops = [
        { op: 'add', path: '/fields/System.Title', value: `${item.key} ${item.title}` },
        { op: 'add', path: '/fields/System.Description', value: item.description.replace(/\n/g, '<br/>') },
        { op: 'add', path: '/fields/System.Tags', value: `mdan; ${item.key}${item.requirements?.length ? `; ${item.requirements.join('; ')}` : ''}` },
      ];
      if (parentRef && !existing) {
        ops.push({ op: 'add', path: '/relations/-', value: { rel: 'System.LinkTypes.Hierarchy-Reverse', url: `https://dev.azure.com/${encodeURIComponent(org)}/_apis/wit/workItems/${parentRef}` } });
      }
      const type = item.kind === 'epic' ? 'Epic' : 'User Story';
      return {
        method: existing ? 'PATCH' : 'POST',
        url: existing ? `${base}/${existing}?api-version=7.1` : `${base}/$${encodeURIComponent(type)}?api-version=7.1`,
        headers: { authorization: `Basic ${Buffer.from(`:${token}`).toString('base64')}`, 'content-type': 'application/json-patch+json' },
        body: ops,
      };
    },
    id: json => json.id,
  },
  jira: {
    env: ['JIRA_API_TOKEN', 'JIRA_EMAIL'],
    options: ['url', 'project'],
    request(item, { url, project, token, email, parentRef, existing }) {
      const fields = {
        summary: `${item.key} ${item.title}`,
        description: adf(item.description || item.title),
        labels: ['mdan', ...(item.requirements || [])],
      };
      if (!existing) {
        fields.project = { key: project };
        fields.issuetype = { name: item.kind === 'epic' ? 'Epic' : 'Story' };
        if (parentRef) fields.parent = { key: parentRef };
      }
      return {
        method: existing ? 'PUT' : 'POST',
        url: `${url.replace(/\/$/, '')}/rest/api/3/issue${existing ? `/${existing}` : ''}`,
        headers: { authorization: `Basic ${Buffer.from(`${email}:${token}`).toString('base64')}`, 'content-type': 'application/json', accept: 'application/json' },
        body: { fields },
      };
    },
    id: json => json.key,
  },
};

function readEnv(spec) {
  for (const name of spec.split('|')) if (process.env[name]) return process.env[name];
  return null;
}

/**
 * Plans (dry run) or applies the export. `fetchImpl` is injectable for tests.
 * @returns {{ operations: object[], created: number, updated: number }}
 */
export async function exportBacklog(projectRoot, target, { apply = false, options = {}, fetchImpl = globalThis.fetch, file } = {}) {
  if (!TARGETS.includes(target) || target === 'csv') throw new Error(`Unsupported target '${target}' (expected ${TARGETS.filter(t => t !== 'csv').join(', ')})`);
  const adapter = ADAPTERS[target];
  const missing = adapter.options.filter(o => !options[o]);
  if (missing.length) throw new Error(`Missing option(s) for ${target}: ${missing.map(o => `--${o}`).join(', ')}`);
  const token = readEnv(adapter.env[0]);
  const email = adapter.env[1] ? readEnv(adapter.env[1]) : undefined;
  if (apply && (!token || (adapter.env[1] && !email))) throw new Error(`Set ${adapter.env.join(' and ')} to export to ${target}`);

  const backlog = buildBacklog(projectRoot, file);
  const mapping = loadMapping(projectRoot, target);
  const operations = [];
  let created = 0;
  let updated = 0;

  const send = async (item, parentRef) => {
    const existing = mapping[item.key];
    const req = adapter.request(item, { ...options, token: token || '<token>', email: email || '<email>', parentRef, existing });
    operations.push({ key: item.key, method: req.method, url: req.url, body: req.body });
    if (!apply) return existing || `<${item.key}>`;
    const res = await fetchImpl(req.url, { method: req.method, headers: req.headers, body: JSON.stringify(req.body) });
    if (!res.ok) throw new Error(`${target} ${req.method} ${req.url} failed: ${res.status} ${await res.text().catch(() => '')}`.slice(0, 500));
    if (existing) { updated++; return existing; }
    const text = await res.text();
    const id = adapter.id(text ? JSON.parse(text) : {});
    mapping[item.key] = id;
    created++;
    writeFileAtomic(mappingPath(projectRoot, target), JSON.stringify(mapping, null, 2) + '\n');
    return id;
  };

  for (const epic of backlog.epics) {
    const epicRef = await send({ ...epic, kind: 'epic' });
    for (const story of epic.stories) await send({ ...story, kind: 'story' }, epicRef);
  }
  return { source: backlog.source, target, apply, operations, created, updated };
}
