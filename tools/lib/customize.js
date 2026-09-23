// Layered agent customization, merged in order (later wins):
//   1. shipped template  _mdan/_config/agents/<module>-<agent>.customize.yaml
//   2. team (versioned)  _mdan/custom/<agent>.yaml
//   3. personal          _mdan/custom/<agent>.user.yaml   (git-ignored via _mdan/custom/.gitignore)
// Schema: agent.metadata.name, persona {role, identity, communication_style, principles[]},
// critical_actions[], memories[], menu[], prompts[].
import { readFileSync, existsSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import YAML from 'yaml';
import { assertId, safeJoin } from './paths.js';
import { writeFileAtomic } from './fs-atomic.js';

export const LAYERS = ['shipped', 'team', 'user'];

const isEmpty = v => v === '' || v === null || v === undefined || (Array.isArray(v) && !v.length)
  || (typeof v === 'object' && !Array.isArray(v) && Object.values(v).every(isEmpty));

// Deep merge: empty values never override, arrays are concatenated without duplicates.
export function mergeLayers(...layers) {
  const merge = (a, b) => {
    if (isEmpty(b)) return a;
    if (Array.isArray(a) && Array.isArray(b)) {
      const seen = new Set(a.map(x => JSON.stringify(x)));
      return [...a, ...b.filter(x => !seen.has(JSON.stringify(x)))];
    }
    if (a && b && typeof a === 'object' && typeof b === 'object' && !Array.isArray(a) && !Array.isArray(b)) {
      const out = { ...a };
      for (const [k, v] of Object.entries(b)) out[k] = k in out ? merge(out[k], v) : v;
      return out;
    }
    return b;
  };
  return layers.reduce((acc, l) => merge(acc, l || {}), {});
}

export function layerPath(root, agent, layer, module = null) {
  assertId(agent, 'agent name');
  if (layer === 'shipped') return safeJoin(root, '_mdan/_config/agents', `${module}-${agent}.customize.yaml`);
  return safeJoin(root, '_mdan/custom', layer === 'user' ? `${agent}.user.yaml` : `${agent}.yaml`);
}

function readLayer(file) {
  if (!existsSync(file)) return null;
  try {
    return YAML.parse(readFileSync(file, 'utf-8')) || {};
  } catch (err) {
    throw new Error(`Invalid YAML in ${file}: ${err.message}`, { cause: err });
  }
}

// The shipped layer lives with the content, team/user layers in the project (they differ when the
// MCP server serves bundled content for a project without an install).
export function resolveCustomization(contentRoot, projectRoot, agent, module) {
  const layers = {
    shipped: readLayer(layerPath(contentRoot, agent, 'shipped', module)),
    team: readLayer(layerPath(projectRoot, agent, 'team')),
    user: readLayer(layerPath(projectRoot, agent, 'user')),
  };
  // `agent.metadata.hasSidecar` is template boilerplate, not a customization.
  if (layers.shipped?.agent?.metadata) delete layers.shipped.agent.metadata.hasSidecar;
  const merged = mergeLayers(layers.shipped, layers.team, layers.user);
  return { layers: Object.fromEntries(Object.entries(layers).map(([k, v]) => [k, v !== null])), merged, empty: isEmpty(merged) };
}

// Adds/overrides fields in the team or user layer (merged with what the layer already has).
export function customize(root, agent, layer, patch) {
  if (!['team', 'user'].includes(layer)) throw new Error(`Layer must be "team" or "user", got '${layer}'`);
  const file = layerPath(root, agent, layer);
  const next = mergeLayers(readLayer(file) || {}, patch);
  mkdirSync(dirname(file), { recursive: true });
  const ignore = join(root, '_mdan/custom/.gitignore');
  if (!existsSync(ignore)) writeFileSync(ignore, '# Personal agent customizations stay out of git\n*.user.yaml\n');
  writeFileAtomic(file, `# ${layer === 'team' ? 'Team (versioned)' : 'Personal (git-ignored)'} customization for ${agent}\n${YAML.stringify(next)}`);
  return { file, merged: next };
}

export function renderCustomization(resolved) {
  if (resolved.empty) return '';
  const active = LAYERS.filter(l => resolved.layers[l]).join(' < ');
  return `## Customization (layers: ${active}; later wins)\n\n\`\`\`yaml\n${YAML.stringify(resolved.merged)}\`\`\`\n` +
    'Apply it: persona fields replace the defaults, critical_actions run after activation, memories are facts to keep in mind, menu items are added to the menu.';
}
