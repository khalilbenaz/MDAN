---
name: 'step-01-aggregate'
description: 'Collect the verdicts of every relevant QA artifact for this release, plus open defects'
templateFile: '../templates/release-decision-template.md'
wipFile: '{mdan_output}/release-gate-wip.md'
nextStepFile: './step-02-stale-check.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 1: Aggregate QA Artifacts

**Progress: Step 1 of 4** - Next: Staleness Check

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 0. Check for Work in Progress

Check `{wipFile}`; offer resume/archive if present (pattern: `{project-root}/_mdan/qa/workflows/qa-test-design/steps/step-01-scope.md`). HALT and wait.

### 1. Identify the Release Scope

Ask: "What's being released — a version tag, a set of epics/stories, a date-based cutoff?" Record it precisely; the gate decision only covers what's in scope.

### 2. Collect Existing Verdicts

For each artifact type, find the latest one relevant to this scope (search `{mdan_output}` for `test-design-*`, `traceability-*`, `nfr-assessment-*`, `test-review-*` files, and via the context graph if available):

- **Test design(s)**: pull P0/P1 scenario count and whether they have passing test coverage (cross-reference with `mdan_graph_impact` on the test-design node if registered).
- **Traceability matrix**: pull its `gate_decision` (PASS/CONCERNS/FAIL) directly — do not recompute it.
- **NFR assessment**: pull its `overall_verdict` directly.
- **Test review**: pull its overall score/band if one exists for the affected suite — a Failing-band suite undermines confidence in the other green signals.

If an expected artifact doesn't exist for something in scope (e.g. no traceability matrix run for this release), record it as **Missing** — a missing artifact is itself a finding, not something to skip past.

### 3. Collect Open Defects

Ask for (or search) the open defect/bug list relevant to this scope. For each, record: id, severity, whether it blocks a P0/P1 flow (cross-reference against test-design priorities if available), and whether a workaround exists.

### 4. Save Progress

a) Copy `{templateFile}` to `{wipFile}`.

b) Fill frontmatter (`title`, `slug`, `release_scope`, `created`, `status: in-progress`, `stepsCompleted: [1]`).

c) Fill the **Release Scope**, **Artifact Verdicts**, and **Open Defects** sections.

### 5. Checkpoint Menu

Display: "**Select:** [P] Party Mode [C] Continue to Staleness Check (Step 2 of 4)"

HALT and wait.

- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: verify `stepsCompleted: [1]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-release-gate/steps/step-02-stale-check.md`
- Other: answer, redisplay.

---

## VERIFICATION CHECKLIST:

- [ ] Release scope explicit.
- [ ] Every relevant artifact type addressed — found-with-verdict or explicitly Missing.
- [ ] Open defects listed with severity and P0/P1-flow linkage.
- [ ] `stepsCompleted: [1]` set.
