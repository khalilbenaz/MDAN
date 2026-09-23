---
name: 'step-02-evidence'
description: 'Gather measured evidence against each threshold, per category'
wipFile: '{mdan_output}/nfr-assessment-wip.md'
nextStepFile: './step-03-score.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 2: Gather Evidence

**Progress: Step 2 of 3** - Next: Score & Finalize

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 1. Collect Evidence per Category

For each non-N/A category from Step 1, find or request the measured value:

**Performance**: look for load/perf test reports, APM dashboards, or ask the user to run one (e.g. k6/Locust/JMeter against the target endpoints). If none exists and a P0/P1 path is at risk on latency, that absence IS the finding — "no load test exists for the checkout endpoint" is evidence of a gap, not something to skip.

**Security**: run or request the output of the dependency audit command for this stack; check for a recent SAST/secret-scan run; walk the OWASP Top 10 checklist against the specific feature's attack surface (what user input reaches a query/shell/template/redirect?). Cite findings by severity.

**Reliability**: inspect the code/config for retry/timeout/circuit-breaker patterns on external calls; check whether mutating endpoints are idempotent (idempotency key, natural idempotency, or none); confirm a rollback/runbook exists for this change.

**Maintainability**: pull the actual coverage number (from the last CI run or by running the suite); pull lint/complexity results; grep for new TODO/FIXME/HACK comments introduced by this change (diff against the base branch if possible).

### 2. Cite Every Piece of Evidence

For every value, record: what was measured, how (tool/command/report), when, and the result. "Fast enough" is not a citation; "p95 = 240ms, k6 run 2026-09-20, 50 VUs" is.

### 3. Update WIP File

a) Write findings into the **Evidence** section of `{wipFile}`, one sub-table per category: `Item | Threshold | Measured | Source | Status (Met/Not Met/Unknown)`.

b) Update frontmatter: `stepsCompleted: [1, 2]`.

### 4. Checkpoint Menu

Display: "**Select:** [P] Party Mode [C] Continue to Score & Finalize (Step 3 of 3)"

HALT and wait.

- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: verify `stepsCompleted: [1, 2]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-nfr-assessment/steps/step-03-score.md`
- Other: answer, redisplay.

---

## VERIFICATION CHECKLIST:

- [ ] Every non-N/A threshold has a Met/Not Met/Unknown status with a cited source.
- [ ] Absence of evidence recorded as "Unknown" (a finding), never silently treated as Met.
- [ ] `stepsCompleted: [1, 2]` set.
