# Changelog

## [Unreleased]

### Added
- Project state for real: `mdan_state_update` (start / step / complete), `mdan_status` and `mdan status` with the recommended next step; interrupted wizards are offered a resume point by `mdan_run_workflow`; completed artifacts are registered in the context graph; decision records are recorded in the state.
- Agent memory sidecars (schema of the party-mode protocol): `mdan_memory_remember` / `recall` / `forget` / `end_session` / `list`, reinforcement of identical memories, decay after 5 idle sessions, relationships and decision history; memories are injected when an agent is consulted or joins party mode; `mdan memory` CLI.

### Fixed
- WIZARD-ENGINE still hardcoded the French-Darija rule; it now defers to `_mdan/core/rules.md`.

## [4.0.1] - 2026-09-23

### Fixed
- `npx mdan-method install` / `npx mdan-method serve` failed with "could not determine executable to run" (no bin named after the package). Added the `mdan-method` bin.

## [4.0.0] - 2026-09-23

### Breaking
- MCP tools regrouped: `mdan_workflow_<name>` → `mdan_run_workflow { name, topic }`, `mdan_agent_<name>` → `mdan_consult_agent { name, question }`; all tool names now use `_` (`mdan_list_workflows`, `mdan_graph_add_node`, `mdan_party_mode`, `mdan_create_decision_record`, `mdan_ecosystem_search`/`read`/`catalog`/`stats`).
- `mdan serve --sse` replaced by `--http` (Streamable HTTP on `/mcp`); `--sse` kept as a deprecated alias.
- Node.js >= 20.

### Fixed
- MCP server crashed at startup with SDK 1.29 (`expected a Zod schema or ToolAnnotations`): every tool now has a real Zod input schema, and arguments actually reach the handlers.
- `npx mdan-method install` did not exist: new interactive / non-interactive installer.
- `mdan-mcp` binary never started the server when launched through the npm bin shim.
- `@modelcontextprotocol/sdk` moved back to `dependencies` (+ `zod`); server version read from `package.json`.
- 298 broken file references in the content (`_.mdan/…`, old `steps-c/` and `2-plan-workflows/` layout, missing `advanced-elicitation`) — `mdan validate` and CI now enforce 0.
- Path traversal in `create-decision-record` (`id`), `ecosystem read-skill/read-agent` and graph node paths.
- Unguarded `JSON.parse`, missing-argument crashes: tool errors are returned as MCP errors instead of killing the call.
- Decision records were never registered in the context graph (`registered_in_graph: false`).
- Context graph writes are atomic and locked (no lost updates on concurrent calls); downstream traversal deduplicated.
- CSV parser handles quoted multi-line fields and CRLF.
- README advertised 10 core agents that do not exist; agent tables and counts are now generated.

### Added
- `mdan install` / `mdan update`: language, optional packs, IDEs (Claude Code, Cursor, OpenCode, Gemini CLI, Qwen Code), user name, optional `.mcp.json`; hash-tracked files so updates never overwrite your changes (`.mdan-new`), managed config keys only.
- MCP prompts for every workflow and agent; `mdan_graph_stale`; decision records with sequential ids and `impacts` edges; ranked ecosystem search on frontmatter; paginated catalog.
- Context graph: cycle detection, relation/type validation, file hashes and staleness (`mdan stale`, `--touch`), `mdan graph --html`.
- Serves the bundled content when the project has no install (Glama, plain `npx`); `Dockerfile` and `glama.json`.
- Single source of truth: `npm run build` generates the manifests, `.claude/commands` and README sections from the content files; `--check` in CI.
- Language and communication rules centralized in `_mdan/core/rules.md` (was duplicated in ~150 files).
- Tests (`node --test`: graph, CSV, paths, build, installer, MCP over stdio and HTTP), ESLint, GitHub Actions CI (Linux + Windows, Node 20/22, Docker handshake) and tag-based npm release with provenance.

### Removed
- `.claude/session-state.md` from the repository; `.npmignore` (the `files` whitelist is authoritative).

## [3.1.3] - 2026-04-05

### Changed
- Moved `@modelcontextprotocol/sdk` from `dependencies` to `optionalDependencies` — zero mandatory deps, SDK loaded only when `mdan serve` is called
- MCP server now shows clear install instructions if SDK is missing

## [3.1.2] - 2026-04-05

### Added
- **Ultra-concise communication rules** enforced across all 149 components (agents, wizards, skills, tasks)
- `ultra-concise-mode` behavior skill in `_mdan/core/`
- Communication Rules section in README (in French)
- `LICENSE` file (MIT)
- `.npmignore` for clean npm publishes
- `files` field in package.json for explicit publish control
- `repository`, `homepage`, `bugs`, `author`, `keywords` metadata

### Changed
- All agent/skill/task markdown files now include mandatory communication rules
- Pinned `@modelcontextprotocol/sdk` to exact `1.29.0` (was `^1.12.1`)
- Fixed bin script paths (removed `./` prefix)
- Made bin scripts executable

## [3.0.1] - 2026-03-22

### Added
- **Standalone Debate Workflow** (`/mdan-debate`): Direct access to structured multi-agent debate without going through party-mode. Full 4-step workflow (topic setup → 3 rounds + arbitration → decision record → conclusion). Produces Decision Records (DR-XXX) and registers in Context Graph.
- `mdan-debate.md` slash command for Claude Code

### Fixed
- **All slash command paths**: Fixed double `_mdan/_mdan/mdan` path in all workflow commands — was causing commands to fail to locate workflow files
- **Agent command paths**: Fixed absolute local paths (`/Users/.../claude_mdan/_mdan/...`) leaked into agent commands — replaced with correct relative `{project-root}/_mdan/...` paths
- Added debate entry to `workflow-manifest.csv`
- Updated README badges and command table

## [3.0.0] - 2026-03-21

### Added

#### MCP Server
- Native Node.js MCP server with stdio transport (`mdan serve`)
- Dynamic tool registration from installed workflows and agents
- `mdan/list-workflows`, `mdan/workflow/{name}` tools
- `mdan/list-agents`, `mdan/agent/{name}` tools
- `mdan/graph/*` tools (add-node, add-edge, impact, visualize)
- `mdan/orchestrate/party-mode` and `mdan/orchestrate/create-decision-record` tools
- MCP resources: `mdan://state`, `mdan://config`, `mdan://graph`
- CLI entry point with `mdan` and `mdan-mcp` bin commands

#### Context Graph
- DAG-based context graph (`_mdan/state/context-graph.json`)
- `ContextGraph` library: addNode, addEdge, getDownstream, getUpstream, toMermaid
- `mdan impact <artifact>` CLI command for downstream impact analysis
- `mdan graph` CLI command for Mermaid/JSON visualization
- Auto-registration of workflow artifacts in the graph at completion
- MDAN-STATE template with graph path, sessions, sidecars, decisions

#### Multi-Agent Orchestration
- **Debate Mode**: 3-role structured argumentation (proponent, opponent, arbitrator)
- **Consensus Mode**: N-agent convergence through 4 phases (positions, mapping, convergence, synthesis)
- Decision Records (DR-XXX) with JSON schema and sequential IDs
- Agent Sidecars: persistent memory across Party Mode sessions
- Turn Protocol: structured speaking turns with word limits and ordering rules
- Memory Protocol: memory lifecycle with confidence scoring and decay
- Mode selection at Party Mode start: [D]iscussion, [B]Debate, [C]onsensus
- Mid-session mode switching from post-round menu
- Context Graph registration of Decision Records
- Memory persistence on graceful exit

### Changed
- Party Mode wizard updated with 3 orchestration modes
- Step 01 (agent loading) now loads sidecars and presents mode selection
- Step 02 (discussion) enhanced with turn protocol and mode switching
- Step 03 (graceful exit) now persists agent memory and registers decisions in graph
- `workflow.xml` auto-registers artifacts in context graph at completion
- WIZARD-ENGINE.md documents context graph, sidecars, and multi-mode orchestration
- All agent customize files now include `hasSidecar: true`
