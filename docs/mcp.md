# MDAN MCP Server

## Overview

MDAN exposes its workflows, agents, context graph and decision records as MCP (Model Context Protocol) tools, prompts and resources, usable from any MCP client (Claude Code, Claude Desktop, Cursor, …).

## Quick Start

```json
{
  "mcpServers": {
    "mdan": {
      "command": "npx",
      "args": ["-y", "mdan-method", "serve"],
      "env": { "MDAN_PROJECT_ROOT": "/path/to/your/project" }
    }
  }
}
```

`mdan install --mcp` writes this entry into the project's `.mcp.json` for you.

```bash
mdan serve                              # stdio (default)
mdan serve --http --port 3100           # Streamable HTTP: POST /mcp, GET /health
docker run -i --rm -v "$PWD:/workspace" mdan-mcp
```

- `MDAN_PROJECT_ROOT` (default: current directory) is where the context graph and decision records are written.
- If the project has no MDAN install (`_mdan/_config/workflow-manifest.csv`), the content bundled in the package is served read-only.
- `MDAN_CLAUDE_DIR` overrides `~/.claude` for the ecosystem tools.
- The HTTP transport is stateless and binds `127.0.0.1` by default (`--host 0.0.0.0` to expose it; put it behind authentication if you do).

## Tools

| Tool | Input | Description |
|------|-------|-------------|
| `mdan_list_workflows` | — | Installed workflows |
| `mdan_run_workflow` | `name` (enum), `topic?` | Returns the rules, the wizard (or workflow engine + YAML config) to execute |
| `mdan_list_agents` | — | Installed agents |
| `mdan_consult_agent` | `name` (enum), `question?` | Agent persona + project customization |
| `mdan_party_mode` | `mode` (`discussion`/`debate`/`consensus`), `topic?`, `agents?[]` | Multi-agent session protocol |
| `mdan_create_decision_record` | `topic`, `decision`, `rationale`, `confidence?`, `participants?`, `rounds?`, `dissent?`, `impacts?[]`, `id?` | Writes `mdan_output/decisions/DR-XXX.json` and registers it in the graph |
| `mdan_graph_add_node` | `id`, `type?`, `path?`, `workflow?`, `agent?` | Adds/updates an artifact, records the file hash |
| `mdan_graph_add_edge` | `source`, `target`, `relation?` | `input_to` / `derived_from` / `impacts` / `references`; cycles rejected |
| `mdan_graph_impact` | `nodeId` | Upstream and downstream artifacts |
| `mdan_graph_stale` | — | Artifacts changed since registration + downstream to review |
| `mdan_graph_visualize` | — | Mermaid diagram |
| `mdan_ecosystem_search` | `kind` (`skill`/`agent`/`command`), `query`, `limit?` | Ranked search in `~/.claude` |
| `mdan_ecosystem_read` | `kind`, `name` | Full content of a component |
| `mdan_ecosystem_catalog` | `offset?`, `length?` | Paginated ecosystem catalog |
| `mdan_ecosystem_stats` | — | Installed component counts |

Errors (unknown name, invalid id, path outside the allowed directory, …) are returned as MCP tool errors (`isError: true`).

## Prompts

Every workflow is a prompt named after it (`create-prd`, `create-architecture`, …) with an optional `topic` argument; every agent is a prompt `agent-<name>` with an optional `question`.

## Resources

- `mdan://state` — `_mdan/state/MDAN-STATE.json`
- `mdan://config` — installed modules, their `config.yaml`, counts
- `mdan://graph` — context graph JSON

## Architecture

```
tools/mcp/
├── bin.js                     # mdan-mcp binary (= mdan serve)
├── server.js                  # createMcpServer(), stdio / Streamable HTTP transports
├── discovery.js               # reads the installed manifests (_mdan/_config/*.csv)
├── resources.js               # mdan://state, mdan://config, mdan://graph
├── util.js                    # error wrapping, enum schemas
└── tools/
    ├── workflow-tools.js      # workflows → tools + prompts
    ├── agent-tools.js         # agents → tools + prompts
    ├── graph-tools.js         # context graph
    ├── orchestration-tools.js # party mode, decision records
    └── ecosystem-tools.js     # ~/.claude skills/agents/commands
```

## Migrating from v3

| v3 | v4 |
|----|----|
| `mdan_workflow_create-prd { topic }` | `mdan_run_workflow { name: "create-prd", topic }` |
| `mdan_agent_risk-manager { question }` | `mdan_consult_agent { name: "risk-manager", question }` |
| `mdan_list-workflows`, `mdan_graph_add-node`, … | `mdan_list_workflows`, `mdan_graph_add_node`, … |
| `mdan_orchestrate_party-mode` | `mdan_party_mode` (`agents` is now an array) |
| `mdan_orchestrate_create-decision-record` | `mdan_create_decision_record` (`participants`/`rounds` are JSON values, not strings) |
| `mdan_ecosystem_search-skills/-agents/-commands` | `mdan_ecosystem_search { kind }` |
| `mdan_ecosystem_read-skill/-agent` | `mdan_ecosystem_read { kind, name }` |
| `mdan serve --sse` | `mdan serve --http` |
