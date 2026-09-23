# Reference: MCP server

MDAN exposes its workflows, agents, context graph, memory, quality gates and decision records as MCP (Model Context Protocol) tools, prompts and resources, usable from any MCP client (Claude Code, Claude Desktop, Cursor, …). See [How to: use MDAN with MCP clients](../how-to/use-with-mcp-clients.md) for setup.

## Quick start

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

```bash
mdan serve                              # stdio (default)
mdan serve --http --port 3100           # Streamable HTTP: POST /mcp, GET /health
docker run -i --rm -v "$PWD:/workspace" mdan-mcp
```

- `MDAN_PROJECT_ROOT` (default: current directory) is where the context graph and decision records are written.
- If the project has no MDAN install (`_mdan/_config/workflow-manifest.csv`), the content bundled in the package is served read-only.
- `MDAN_CLAUDE_DIR` overrides `~/.claude` for the ecosystem tools.
- The HTTP transport is stateless and binds `127.0.0.1` by default. `--token` / `MDAN_HTTP_TOKEN` requires `Authorization: Bearer <token>`; binding a non-loopback address without a token is refused unless `--insecure` is passed.

## Tools

### Status and state

| Tool | Input | Description |
|------|-------|-------------|
| `mdan_status` | — | Current workflow and step, completed workflows per phase, artifacts, decisions, recommended next step. Includes stale artifacts. |
| `mdan_state_update` | `action` (`start`\|`step`\|`complete`), `workflow`, `step?`, `stepFile?`, `artifacts?[{id, path, inputs?}]`, `summary?` | Starts/resumes, advances, or completes a workflow. On `complete`, artifacts are registered as context-graph nodes (with `input_to` edges from `inputs`) and the response includes the recommended next workflow. |

### Workflows

| Tool | Input | Description |
|------|-------|-------------|
| `mdan_list_workflows` | — | Installed workflows (name, description, module, path). |
| `mdan_run_workflow` | `name` (enum), `topic?` | Returns the mandatory rules (`_mdan/core/rules.md`), a progress section (resume point / existing artifacts / how to call `mdan_state_update`), and the wizard (or workflow engine + YAML config) to execute step by step. |

### Agents

| Tool | Input | Description |
|------|-------|-------------|
| `mdan_list_agents` | — | Installed agents (name, displayName, title, icon, role, module). |
| `mdan_consult_agent` | `name` (enum), `question?` | Loads an agent persona with its layered customization and a memory briefing, to answer in character. |
| `mdan_customize_agent` | `agent` (enum), `layer` (`team`\|`user`, default `team`), `displayName?`, `communication_style?`, `principles?[]`, `critical_actions?[]`, `memories?[]`, `menu?[{trigger, description, exec?, workflow?}]` | Writes/merges a customization layer. See [Customize an agent](../how-to/customize-agents.md). |

### Party mode and decisions

| Tool | Input | Description |
|------|-------|-------------|
| `mdan_party_mode` | `mode` (`discussion`\|`debate`\|`consensus`, default `discussion`), `topic?`, `agents?[]` | Returns the party-mode protocol plus the mode-specific step (debate/consensus) and a memory briefing per named agent. Default agents: all installed. |
| `mdan_create_decision_record` | `id?`, `topic`, `mode` (`debate`\|`consensus`, default `debate`), `decision`, `rationale`, `confidence?` (0-1, default 0.5), `participants?` (object), `rounds?[]`, `dissent?`, `impacts?[]` | Writes `mdan_output/decisions/DR-XXX.json` (sequential id if not given), registers it as a `decision` node in the context graph with `impacts` edges to the given node ids, and records it in project state. |

### Memory (agent sidecars)

| Tool | Input | Description |
|------|-------|-------------|
| `mdan_memory_remember` | `agent`, `content` (≤500 chars), `type?` (default `observation`), `confidence?` (0-1, default 0.6), `tags?[]` | Stores a memory; an identical one is reinforced (confidence boosted) instead of duplicated. |
| `mdan_memory_recall` | `agent`, `query?`, `type?`, `limit?` (default 10, max 50) | Returns memories (highest confidence first), sessions participated, relationships, decision history. |
| `mdan_memory_forget` | `agent`, `id` | Deletes one memory. |
| `mdan_memory_end_session` | `agents[{name, agrees_with?, disagrees_with?, complements?, decisions?[{dr_id, role, position, outcome}]}]` (min 1) | Closes a session: counts it, applies decay, records relationships and decision outcomes (`won`/`lost`/`compromised`) for each agent. |
| `mdan_memory_list` | — | Agents that have a memory sidecar. |

Memory types (`MEMORY_TYPES`, used by `type` above): see `mdan_memory_recall`'s enum at runtime (`observation`, `preference`, `project_context`, `decision`, …) — confidence guidance: 1.0 explicit decision/fact, 0.8 unchallenged argument, 0.6 observation, 0.5 inference. Memories decay after 5 idle sessions.

### Context graph

| Tool | Input | Description |
|------|-------|-------------|
| `mdan_graph_add_node` | `id`, `type?` (default `artifact`), `path?`, `workflow?`, `agent?` | Adds/updates an artifact node, recording the file's hash (used by `mdan_graph_stale`). |
| `mdan_graph_add_edge` | `source`, `target`, `relation?` (`input_to` default; also `derived_from`, `impacts`, `references`) | Adds a relation; cycles are rejected. |
| `mdan_graph_impact` | `nodeId` | Upstream dependencies and downstream impact. |
| `mdan_graph_stale` | — | Artifacts changed since registration and the downstream artifacts to review. |
| `mdan_graph_visualize` | — | Mermaid diagram of the whole graph. |

### Quality and traceability

| Tool | Input | Description |
|------|-------|-------------|
| `mdan_check` | `paths?[]` (default: state-registered artifacts, then `docs/`), `scale?` (`solo`\|`team`\|`enterprise`, default: detected) | Quality gate: placeholders, empty/missing sections, FR/NFR coverage across documents, acceptance criteria. |
| `mdan_trace` | `register?` (boolean, default `false`) | Requirement → story → test matrix, coverage, gate decision; `register: true` also writes requirement/story/test nodes and edges into the context graph. |
| `mdan_estimate_scope` | `description`, `files?[]`, `artifacts?[]` (context-graph node ids touched) | `oneshot` / `spec` / `full` recommendation, from the description, files and the real downstream impact of the named artifacts. |

### Export

| Tool | Input | Description |
|------|-------|-------------|
| `mdan_export_backlog` | `target` (`csv`\|`github`\|`ado`\|`jira`), `apply?` (default `false`), `file?`, `repo?`, `org?`, `project?`, `url?` | Exports the epics/stories document. Dry run by default (`apply: false` returns the planned requests); tokens come from environment variables. See [Export the backlog](../how-to/export-backlog.md). |

### Ecosystem (`~/.claude`)

| Tool | Input | Description |
|------|-------|-------------|
| `mdan_ecosystem_search` | `kind` (`skill`\|`agent`\|`command`), `query`, `limit?` (default 20, max 100) | Ranked search over installed Claude Code skills/agents/commands, by name/description/frontmatter match. |
| `mdan_ecosystem_read` | `kind`, `name` | Full content of a component. |
| `mdan_ecosystem_catalog` | `offset?` (default 0), `length?` (default 15000, 1000-50000) | Paginated read of the ecosystem catalog (`_mdan/ecosystem/catalog/CATALOG.md`, requires the `ecosystem` module). |
| `mdan_ecosystem_stats` | — | Installed component counts under `MDAN_CLAUDE_DIR` (default `~/.claude`). |

Errors (unknown name, invalid id, path outside the allowed directory, …) are returned as MCP tool errors (`isError: true`), not thrown exceptions that kill the connection.

## Prompts

Every workflow is a prompt named after it (`create-prd`, `create-architecture`, …) with an optional `topic` argument; every agent is a prompt `agent-<name>` with an optional `question` argument. Clients that surface MCP prompts as slash commands (e.g. Claude Code) get `/create-prd`, `/agent-architect`, etc. this way — in addition to the `/mdan-*` commands generated at install time.

## Resources

| URI | Description |
|-----|-------------|
| `mdan://state` | `_mdan/state/MDAN-STATE.json` |
| `mdan://config` | Installed modules, their `config.yaml`, agent/workflow counts |
| `mdan://graph` | Context graph JSON |
| `mdan://workflow/{name}` | Wizard / workflow definition (listable) |
| `mdan://agent/{name}` | Agent persona definition (listable) |
| `mdan://health` | One-call health report: version, current/next step, quality gate summary, graph node/edge/stale counts, agents with memory |

## Architecture

```
tools/mcp/
├── bin.js                     # mdan-mcp binary (= mdan serve)
├── server.js                  # createMcpServer(), stdio / Streamable HTTP transports
├── discovery.js                # reads the installed manifests (_mdan/_config/*.csv)
├── resources.js                # mdan://state, mdan://config, mdan://graph, mdan://health, mdan://workflow/{}, mdan://agent/{}
├── util.js                     # error wrapping, enum schemas
└── tools/
    ├── state-tools.js          # mdan_status, mdan_state_update
    ├── workflow-tools.js       # workflows → tools + prompts
    ├── agent-tools.js          # agents → tools + prompts, mdan_customize_agent
    ├── memory-tools.js         # agent memory sidecars
    ├── graph-tools.js          # context graph
    ├── orchestration-tools.js  # party mode, decision records
    ├── quality-tools.js        # mdan_check, mdan_trace, mdan_estimate_scope
    ├── export-tools.js         # mdan_export_backlog
    └── ecosystem-tools.js      # ~/.claude skills/agents/commands
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
