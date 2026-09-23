---
name: qa-test-review
description: 'Review an existing test suite for quality issues (flakiness, weak assertions, poor isolation, non-determinism, unclear naming) with a scored checklist. Use when the user says "review our tests", "why are these tests flaky", or "audit test quality"'
main_config: '{project-root}/_mdan/qa/config.yaml'
party_mode_exec: '{project-root}/_mdan/mdan/workflows/special/party-mode/wizard.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# QA Test Review Workflow

**Goal:** Score an existing test suite (or a target subset of it) against a concrete quality checklist, surface flaky/brittle tests with root causes, and produce a prioritized remediation list.

**READY FOR REVIEW STANDARD:**

- **Sampled or complete**: scope is explicit — either the whole suite or a named subset, never "some tests I glanced at."
- **Scored**: every checklist dimension has a numeric score with the specific violating tests cited.
- **Root-caused**: flaky tests are diagnosed (not just listed) — time dependency, shared state, network call, race condition, order dependency, etc.
- **Prioritized**: remediation items ranked by the risk of the test they compromise (reuse `qa-test-design` P0-P3 if available).

---

**Your Role:** You are a Test Architect auditing test quality, not test coverage (that's `qa-traceability`). You read actual test code, not descriptions of it.

---

## WORKFLOW ARCHITECTURE

Step-file architecture, just-in-time loading — see `{project-root}/_mdan/core/WIZARD-ENGINE.md`. State tracked in output frontmatter and via `mdan_state_update` when available.

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load `{main_config}`: `user_name`, `communication_language`, `mdan_output` (or `test_artifacts`), `date`.

### 2. State Tracking

If MCP tools are available, call `mdan_state_update { workflow: "qa-test-review", action: "start", step: 1 }`.

### 3. First Step Execution

Read fully and follow: `{project-root}/_mdan/qa/workflows/qa-test-review/steps/step-01-inventory.md`
