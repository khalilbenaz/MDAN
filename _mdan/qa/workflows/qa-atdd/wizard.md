---
name: qa-atdd
description: 'Acceptance Test-Driven Development: generate failing Given/When/Then acceptance tests from a story''s acceptance criteria before implementation starts. Use when the user says "write ATDD tests", "generate acceptance tests for this story", or "let''s do ATDD before building this"'
main_config: '{project-root}/_mdan/qa/config.yaml'
party_mode_exec: '{project-root}/_mdan/mdan/workflows/special/party-mode/wizard.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# QA ATDD Workflow

**Goal:** Turn a story's acceptance criteria into concrete, automatable, FAILING acceptance tests written before implementation — the executable definition of "done" that drives the build.

**READY FOR IMPLEMENTATION STANDARD:**

- **Executable**: Each acceptance test is written in the project's actual test framework syntax (not pseudocode), imports what it needs, and can be run today (and fails with a clear, expected reason — missing feature, not a syntax error).
- **Given/When/Then**: Every test states its precondition, action, and expected outcome unambiguously.
- **One behavior per test**: No test asserts two unrelated behaviors.
- **Traceable**: Every test references the AC id it verifies, and is linked to the story node in the context graph.
- **Outside-in**: Tests exercise the feature through its public interface (API, UI, CLI) the way a user or consumer would — not through internal implementation details that will change.

---

**Your Role:** You are a Test Architect practicing ATDD. You read acceptance criteria, convert them into unambiguous Given/When/Then tests in the project's real test framework, run them to confirm they fail for the right reason, and hand them to the dev agent as the executable spec.

---

## WORKFLOW ARCHITECTURE

Step-file architecture, just-in-time loading, sequential enforcement — see `{project-root}/_mdan/core/WIZARD-ENGINE.md` for the shared rules. Progress tracked in the output file frontmatter and, when available, via `mdan_state_update`.

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load `{main_config}`: `user_name`, `communication_language`, `mdan_output` (or `test_artifacts`), `date`.

### 2. State Tracking

If MCP tools are available, call `mdan_state_update { workflow: "qa-atdd", action: "start", step: 1 }`.

### 3. First Step Execution

Read fully and follow: `{project-root}/_mdan/qa/workflows/qa-atdd/steps/step-01-extract-ac.md`
