#!/usr/bin/env node
import { VERSION } from '../lib/paths.js';

const commands = {
  install: { load: () => import('./commands/install.js'), summary: 'Install MDAN into a project (interactive)' },
  update: { load: () => import('./commands/install.js'), summary: 'Update an existing install, keeping your changes', options: { update: true } },
  status: { load: () => import('./commands/status.js'), summary: 'Where the project is and what to do next' },
  memory: { load: () => import('./commands/memory.js'), summary: 'Show or edit agent memories' },
  serve: { load: () => import('./commands/serve.js'), summary: 'Start the MCP server (stdio, or --http)' },
  graph: { load: () => import('./commands/graph.js'), summary: 'Output the context graph (Mermaid, --json, --html <file>)' },
  impact: { load: () => import('./commands/impact.js'), summary: 'Upstream/downstream impact of an artifact' },
  stale: { load: () => import('./commands/stale.js'), summary: 'Artifacts changed since registration and what to review' },
  validate: { load: () => import('./commands/validate.js'), summary: 'Check that every file reference in _mdan resolves' },
};

function usage() {
  const width = Math.max(...Object.keys(commands).map(k => k.length));
  console.log(`MDAN v${VERSION}\n\nUsage: mdan <command> [options]\n\nCommands:`);
  for (const [name, c] of Object.entries(commands)) console.log(`  ${name.padEnd(width)}  ${c.summary}`);
  console.log('\nRun `mdan <command> --help` for details.');
}

const [command, ...rest] = process.argv.slice(2);

if (command === '--version' || command === '-v') {
  console.log(VERSION);
} else if (!command || command === '--help' || command === '-h' || command === 'help') {
  usage();
} else if (!commands[command]) {
  console.error(`Unknown command: ${command}\n`);
  usage();
  process.exit(1);
} else {
  try {
    const mod = await commands[command].load();
    await mod.default(rest, commands[command].options);
  } catch (err) {
    console.error(`[mdan] ${err.message}`);
    if (process.env.MDAN_DEBUG) console.error(err.stack);
    process.exit(1);
  }
}
