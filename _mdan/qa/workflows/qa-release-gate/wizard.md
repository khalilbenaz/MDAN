---
name: qa-release-gate
description: 'Go/no-go release decision aggregating test design, traceability, NFR assessment and open defects by priority, using mdan_graph_stale to block release if artifacts downstream of changed specs were not re-verified. Use when the user says "are we ready to ship", "run the release gate", or "go/no-go decision"'
main_config: '{project-root}/_mdan/qa/config.yaml'
party_mode_exec: '{project-root}/_mdan/mdan/workflows/special/party-mode/wizard.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# QA Release Gate Workflow

**Goal:** Aggregate every QA artifact for this release (test design, traceability matrix, NFR assessment, open defects) plus the context graph's staleness report into one explicit PASS/CONCERNS/FAIL go/no-go decision — MDAN's differentiator over ad-hoc "I think we're ready": the graph tells you what changed since it was last verified.

**READY FOR REVIEW STANDARD:**

- **Aggregated, not re-derived**: this workflow pulls existing artifact verdicts (test-design priorities, traceability gate, NFR verdict), it does not redo their analysis.
- **Staleness-checked**: `mdan_graph_stale` is consulted; any artifact downstream of a changed spec that was not re-verified blocks the release until re-verified or explicitly waived.
- **Defect-aware**: open defects are weighed by severity against what they block.
- **Recorded**: the decision is written as a Decision Record, ideally via `mdan_create_decision_record`, so it is itself a graph node other artifacts can reference later.

---

**Your Role:** You are a Test Architect running the release gate. You are the last line before ship — you say what you can defend with evidence, and nothing else.

---

## WORKFLOW ARCHITECTURE

Step-file architecture, just-in-time loading — see `{project-root}/_mdan/core/WIZARD-ENGINE.md`. State tracked in output frontmatter and via `mdan_state_update` when available.

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load `{main_config}`: `user_name`, `communication_language`, `mdan_output` (or `test_artifacts`), `date`.

### 2. State Tracking

If MCP tools are available, call `mdan_state_update { workflow: "qa-release-gate", action: "start", step: 1 }`.

### 3. First Step Execution

Read fully and follow: `{project-root}/_mdan/qa/workflows/qa-release-gate/steps/step-01-aggregate.md`
