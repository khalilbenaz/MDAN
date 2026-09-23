import { resolve, relative, isAbsolute, join } from 'node:path';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

export const PACKAGE_ROOT = fileURLToPath(new URL('../../', import.meta.url));

export const VERSION = JSON.parse(readFileSync(join(PACKAGE_ROOT, 'package.json'), 'utf-8')).version;

const ID = /^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$/;

// Identifiers end up in file names: letters, digits, "_", "-", "." only, no leading dot.
export function assertId(value, label = 'id') {
  if (typeof value !== 'string' || !ID.test(value) || value.includes('..')) {
    throw new Error(`Invalid ${label}: ${JSON.stringify(value)} (allowed: letters, digits, _ - .)`);
  }
  return value;
}

// Joins `parts` under `base` and refuses any result that escapes `base`.
export function safeJoin(base, ...parts) {
  const root = resolve(base);
  const target = resolve(root, ...parts);
  const rel = relative(root, target);
  if (rel.startsWith('..') || isAbsolute(rel)) {
    throw new Error(`Path escapes ${root}: ${parts.join('/')}`);
  }
  return target;
}

export function projectRootFromEnv() {
  return resolve(process.env.MDAN_PROJECT_ROOT || process.cwd());
}
