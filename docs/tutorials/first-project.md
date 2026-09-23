# Tutorial: your first project

This walks a new project through MDAN end to end: install, brief, PRD, architecture, epics, sprint, one story implemented and reviewed — checking status and quality along the way. Roughly 30-45 minutes if you answer the wizards yourself; MDAN does not write the answers for you, it structures the conversation and the deliverables.

Everything here works identically through IDE slash commands (Claude Code, Cursor, …) or through the MCP tools (`mdan_run_workflow`, `mdan_status`, …) from an MCP client. The examples use slash commands; the [MCP clients guide](../how-to/use-with-mcp-clients.md) covers the tool-call equivalents.

## 1. Install

```bash
mkdir my-app && cd my-app
npx mdan-method install
```

Answer the prompts (language, optional packs, IDE, your name). For a non-interactive install:

```bash
npx mdan-method install --yes --lang en --ide claude-code
```

This creates `_mdan/` (content, config, state) and `.claude/commands/mdan-*.md` (or the equivalent for your IDE). Open your IDE in this folder and type `/mdan-` to see every available command.

## 2. Check where you stand

```bash
mdan status
```

On a fresh install this reports no workflow completed yet, and recommends starting with `create-product-brief`. Re-run this anytime — it is the fastest way to know what MDAN thinks the next step is.

## 3. Product brief

```
/mdan-create-product-brief
```

A 6-step conversation: vision, target users, scope, success metrics. The agent asks, you answer; the wizard tracks progress via `mdan_state_update` (or writes directly to `_mdan/state/MDAN-STATE.json` without MCP) so if you close the session mid-way, `/mdan-create-product-brief` again resumes at the interrupted step instead of restarting.

The brief is saved under `mdan_output/planning-artifacts/` and registered as a node in the context graph.

## 4. PRD

```
/mdan-create-prd
```

12 steps, using the brief as input: vision, user journeys, scoping, functional (FR) and non-functional (NFR) requirements. Before the wizard marks the PRD complete, it runs the quality gate on it — unfilled placeholders, empty sections, requirements without a measurable NFR, etc. You can also run it yourself at any point:

```bash
mdan check mdan_output/planning-artifacts/prd.md
```

`PASS` / `CONCERNS` / `FAIL`, with strictness following the project scale (`auto` by default — see [concepts](../explanation/concepts.md#scale-adaptive-routing)).

## 5. Architecture

```
/mdan-create-architecture
```

8 steps: context, decisions, patterns, structure, validation — reading the PRD's FRs/NFRs as input. Architectural decisions worth debating (e.g. "REST vs GraphQL", "monolith vs microservices") are good candidates for `/mdan-debate` first; the resulting decision record (`DR-001`, …) gets an `impacts` edge to the architecture node, so `mdan graph --since DR-001` later shows exactly what that decision touched.

## 6. Epics and stories

```
/mdan-create-epics-and-stories
```

Breaks the PRD's requirements into epics and development-ready user stories. Run the traceability check to confirm every FR/NFR maps to at least one story:

```bash
mdan trace
```

## 7. Sprint plan

```
/mdan-sprint-planning
```

Builds a sprint plan from the epics with estimation.

## 8. Implement a story

```
/mdan-dev-story
```

Give it the story file; the agent implements with TDD (tests first), documents as it goes. For a small change that doesn't need this ceremony, `mdan scope "<description>"` tells you whether `quick-dev` (oneshot), `quick-spec` (spec first) or full planning is warranted, based on the real downstream impact in the context graph — not just a guess from the wording.

## 9. Code review

```
/mdan-code-review
```

Adversarial review: bugs, security, pattern violations — and, because the story is in the context graph, a check of what else depends on the changed artifact (`mdan_graph_stale` under the hood) so nothing downstream is silently left unreviewed.

## Checking in along the way

```bash
mdan status              # current workflow/step, completed phases, next recommended step
mdan check               # quality gate on the registered artifacts
mdan trace                # requirement -> story -> test coverage
mdan graph                # Mermaid diagram of everything produced so far
mdan graph --since DR-001 # highlight a decision and everything downstream of it
```

## What's next

- A mid-sprint scope change: `/mdan-correct-course` (impact analysis first, then a Sprint Change Proposal).
- End of a sprint or epic: `/mdan-retrospective` — lessons become agent memories, so the same mistake gets flagged next time.
- Shipping: `/mdan-document-project` for project docs, `mdan export --to github` (or `ado`/`jira`/`csv`) to push the backlog to your tracker.
- Wire `mdan check` and `mdan trace` into CI: see [Quality gates in CI](../how-to/quality-gates-in-ci.md).
