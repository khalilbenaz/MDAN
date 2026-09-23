import { parseArgs } from 'node:util';

export const help = `Usage: mdan serve [--http] [--port 3100] [--host 127.0.0.1]

Starts the MDAN MCP server. Default transport is stdio.
  --http        Streamable HTTP transport on /mcp (health check on /health)
  --sse         Deprecated alias of --http
  --port <n>    HTTP port (default 3100, or $PORT)
  --host <h>    HTTP bind address (default 127.0.0.1, or $HOST)`;

export default async function serve(argv) {
  const { values } = parseArgs({
    args: argv,
    options: {
      http: { type: 'boolean' },
      sse: { type: 'boolean' },
      port: { type: 'string' },
      host: { type: 'string' },
      help: { type: 'boolean', short: 'h' },
    },
  });
  if (values.help) return console.log(help);
  if (values.sse) console.error('[mdan] --sse is deprecated (SSE transport was removed from the MCP spec); using --http.');

  let startServer;
  try {
    ({ startServer } = await import('../../mcp/server.js'));
  } catch (err) {
    if (err.code !== 'ERR_MODULE_NOT_FOUND') throw err;
    console.error(`[mdan] Missing dependency: ${err.message}\n[mdan] Reinstall the package: npm install mdan-method`);
    process.exit(1);
  }

  const port = Number(values.port ?? process.env.PORT ?? 3100);
  if (!Number.isInteger(port) || port < 0 || port > 65535) throw new Error(`Invalid port: ${values.port}`);
  await startServer({
    transport: values.http || values.sse ? 'http' : 'stdio',
    port,
    host: values.host ?? process.env.HOST ?? '127.0.0.1',
  });
}
