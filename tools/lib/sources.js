// Single source of truth: reads agents, workflows and tasks directly from the content files.
// The CSV manifests and IDE commands are derived from this by tools/build/build.js.
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, relative, sep, basename, extname } from 'node:path';
import { parseFrontmatter, parseYamlScalars } from './frontmatter.js';

const toPosix = p => p.split(sep).join('/');

function listDir(dir) {
  return existsSync(dir) ? readdirSync(dir).sort() : [];
}

export function modulesOf(root) {
  return listDir(join(root, '_mdan')).filter(d => !d.startsWith('_') && d !== 'state' && d !== 'custom'
    && statSync(join(root, '_mdan', d)).isDirectory());
}

function decodeXml(s) {
  return s.replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
}

function attr(tag, name) {
  const m = tag.match(new RegExp(`\\b${name}="([^"]*)"`));
  return m ? decodeXml(m[1]) : '';
}

function element(text, name) {
  const m = text.match(new RegExp(`<${name}>([\\s\\S]*?)</${name}>`));
  return m ? decodeXml(m[1].replace(/\s+/g, ' ').trim()) : '';
}

function assertUnique(items, label) {
  const seen = new Set();
  for (const i of items) {
    if (seen.has(i.name)) throw new Error(`Duplicate ${label} name: ${i.name}`);
    seen.add(i.name);
  }
}

export function readAgents(root) {
  const agents = [];
  for (const module of modulesOf(root)) {
    const dir = join(root, '_mdan', module, 'agents');
    for (const file of listDir(dir).filter(f => f.endsWith('.md'))) {
      const full = join(dir, file);
      const text = readFileSync(full, 'utf-8');
      const tag = text.match(/<agent\b[^>]*>/)?.[0];
      if (!tag) continue;
      agents.push({
        name: attr(tag, 'id').replace(/\.agent\.yaml$/, '') || basename(file, '.md'),
        displayName: attr(tag, 'name'),
        title: attr(tag, 'title'),
        icon: attr(tag, 'icon'),
        capabilities: attr(tag, 'capabilities'),
        role: element(text, 'role'),
        identity: element(text, 'identity'),
        communicationStyle: element(text, 'communication_style'),
        principles: element(text, 'principles'),
        module,
        path: toPosix(relative(root, full)),
      });
    }
  }
  assertUnique(agents, 'agent');
  return agents;
}

function walkWorkflows(dir, out) {
  for (const name of listDir(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) {
      if (name !== 'steps' && !name.endsWith('-steps') && name !== 'templates') walkWorkflows(full, out);
    } else if (name === 'wizard.md' || name === 'workflow.yaml' || /^workflow-.+\.md$/.test(name)) {
      out.push(full);
    }
  }
  return out;
}

export function readWorkflows(root) {
  const workflows = [];
  for (const module of modulesOf(root)) {
    for (const full of walkWorkflows(join(root, '_mdan', module, 'workflows'), [])) {
      const text = readFileSync(full, 'utf-8');
      const meta = full.endsWith('.yaml') ? parseYamlScalars(text) : parseFrontmatter(text);
      if (!meta.name) throw new Error(`Workflow without "name": ${toPosix(relative(root, full))}`);
      workflows.push({
        name: meta.name,
        description: meta.description || '',
        module,
        path: toPosix(relative(root, full)),
        kind: full.endsWith('.yaml') ? 'yaml' : 'wizard',
      });
    }
  }
  assertUnique(workflows, 'workflow');
  return workflows.sort((a, b) => a.path.localeCompare(b.path));
}

export function readTasks(root) {
  const tasks = [];
  for (const module of modulesOf(root)) {
    const dir = join(root, '_mdan', module, 'tasks');
    for (const file of listDir(dir)) {
      const full = join(dir, file);
      const ext = extname(file);
      const text = readFileSync(full, 'utf-8');
      let meta;
      if (ext === '.xml') {
        const tag = text.match(/<task\b[^>]*>/)?.[0];
        if (!tag || attr(tag, 'internal') === 'true') continue;
        meta = { displayName: attr(tag, 'name'), description: attr(tag, 'description') };
      } else if (ext === '.md') {
        const fm = parseFrontmatter(text);
        meta = { displayName: fm.name, description: fm.description };
      } else continue;
      tasks.push({
        name: basename(file, ext),
        displayName: meta.displayName || basename(file, ext),
        description: meta.description || '',
        module,
        path: toPosix(relative(root, full)),
        standalone: 'true',
      });
    }
  }
  assertUnique(tasks, 'task');
  return tasks;
}

export function readSources(root) {
  return { agents: readAgents(root), workflows: readWorkflows(root), tasks: readTasks(root) };
}
