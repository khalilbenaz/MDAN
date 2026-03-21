import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { existsSync } from 'node:fs';

export async function discoverMdan(projectRoot) {
  const mdanDir = join(projectRoot, '_mdan');
  const configDir = join(mdanDir, '_config');

  const result = {
    modules: [],
    workflows: [],
    agents: [],
    teams: [],
    manifest: null,
  };

  // Load manifest
  const manifestPath = join(configDir, 'manifest.yaml');
  if (existsSync(manifestPath)) {
    result.manifest = await readFile(manifestPath, 'utf-8');
  }

  // Load workflow manifest (CSV)
  const workflowCsv = join(configDir, 'workflow-manifest.csv');
  if (existsSync(workflowCsv)) {
    result.workflows = parseCsv(await readFile(workflowCsv, 'utf-8'));
  }

  // Load agent manifest (CSV)
  const agentCsv = join(configDir, 'agent-manifest.csv');
  if (existsSync(agentCsv)) {
    result.agents = parseCsv(await readFile(agentCsv, 'utf-8'));
  }

  // Extract module names from manifest
  if (result.manifest) {
    const moduleMatches = result.manifest.matchAll(/- name: (\S+)/g);
    for (const m of moduleMatches) {
      result.modules.push(m[1]);
    }
  }

  return result;
}

function parseCsv(content) {
  const lines = content.trim().split('\n');
  if (lines.length < 2) return [];

  const headers = parseCsvLine(lines[0]);
  return lines.slice(1).map(line => {
    const values = parseCsvLine(line);
    const obj = {};
    headers.forEach((h, i) => { obj[h] = values[i] || ''; });
    return obj;
  });
}

function parseCsvLine(line) {
  const result = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && line[i + 1] === '"') {
        current += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (ch === ',' && !inQuotes) {
      result.push(current.trim());
      current = '';
    } else {
      current += ch;
    }
  }
  result.push(current.trim());
  return result;
}
