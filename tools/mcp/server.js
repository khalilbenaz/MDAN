import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { createServer as createHttpServer } from 'node:http';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import { VERSION, PACKAGE_ROOT, projectRootFromEnv } from '../lib/paths.js';
import { discoverMdan } from './discovery.js';
import { registerWorkflowTools } from './tools/workflow-tools.js';
import { registerAgentTools } from './tools/agent-tools.js';
import { registerGraphTools } from './tools/graph-tools.js';
import { registerOrchestrationTools } from './tools/orchestration-tools.js';
import { registerEcosystemTools } from './tools/ecosystem-tools.js';
import { registerStateTools } from './tools/state-tools.js';
import { registerMemoryTools } from './tools/memory-tools.js';
import { registerQualityTools } from './tools/quality-tools.js';
import { registerResources } from './resources.js';

const log = msg => console.error(`[mdan] ${msg}`);

// When the project has no MDAN install, serve the content bundled in the package (read-only);
// graph and decision records are still written to the project.
export async function resolveRoots(projectRoot = projectRootFromEnv()) {
  const installed = existsSync(join(projectRoot, '_mdan', '_config', 'workflow-manifest.csv'));
  return { projectRoot, contentRoot: installed ? projectRoot : PACKAGE_ROOT, installed };
}

export async function createMcpServer({ projectRoot, contentRoot }) {
  const discovery = await discoverMdan(contentRoot);
  const server = new McpServer(
    { name: 'mdan', version: VERSION },
    { instructions: 'MDAN: AI-driven development methodology. Start with mdan_status (where the project is, what to do next). Use mdan_run_workflow to run or resume a wizard and mdan_state_update to record progress, mdan_consult_agent for an expert persona (with its memories), mdan_party_mode for multi-agent debate, mdan_memory_* for agent memory and mdan_graph_* to track artifacts.' },
  );

  registerWorkflowTools(server, discovery, contentRoot, projectRoot);
  registerAgentTools(server, discovery, contentRoot, projectRoot);
  registerGraphTools(server, projectRoot);
  registerOrchestrationTools(server, discovery, projectRoot, contentRoot);
  registerEcosystemTools(server, contentRoot);
  registerStateTools(server, discovery, projectRoot);
  registerMemoryTools(server, projectRoot);
  registerQualityTools(server, projectRoot);
  registerResources(server, discovery, projectRoot);
  return server;
}

async function startHttp(roots, { port, host }) {
  const http = createHttpServer(async (req, res) => {
    const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
    if (url.pathname === '/health') {
      res.writeHead(200, { 'content-type': 'application/json' }).end(JSON.stringify({ status: 'ok', version: VERSION }));
      return;
    }
    if (url.pathname !== '/mcp') {
      res.writeHead(404).end('Not found. MCP endpoint: /mcp');
      return;
    }
    if (req.method !== 'POST') {
      res.writeHead(405, { allow: 'POST' }).end(JSON.stringify({ jsonrpc: '2.0', error: { code: -32000, message: 'Method not allowed (stateless server: POST only)' }, id: null }));
      return;
    }
    // Stateless mode: one server + transport per request, as recommended by the SDK.
    try {
      const server = await createMcpServer(roots);
      const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
      res.on('close', () => { transport.close(); server.close(); });
      await server.connect(transport);
      await transport.handleRequest(req, res);
    } catch (err) {
      log(`HTTP error: ${err.message}`);
      if (!res.headersSent) res.writeHead(500).end(JSON.stringify({ jsonrpc: '2.0', error: { code: -32603, message: 'Internal server error' }, id: null }));
    }
  });
  await new Promise((resolve, reject) => http.once('error', reject).listen(port, host, resolve));
  log(`MCP server on http://${host}:${http.address().port}/mcp`);
  return http;
}

export async function startServer({ transport = 'stdio', port = 3100, host = '127.0.0.1', projectRoot } = {}) {
  const roots = await resolveRoots(projectRoot);
  if (!roots.installed) log(`No MDAN install in ${roots.projectRoot} — serving bundled content (run \`mdan install\` to customize).`);

  if (transport === 'http') return startHttp(roots, { port, host });

  const server = await createMcpServer(roots);
  await server.connect(new StdioServerTransport());
  log(`MCP server v${VERSION} running on stdio (project: ${roots.projectRoot})`);
  return server;
}
