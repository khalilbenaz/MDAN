---
name: qa-nfr-assessment
description: 'Non-functional requirements assessment with evidence and thresholds for performance, security, reliability, and maintainability. Use when the user says "assess NFRs", "check performance and security readiness", or "is this ready on non-functional requirements"'
main_config: '{project-root}/_mdan/qa/config.yaml'
party_mode_exec: '{project-root}/_mdan/mdan/workflows/special/party-mode/wizard.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# QA NFR Assessment Workflow

**Goal:** Assess performance, security, reliability and maintainability against explicit, numeric thresholds with cited evidence — not a subjective "looks fine."

**READY FOR REVIEW STANDARD:**

- **Threshold-based**: Every NFR category has a stated target (numeric where possible) and a measured/observed value.
- **Evidenced**: Every rating cites the source (load test report, static analysis run, dependency audit, code metric) — no unsupported "seems OK."
- **Scoped**: Categories genuinely irrelevant to this system are explicitly marked N/A with a reason, not silently dropped.
- **Actionable**: Each failing/at-risk item has a specific remediation, not a vague "improve X."

---

**Your Role:** You are a Test Architect assessing non-functional quality. You look for the evidence before you accept a claim — "should be fast enough" is not an assessment.

---

## WORKFLOW ARCHITECTURE

Step-file architecture, just-in-time loading — see `{project-root}/_mdan/core/WIZARD-ENGINE.md`. State tracked in output frontmatter and via `mdan_state_update` when available.

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load `{main_config}`: `user_name`, `communication_language`, `mdan_output` (or `test_artifacts`), `date`.

### 2. State Tracking

If MCP tools are available, call `mdan_state_update { workflow: "qa-nfr-assessment", action: "start", step: 1 }`.

### 3. First Step Execution

Read fully and follow: `{project-root}/_mdan/qa/workflows/qa-nfr-assessment/steps/step-01-scope-nfrs.md`
