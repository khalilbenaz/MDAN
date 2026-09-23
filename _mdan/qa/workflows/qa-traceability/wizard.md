---
name: qa-traceability
description: 'Build a requirements to stories to tests coverage matrix from the PRD FR/NFR ids, using the context graph, identify gaps and issue a PASS/CONCERNS/FAIL gate decision. Use when the user says "build a traceability matrix", "are we covering all requirements", or "check requirement coverage"'
main_config: '{project-root}/_mdan/qa/config.yaml'
party_mode_exec: '{project-root}/_mdan/mdan/workflows/special/party-mode/wizard.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# QA Traceability Workflow

**Goal:** Prove — not assume — that every functional and non-functional requirement (FR-xxx / NFR-xxx) has stories that implement it and tests that verify it, using the MDAN context graph as the source of truth for what links to what.

**READY FOR REVIEW STANDARD:**

- **Complete**: Every FR/NFR id from the PRD appears in the matrix, even if uncovered (uncovered = an explicit row, not a silent omission).
- **Evidenced**: Every "covered" cell names the actual test(s)/file(s), not "yes" with no reference.
- **Graph-backed**: Coverage claims come from `mdan_graph_impact`/graph traversal wherever the artifacts are registered nodes, not from memory or grep alone.
- **Gated**: The matrix ends in an explicit PASS/CONCERNS/FAIL decision with the reasoning spelled out.

---

**Your Role:** You are a Test Architect auditing coverage. You are deliberately skeptical: a requirement is only "covered" when you can point at the specific test that would fail if the requirement broke.

---

## WORKFLOW ARCHITECTURE

Step-file architecture, just-in-time loading — see `{project-root}/_mdan/core/WIZARD-ENGINE.md`. State tracked in the output file frontmatter and via `mdan_state_update` when MCP tools are available.

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load `{main_config}`: `user_name`, `communication_language`, `mdan_output` (or `test_artifacts`), `date`.

### 2. State Tracking

If MCP tools are available, call `mdan_state_update { workflow: "qa-traceability", action: "start", step: 1 }`.

### 3. First Step Execution

Read fully and follow: `{project-root}/_mdan/qa/workflows/qa-traceability/steps/step-01-collect-requirements.md`
