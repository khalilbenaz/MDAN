#!/usr/bin/env node
// `mdan-mcp` binary: same as `mdan serve`.
import serve from '../cli/commands/serve.js';

await serve(process.argv.slice(2));
