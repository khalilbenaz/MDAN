#!/usr/bin/env node
import { parseArgs } from 'node:util';
import { resolve } from 'node:path';

const args = process.argv.slice(2);
const command = args[0];

const commands = {
  serve: () => import('./commands/serve.js'),
  impact: () => import('./commands/impact.js'),
  graph: () => import('./commands/graph.js'),
};

if (!command || !commands[command]) {
  console.log('Usage: mdan <command>\n\nCommands:');
  console.log('  serve    Start MCP server');
  console.log('  impact   Analyze artifact impact');
  console.log('  graph    Output context graph as Mermaid');
  process.exit(command ? 1 : 0);
}

const mod = await commands[command]();
await mod.default(args.slice(1));
