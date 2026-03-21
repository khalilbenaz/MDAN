#!/usr/bin/env node
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { discoverMdan } from './discovery.js';
import { registerWorkflowTools } from './tools/workflow-tools.js';
import { registerAgentTools } from './tools/agent-tools.js';
import { registerGraphTools } from './tools/graph-tools.js';
import { registerOrchestrationTools } from './tools/orchestration-tools.js';
import { registerStateResource } from './resources/state-resource.js';
import { registerConfigResource } from './resources/config-resource.js';
import { registerGraphResource } from './resources/graph-resource.js';

export async function startServer({ transport = 'stdio', port = 3100 } = {}) {
  const projectRoot = process.env.MDAN_PROJECT_ROOT || process.cwd();

  const server = new McpServer({ name: 'mdan', version: '3.0.0' });

  // Discover installed modules, workflows, agents
  const discovery = await discoverMdan(projectRoot);

  // Register tools
  registerWorkflowTools(server, discovery, projectRoot);
  registerAgentTools(server, discovery, projectRoot);
  registerGraphTools(server, projectRoot);
  registerOrchestrationTools(server, projectRoot);

  // Register resources
  registerStateResource(server, projectRoot);
  registerConfigResource(server, discovery, projectRoot);
  registerGraphResource(server, projectRoot);

  // Start transport
  if (transport === 'stdio') {
    const stdioTransport = new StdioServerTransport();
    await server.connect(stdioTransport);
    console.error('[mdan] MCP server running on stdio');
  }

  return server;
}

// Direct execution
if (process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, '/'))) {
  startServer().catch(err => {
    console.error('[mdan] Fatal:', err);
    process.exit(1);
  });
}
