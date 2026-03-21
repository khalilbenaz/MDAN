# MDAN MCP Server

## Overview

MDAN exposes its workflows, agents, and state as MCP (Model Context Protocol) tools and resources. This allows any MCP-compatible client (Claude Code, Claude Desktop, etc.) to interact with MDAN programmatically.

## Quick Start

### 1. Install dependencies

```bash
cd your-project
npm install
```

### 2. Configure MCP client

Add to your `.mcp.json` (Claude Code) or `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mdan": {
      "command": "node",
      "args": ["path/to/tools/mcp/server.js"],
      "env": {
        "MDAN_PROJECT_ROOT": "/path/to/your/project"
      }
    }
  }
}
```

### 3. Or run via CLI

```bash
mdan serve          # stdio transport (default)
mdan serve --sse    # SSE transport for remote
```

## Available Tools

### Workflow Tools
- `mdan/list-workflows` — List all available MDAN workflows
- `mdan/workflow/{name}` — Execute a specific workflow (e.g., `mdan/workflow/create-prd`)

### Agent Tools
- `mdan/list-agents` — List all installed agents with capabilities
- `mdan/agent/{name}` — Consult a specific agent (e.g., `mdan/agent/mdan-master`)

### Context Graph Tools
- `mdan/graph/add-node` — Add an artifact node to the context graph
- `mdan/graph/add-edge` — Add a relationship edge between nodes
- `mdan/graph/impact` — Analyze downstream impact of an artifact
- `mdan/graph/visualize` — Generate Mermaid diagram of the graph

### Orchestration Tools
- `mdan/orchestrate/party-mode` — Start multi-agent session (discussion/debate/consensus)
- `mdan/orchestrate/create-decision-record` — Create a decision record from a session

## Available Resources

- `mdan://state` — Current MDAN-STATE.json
- `mdan://config` — Module configs and manifest
- `mdan://graph` — Context graph (DAG of artifacts and relationships)

## Architecture

```
tools/mcp/
├── server.js              # Core server (SDK init, JSON-RPC lifecycle)
├── discovery.js           # Scans _mdan/ for modules/workflows/agents
├── tools/
│   ├── workflow-tools.js  # Workflows → MCP tools
│   ├── agent-tools.js     # Agents → MCP tools
│   ├── graph-tools.js     # Context graph → MCP tools
│   └── orchestration-tools.js  # Multi-agent → MCP tools
└── resources/
    ├── state-resource.js  # MDAN-STATE → MCP resource
    ├── config-resource.js # Config/manifest → MCP resource
    └── graph-resource.js  # Context graph → MCP resource
```
