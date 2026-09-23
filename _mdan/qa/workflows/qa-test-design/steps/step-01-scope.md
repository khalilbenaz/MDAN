---
name: 'step-01-scope'
description: 'Identify the story/epic under design and enumerate its failure-mode scenarios'
templateFile: '../templates/test-design-template.md'
wipFile: '{mdan_output}/test-design-wip.md'
nextStepFile: './step-02-risk-scoring.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 1: Scope & Scenario Enumeration

**Progress: Step 1 of 4** - Next: Risk Scoring

## RULES:

- MUST NOT skip steps.
- MUST follow exact instructions.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## CONTEXT:

- Focus: identify what is being tested and every way it can fail — not yet how to test it.
- Investigation: surface-level only (read the story/epic and referenced acceptance criteria). Deep code investigation is out of scope for this workflow.

## SEQUENCE OF INSTRUCTIONS

### 0. Check for Work in Progress

a) Check if `{wipFile}` exists.

b) **IF IT EXISTS**, read its frontmatter (`title`, `slug`, `stepsCompleted`), present:

```
Hey {user_name}! Found a test design in progress: **{title}** — Step {lastStep} of 4.
Resume it?
[Y] Yes, continue   [N] No, archive and start new
```

HALT and wait. On [Y], jump to the step after the last completed one. On [N], rename `{wipFile}` to `{mdan_output}/test-design-{slug}-archived-{date}.md` and continue below.

### 1. Identify the Target

a) Ask: "What story or epic are we designing tests for? Paste the ID, title, or content — or point me at the file."

b) Read the story/epic content. If it references a PRD requirement ID (FR-xxx/NFR-xxx), note it — it will be needed for `qa-traceability` later.

c) If MCP tools are available, look up the story/epic node in the context graph (e.g. via `mdan_graph_impact` on its node id) to see what already depends on it. If unavailable, skip silently.

### 2. Enumerate Scenarios

For the target, list every distinct scenario a tester would need to consider. Be systematic — do not just restate the acceptance criteria. For each AC, derive:

- **Happy path**: the AC exactly as specified.
- **Boundary conditions**: min/max values, empty/null inputs, off-by-one (first/last page, zero items, exactly-at-limit amounts).
- **Negative paths**: invalid input, unauthorized access, expired/missing state.
- **Concurrency / state**: what happens if two actors act on the same resource at once, or the same action is retried (idempotency).
- **Integration failure**: what happens if a downstream dependency (DB, external API, queue) is slow, down, or returns garbage.

Present the enumerated list as a numbered table: `# | Scenario | Type (happy/boundary/negative/concurrency/integration) | AC/Requirement ref`.

### 3. Confirm Scope

Ask the user to confirm or edit the list before scoring. Explicitly ask: "Anything I'm missing — a known fragile area, a past incident, a compliance requirement?"

### 4. Initialize WIP File

a) Copy `{templateFile}` to `{wipFile}`.

b) Fill frontmatter:

```yaml
---
title: '{title}'
slug: '{slug}'
target_id: '{story-or-epic-id}'
created: '{date}'
status: 'in-progress'
stepsCompleted: [1]
---
```

c) Fill the **Scope** and **Scenarios (unscored)** sections with the confirmed list.

d) Write the file.

### 5. Present Checkpoint Menu

Display: "**Select:** [P] Party Mode — sanity-check the scenario list with other agents [C] Continue to Risk Scoring (Step 2 of 4)"

HALT and wait.

- IF P: Read fully and follow `{party_mode_exec}` with the current scenario list, process feedback, ask "Accept changes? (y/n)", update WIP if yes, redisplay menu.
- IF C: Verify `{wipFile}` has `stepsCompleted: [1]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-test-design/steps/step-02-risk-scoring.md`
- Other input: answer, then redisplay menu.

---

## VERIFICATION CHECKLIST:

- [ ] WIP check performed first.
- [ ] Scenario list covers happy/boundary/negative/concurrency/integration for every AC.
- [ ] `{wipFile}` created with `stepsCompleted: [1]`.
- [ ] User selected [C].
