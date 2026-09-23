---
name: 'step-02-score'
description: 'Score the test suite against the 5-dimension quality checklist'
wipFile: '{mdan_output}/test-review-wip.md'
nextStepFile: './step-03-report.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 2: Score Against Checklist

**Progress: Step 2 of 3** - Next: Report & Remediation

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 1. Score the 5 Dimensions

Read the actual test code for the files in scope (not summaries). Score each dimension 0-4 (0 = pervasive problem, 4 = consistently excellent), citing specific tests for anything below 3:

**1. Determinism (0-4)**
- Violations: reliance on real system clock/`Date.now()` without freezing/injecting it, unseeded randomness, reliance on network calls to third parties, reliance on test execution order, floating-point equality without tolerance.
- 4 = no such patterns found; 0 = found in most files.

**2. Isolation (0-4)**
- Violations: shared mutable state between tests (module-level variables, shared DB rows without cleanup), tests that only pass when run in a specific order, missing `beforeEach`/`afterEach` teardown, tests that depend on a previous test's side effect.
- Quick check: can each test run alone (`-t "test name"`) and pass? If not, isolation is broken.

**3. Assertion Quality (0-4)**
- Violations: no assertion at all (a test that only calls code and expects no throw), overly broad assertions (`expect(result).toBeTruthy()` when a specific value is knowable), asserting implementation details (internal method call counts) instead of observable behavior, missing negative-case assertions (only checking the happy path returned something, not that it's correct).

**4. Naming & Readability (0-4)**
- Violations: names that don't state the expected behavior (`test1`, `testUserStuff`), no clear Arrange/Act/Assert (or Given/When/Then) structure, magic numbers/strings without explanation, excessive setup duplicated instead of using a factory/builder.

**5. Speed & Feedback (0-4)**
- Violations: unit tests that hit a real DB/network (should be integration-tier, mislabeled), sleep()-based waits instead of proper async/condition waits, suite runtime that discourages running it locally before commit.

### 2. Diagnose Flaky Tests Specifically

For any test known or suspected flaky (from CI history or Step 1 flags), name the root cause using this triage order: (1) time/clock dependency, (2) shared/leaked state between tests, (3) race condition on async code without proper awaiting, (4) network/external dependency not mocked, (5) test order dependency, (6) resource exhaustion (parallel runs competing for a port/file). Do not label a test "flaky" without picking one of these — "just flaky" is not a diagnosis.

### 3. Update WIP File

a) Write the scored checklist + flaky-test diagnoses into the **Checklist Scores** and **Flaky Test Diagnosis** sections of `{wipFile}`.

b) Update frontmatter: `stepsCompleted: [1, 2]`.

### 4. Checkpoint Menu

Display: "**Select:** [P] Party Mode [C] Continue to Report & Remediation (Step 3 of 3)"

HALT and wait.

- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: verify `stepsCompleted: [1, 2]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-test-review/steps/step-03-report.md`
- Other: answer, redisplay.

---

## VERIFICATION CHECKLIST:

- [ ] All 5 dimensions scored 0-4 with specific tests cited for anything below 3.
- [ ] Every flaky test assigned a root cause from the triage list.
- [ ] `stepsCompleted: [1, 2]` set.
