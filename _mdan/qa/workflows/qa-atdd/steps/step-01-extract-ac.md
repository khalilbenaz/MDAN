---
name: 'step-01-extract-ac'
description: 'Extract and normalize acceptance criteria into unambiguous Given/When/Then statements'
templateFile: '../templates/acceptance-tests-template.md'
wipFile: '{mdan_output}/atdd-wip.md'
nextStepFile: './step-02-generate-tests.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 1: Extract & Normalize Acceptance Criteria

**Progress: Step 1 of 3** - Next: Generate Failing Tests

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 0. Check for Work in Progress

Check `{wipFile}`. If it exists, present resume/archive choice as in other QA workflows (see `{project-root}/_mdan/qa/workflows/qa-test-design/steps/step-01-scope.md` for the exact pattern). HALT and wait.

### 1. Identify the Story

Ask: "Which story are we writing acceptance tests for? Paste it or point me at the file." Read the story and its acceptance criteria list. Note the story's node id if known (needed for graph linking in Step 3).

### 2. Normalize Each AC into Given/When/Then

For every acceptance criterion, rewrite it — if it isn't already — as:

```
Given <precondition / starting state>
When <the action the actor takes>
Then <the observable, verifiable outcome>
```

Rules for a GOOD Given/When/Then:

- **Given** sets up state, not behavior — no assertions here.
- **When** is a single action. Split multi-step interactions into multiple tests rather than one long When.
- **Then** must be objectively verifiable (a returned value, a status code, a persisted row, a visible element) — never "the system works correctly."
- If an AC is vague ("the user is notified"), STOP and ask: notified how — email, in-app toast, webhook? Do not guess; an ambiguous AC produces a test that tests the wrong thing.

### 3. Cover the Edges ATDD Tends to Skip

For each AC, also ask: is there an implied negative case? ("User can submit the form" implies "user CANNOT submit an invalid form" — that's a second test, not a footnote.) Add these as separate Given/When/Then entries, each still tagged with the AC id they extend.

### 4. Confirm and Save

a) Present the full normalized list numbered `AC1`, `AC1b` (negative), `AC2`, etc.

b) Ask user to confirm.

c) Copy `{templateFile}` to `{wipFile}`, fill frontmatter (`title`, `slug`, `story_id`, `created`, `status: in-progress`, `stepsCompleted: [1]`) and the **Normalized Acceptance Criteria** section.

### 5. Checkpoint Menu

Display: "**Select:** [P] Party Mode [C] Continue to Generate Failing Tests (Step 2 of 3)"

HALT and wait.

- IF P: read and follow `{party_mode_exec}`, update if accepted, redisplay menu.
- IF C: verify `stepsCompleted: [1]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-atdd/steps/step-02-generate-tests.md`
- Other: answer, redisplay menu.

---

## VERIFICATION CHECKLIST:

- [ ] Every AC normalized to Given/When/Then, no ambiguous "Then".
- [ ] Implied negative cases added as separate entries.
- [ ] `stepsCompleted: [1]` set.
