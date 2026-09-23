import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { existsSync } from 'node:fs';
import { parseCsv } from '../lib/csv.js';

// Reads what is installed in the project (the manifests written by `mdan install`).
export async function discoverMdan(projectRoot) {
  const configDir = join(projectRoot, '_mdan', '_config');
  const readCsv = async name => {
    const p = join(configDir, name);
    return existsSync(p) ? parseCsv(await readFile(p, 'utf-8')) : [];
  };

  const manifestPath = join(configDir, 'manifest.yaml');
  const manifest = existsSync(manifestPath) ? await readFile(manifestPath, 'utf-8') : null;
  const modules = manifest ? [...manifest.matchAll(/^\s*- name: (\S+)/gm)].map(m => m[1]) : [];

  const workflows = (await readCsv('workflow-manifest.csv'))
    .map(w => ({ ...w, kind: w.path.endsWith('.yaml') ? 'yaml' : 'wizard' }));

  return {
    installed: existsSync(join(projectRoot, '_mdan')),
    manifest,
    modules,
    workflows,
    agents: await readCsv('agent-manifest.csv'),
    tasks: await readCsv('task-manifest.csv'),
  };
}
