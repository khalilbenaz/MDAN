import { writeFileSync, renameSync, mkdirSync, rmSync, statSync } from 'node:fs';
import { dirname } from 'node:path';

export function writeFileAtomic(filePath, data) {
  mkdirSync(dirname(filePath), { recursive: true });
  const tmp = `${filePath}.${process.pid}.${Date.now()}.tmp`;
  writeFileSync(tmp, data);
  renameSync(tmp, filePath);
}

const sleep = ms => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);

// Cross-process exclusive section based on an atomic mkdir. Stale locks (> staleMs) are broken.
export function withLock(filePath, fn, { timeoutMs = 5000, staleMs = 30000 } = {}) {
  const lock = `${filePath}.lock`;
  mkdirSync(dirname(filePath), { recursive: true });
  const start = Date.now();
  for (;;) {
    try {
      mkdirSync(lock);
      break;
    } catch (err) {
      if (err.code !== 'EEXIST') throw err;
      try {
        if (Date.now() - statSync(lock).mtimeMs > staleMs) { rmSync(lock, { recursive: true, force: true }); continue; }
      } catch { continue; }
      if (Date.now() - start > timeoutMs) throw new Error(`Timed out waiting for lock ${lock}`, { cause: err });
      sleep(25);
    }
  }
  try {
    return fn();
  } finally {
    rmSync(lock, { recursive: true, force: true });
  }
}
