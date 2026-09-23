---
name: 'step-01-scope-nfrs'
description: 'Identify which NFR categories apply and set explicit thresholds for each'
templateFile: '../templates/nfr-assessment-template.md'
wipFile: '{mdan_output}/nfr-assessment-wip.md'
nextStepFile: './step-02-evidence.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 1: Scope & Thresholds

**Progress: Step 1 of 3** - Next: Gather Evidence

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 0. Check for Work in Progress

Check `{wipFile}`; offer resume/archive if present (pattern: `{project-root}/_mdan/qa/workflows/qa-test-design/steps/step-01-scope.md`). HALT and wait.

### 1. Identify the Target and Source of NFRs

Ask what system/feature/release is being assessed. Look for existing NFR-xxx ids in the PRD; if none, derive category-level requirements from context (e.g. "public API" implies latency + rate-limiting NFRs even if unstated).

### 2. Set Thresholds per Category

For each of the four categories, set an explicit, numeric-where-possible threshold. Use the PRD's stated NFR if present; otherwise propose the following defaults and confirm with the user (never assess silently against an un-agreed threshold):

**Performance**
- API p95 latency ≤ 300ms, p99 ≤ 1000ms (adjust per SLA); throughput target (req/s) sized to expected peak x safety margin (commonly 1.5-2x); error rate under load < 1%.

**Security**
- Zero Critical/High findings from dependency audit (`npm audit`/`pip-audit`/`dotnet list package --vulnerable`/etc.) unblocked; OWASP Top 10 categories reviewed for this feature (injection, broken auth, sensitive data exposure, access control, SSRF); secrets not committed (scan clean); authN/authZ enforced on every new endpoint.

**Reliability**
- Uptime/error-budget target if defined (e.g. 99.9%); retries + timeouts on every external call; idempotency on mutating endpoints that can be retried; graceful degradation defined for each critical dependency; documented rollback path.

**Maintainability**
- Test coverage does not regress below the project's `coverage_gate` (see `{project-root}/_mdan/qa/config.yaml`, default 80% if unset); cyclomatic complexity / lint rules pass with no new suppressions; no new TODO/FIXME on the critical path without a tracked ticket; documentation updated for new public interfaces.

### 3. Mark Irrelevant Categories N/A

If a category genuinely doesn't apply (e.g. a CLI-only internal tool has no meaningful "throughput under load"), mark it N/A with a one-line reason — do not delete the row.

### 4. Save Progress

a) Copy `{templateFile}` to `{wipFile}`.

b) Fill frontmatter (`title`, `slug`, `target`, `created`, `status: in-progress`, `stepsCompleted: [1]`).

c) Fill the **Thresholds** section.

### 5. Checkpoint Menu

Display: "**Select:** [P] Party Mode [C] Continue to Gather Evidence (Step 2 of 3)"

HALT and wait.

- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: verify `stepsCompleted: [1]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-nfr-assessment/steps/step-02-evidence.md`
- Other: answer, redisplay.

---

## VERIFICATION CHECKLIST:

- [ ] All 4 categories addressed (threshold set or explicit N/A + reason).
- [ ] Thresholds are numeric or clearly binary, confirmed with the user.
- [ ] `stepsCompleted: [1]` set.
