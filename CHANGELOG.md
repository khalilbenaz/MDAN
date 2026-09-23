# Changelog

## [Unreleased]

### Added
- Project state for real: `mdan_state_update` (start / step / complete), `mdan_status` and `mdan status` with the recommended next step; interrupted wizards are offered a resume point by `mdan_run_workflow`; completed artifacts are registered in the context graph; decision records are recorded in the state.
- Agent memory sidecars (schema of the party-mode protocol): `mdan_memory_remember` / `recall` / `forget` / `end_session` / `list`, reinforcement of identical memories, decay after 5 idle sessions, relationships and decision history; memories are injected when an agent is consulted or joins party mode; `mdan memory` CLI.

- Quality gates: `mdan check` / `mdan_check` — unfilled placeholders, TODO/TBD, empty and missing sections, measurable NFRs, FR coverage by stories, NFR coverage by the architecture, acceptance criteria; PASS / CONCERNS / FAIL with strictness from the project scale (`project_scale`: auto | solo | team | enterprise, `--scale` at install). Planning wizards run it before completing.
- Traceability: `mdan trace` / `mdan_trace` — requirement → story → test matrix from the PRD, epics and test files, coverage thresholds per scale, optional write into the context graph (`mdan impact FR3` then lists stories and tests).
- Scale-adaptive routing: `mdan scope` / `mdan_estimate_scope` — oneshot / spec / full from risk terms, file count and the real downstream impact in the context graph; quick-dev uses it, code-review now re-validates downstream artifacts and stale items.

- Layered agent customization (shipped < team `_mdan/custom/<agent>.yaml` < personal `<agent>.user.yaml`, git-ignored), merged when the agent is loaded; `mdan_customize_agent`; reinstalls never touch `_mdan/custom/`.
- HTTP transport security: `--token` / `MDAN_HTTP_TOKEN` bearer auth (constant-time), refusal to bind a non-loopback address without a token unless `--insecure`.
- MCP resources `mdan://workflow/{name}`, `mdan://agent/{name}` (listable) and `mdan://health` (progress, quality gate, stale artifacts, memories in one call).
- `mdan graph --since <node>` highlights a decision and everything downstream of it (Mermaid and HTML).
- `mdan update --channel latest|next|<version>` delegates to another published installer.
- Dependabot for npm (MCP SDK + zod grouped) and GitHub Actions.

- Core team: 8 real agents in `_mdan/core/agents/` — Amina (analyst), Khadija (PM), Reda (architect), Haytame (dev), Jihane (UX), Nadia (scrum master), Youssef (tech writer), Yassir (security); the party team now lists only real agents.
- Workflows `correct-course` (mid-sprint change with graph impact analysis → Sprint Change Proposal) and `retrospective` (lessons stored as agent memories).
- Module `qa` (Test Architect, Fatima): test design P0-P3, ATDD, traceability, NFR assessment, test review, CI gates, release gate — every artifact linked in the context graph.
- Module `payments-ma` (Houda, Anas, Samira): KYC tiers and ceilings, money-movement flows, ISO 8583 spec, EOD reconciliation, BAM/AML/CNDP/PCI compliance review, RIB/IBAN and ISO 8583 references.
- `mdan validate` also checks every `path` column of the content CSVs; tests guard unique persona names, real party members and BMAD leftovers.
- `mdan export --to csv|github|ado|jira` / `mdan_export_backlog`: epics and stories to CSV, GitHub Issues (with "Part of #N"), Azure DevOps (Epic / User Story with parent links) or Jira (ADF, parent keys); dry run by default, idempotent re-runs update instead of duplicating.
- Web bundles: `mdan bundle [agent…] [--all]` builds `<agent>.instructions.md` (fits the ~8k GPT limit) + `<agent>.knowledge.md` (persona, rules and every workflow the agent's menu references) for ChatGPT GPTs, Gemini Gems and Claude Projects.
- Wizard evaluation harness `npm run eval` (tools/eval): an LLM runs a wizard end to end against a scripted user persona, the document goes through `mdan check` and expected-content assertions; three scenarios included.

### Fixed
- BMAD leftovers: party team and help tables referenced agents and `bmm` files that do not exist; duplicate persona names across modules renamed; hardcoded French-Darija mandates removed from ecosystem agents.
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
