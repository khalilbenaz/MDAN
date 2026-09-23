#!/usr/bin/env node
// Checks that every file reference inside MDAN content resolves to an existing file.
import { findBrokenRefs } from '../lib/refs.js';

const root = process.argv[2] || process.cwd();
const broken = findBrokenRefs(root);
for (const b of broken) console.log(`${b.file}: ${b.ref}`);
console.log(`\n${broken.length} broken reference(s)`);
process.exit(broken.length ? 1 : 0);
