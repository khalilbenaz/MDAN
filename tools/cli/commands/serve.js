import { startServer } from '../../mcp/server.js';

export default async function serve(args) {
  const transport = args.includes('--sse') ? 'sse' : 'stdio';
  const port = args.find((a, i) => args[i - 1] === '--port') || 3100;

  console.error(`[mdan] Starting MCP server (${transport})...`);
  await startServer({ transport, port: Number(port) });
}
