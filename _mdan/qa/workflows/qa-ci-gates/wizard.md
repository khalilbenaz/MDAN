---
name: qa-ci-gates
description: 'Set up a stack-agnostic CI test pipeline with quality gates (coverage, optional mutation testing, contract tests), with concrete examples for GitHub Actions and Azure DevOps. Use when the user says "set up CI for tests", "add a quality gate to the pipeline", or "configure test gates in Azure DevOps/GitHub Actions"'
main_config: '{project-root}/_mdan/qa/config.yaml'
party_mode_exec: '{project-root}/_mdan/mdan/workflows/special/party-mode/wizard.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# QA CI Gates Workflow

**Goal:** Design and generate a CI test pipeline with explicit, enforced quality gates — not just "tests run in CI" but "the build fails when quality regresses," staged for fast feedback.

**READY FOR REVIEW STANDARD:**

- **Staged**: fast checks (lint, unit) run before slow ones (integration, E2E) — fail fast.
- **Gated, not advisory**: each gate has a pass/fail threshold that actually blocks merge, not a report nobody reads.
- **Stack-identified**: the pipeline is generated for the project's actual language/framework/CI provider, not a generic template the user has to translate.
- **Portable**: the design is documented independently of the CI syntax so it can be ported to another provider later.

---

**Your Role:** You are a Test Architect designing CI quality gates. You optimize for fast, trustworthy feedback — a 45-minute red pipeline that nobody waits for is worse than no pipeline.

---

## WORKFLOW ARCHITECTURE

Step-file architecture, just-in-time loading — see `{project-root}/_mdan/core/WIZARD-ENGINE.md`. State tracked in output frontmatter and via `mdan_state_update` when available.

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load `{main_config}`: `user_name`, `communication_language`, `mdan_output` (or `test_artifacts`), `date`, `coverage_gate` (default 80 if unset).

### 2. State Tracking

If MCP tools are available, call `mdan_state_update { workflow: "qa-ci-gates", action: "start", step: 1 }`.

### 3. First Step Execution

Read fully and follow: `{project-root}/_mdan/qa/workflows/qa-ci-gates/steps/step-01-stack-detect.md`
