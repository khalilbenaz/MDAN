---
name: 'step-01-inventory'
description: 'Scope the review and inventory the test files/cases to examine'
templateFile: '../templates/test-review-checklist-template.md'
wipFile: '{mdan_output}/test-review-wip.md'
nextStepFile: './step-02-score.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 1: Scope & Inventory

**Progress: Step 1 of 3** - Next: Score Against Checklist

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 0. Check for Work in Progress

Check `{wipFile}`; offer resume/archive if present (pattern: `{project-root}/_mdan/qa/workflows/qa-test-design/steps/step-01-scope.md`). HALT and wait.

### 1. Define Scope

Ask: "Review the whole test suite, or a specific area (a package, a module, the flakiest tests from CI)?" If the user has CI history showing intermittent failures, ask for it — it's the fastest signal for flakiness.

### 2. Inventory Test Files

List the test files in scope with: file path, test count, framework, last-modified date (older, untouched tests are more likely to have rotted alongside the code they test).

### 3. Flag Structural Smells at a Glance

Before deep review, note anything visible immediately:

- Test files with skip/disable annotations (`.skip`, `[Ignore]`, `@pytest.mark.skip`) — these are silent coverage holes.
- Disproportionately large single test files (a 2000-line test file usually means poor isolation or copy-pasted setup).
- Test names like `test1`, `testFoo`, `should_work` — indicates unclear intent, flag for the naming dimension in Step 2.

### 4. Save Progress

a) Copy `{templateFile}` to `{wipFile}`.

b) Fill frontmatter (`title`, `slug`, `scope`, `created`, `status: in-progress`, `stepsCompleted: [1]`).

c) Fill the **Scope & Inventory** section.

### 5. Checkpoint Menu

Display: "**Select:** [P] Party Mode [C] Continue to Score Against Checklist (Step 2 of 3)"

HALT and wait.

- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: verify `stepsCompleted: [1]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-test-review/steps/step-02-score.md`
- Other: answer, redisplay.

---

## VERIFICATION CHECKLIST:

- [ ] Scope explicit (whole suite or named subset).
- [ ] Test files inventoried with skip-annotations and outsized files flagged.
- [ ] `stepsCompleted: [1]` set.
