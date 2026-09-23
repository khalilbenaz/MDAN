import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, dirname, relative, sep } from 'node:path';

const TEXT_EXT = /\.(md|xml|yaml|yml|csv|json)$/;
const PROJECT_REF = /\{project-root\}\/([^\s`'"()<>\]|,]+)/g;
const RELATIVE_REF = /^\s*[A-Za-z]+File:\s*['"]?(\.{1,2}\/[^\s'"]+)/gm;

export function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) walk(full, out);
    else out.push(full);
  }
  return out;
}

// Files created at runtime by workflows or the user, not shipped in the package.
const RUNTIME_PREFIXES = ['mdan_output/', 'docs/', '_mdan/state/MDAN-STATE.json', '_mdan/state/sidecars/'];

function clean(p) {
  return p.replace(/[.:;]+$/, '');
}

// Returns [{ file, ref, resolved }] for every file reference that does not exist.
export function findBrokenRefs(root, dirs = ['_mdan', '.claude/commands']) {
  const broken = [];
  for (const d of dirs) {
    const base = join(root, d);
    if (!existsSync(base)) continue;
    for (const file of walk(base)) {
      if (!TEXT_EXT.test(file)) continue;
      let text = readFileSync(file, 'utf-8');
      if (/\.ya?ml$/.test(file)) text = text.replace(/^\s*#.*$/gm, '');
      const rel = relative(root, file).split(sep).join('/');
      for (const m of text.matchAll(PROJECT_REF)) {
        const ref = clean(m[1]);
        if (ref.includes('{') || ref.includes('*') || !/\.[a-z]+$/.test(ref)) continue;
        if (RUNTIME_PREFIXES.some(p => ref.startsWith(p))) continue;
        if (!existsSync(join(root, ref))) broken.push({ file: rel, ref: `{project-root}/${ref}` });
      }
      for (const m of text.matchAll(RELATIVE_REF)) {
        const ref = clean(m[1]);
        if (ref.includes('{')) continue;
        if (!existsSync(join(dirname(file), ref))) broken.push({ file: rel, ref });
      }
    }
  }
  return broken;
}
