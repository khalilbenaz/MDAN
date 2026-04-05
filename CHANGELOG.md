# Changelog

## [3.1.1] - 2026-04-05

### Added
- **Ultra-concise communication rules** enforced across all 149 components (agents, wizards, skills, tasks)
- `ultra-concise-mode` behavior skill in `_mdan/core/`
- Communication Rules section in README (in French)

### Changed
- All agent/skill/task markdown files now include mandatory communication rules: tool-first, result-first, no filler, no politeness wrappers, minimum words

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
