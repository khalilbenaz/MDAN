---
name: 'step-02-generate-tests'
description: 'Generate the concrete, executable, failing acceptance tests in the project test framework'
wipFile: '{mdan_output}/atdd-wip.md'
nextStepFile: './step-03-link-graph.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 2: Generate Failing Acceptance Tests

**Progress: Step 2 of 3** - Next: Link & Register

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 1. Detect the Test Framework

Scan the project (package.json/pyproject.toml/*.csproj/go.mod, existing `test/`/`tests/`/`__tests__`/`spec/` directories) to detect the framework already in use (e.g. Jest/Vitest/Playwright for JS/TS, pytest/behave for Python, xUnit/SpecFlow for .NET, RSpec/Cucumber for Ruby). Use it — do not introduce a second test framework for acceptance tests unless none exists, in which case propose one suited to the AC's layer (BDD framework like Cucumber/SpecFlow/behave for stakeholder-readable Given/When/Then; plain test-runner `describe/it` blocks with G/W/T comments otherwise) and confirm with the user.

### 2. Write One Test per Given/When/Then

For each normalized AC from Step 1, write a real test:

- **Test name** states the behavior, not the mechanism: `should_reject_transfer_when_balance_insufficient`, not `test_case_3`.
- **Given** → setup/fixtures/mocks representing the precondition exactly (use factories/builders already in the codebase if they exist — check for a `test/fixtures` or `test/factories` dir first).
- **When** → the single action, through the public interface (call the API/service/CLI entrypoint, not a private method).
- **Then** → a real assertion on the observable outcome (status code, return value, DB row, emitted event) — never a placeholder `assert True`.
- Tag or annotate the test with the AC id (comment, tag, or naming convention consistent with the codebase) so traceability holds.

### 3. Confirm They Fail For the Right Reason

a) Instruct/run the test suite for these new tests (or tell the user the exact command to run if you cannot execute it yourself).

b) Every new test MUST fail. If a test fails with a syntax/import/compile error, that is a BUG in the test — fix it. The only acceptable failure is "expected behavior not implemented" (e.g. `404 Not Found` when an endpoint doesn't exist yet, or a clear assertion mismatch).

c) If a test unexpectedly PASSES, stop and investigate: either the feature already exists, or the test is not actually exercising the new behavior — both must be resolved before moving on.

### 4. Update WIP File

a) Write the generated test file paths + one-line summaries into the **Generated Tests** section of `{wipFile}`.

b) Update frontmatter: `stepsCompleted: [1, 2]`.

### 5. Checkpoint Menu

Display: "**Select:** [P] Party Mode [C] Continue to Link & Register (Step 3 of 3)"

HALT and wait.

- IF P: read and follow `{party_mode_exec}`, redisplay menu after.
- IF C: verify `stepsCompleted: [1, 2]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-atdd/steps/step-03-link-graph.md`
- Other: answer, redisplay menu.

---

## VERIFICATION CHECKLIST:

- [ ] Correct/existing test framework used, no needless new one introduced.
- [ ] One test per Given/When/Then, real assertions, no placeholders.
- [ ] Every test confirmed failing for the right reason (missing behavior, not broken test).
- [ ] `stepsCompleted: [1, 2]` set.
