---
name: 'step-04-report'
description: 'Finalize and present the retrospective report'
outputFile: '{implementation_artifacts}/retrospective-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 4: Final Report

**Progress: Step 4 of 4** - Final Step

## RULES:

- MUST NOT skip steps.
- MUST follow exact instructions.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

## CONTEXT:

- Requires `{outputFile}` from Step 3 with confirmed action items and memory persistence status.
- Criteria: the retro MUST meet the **READY TO CLOSE** standard defined in `wizard.md`.

## SEQUENCE OF INSTRUCTIONS

### 1. Load and Present Complete Report

**Read `{outputFile}` completely and extract `slug` from frontmatter.**

Present: "Here's the complete retrospective. Please review:"

[Display the complete report — all sections]

"**Quick Summary:**

- {went_well_count} things that went well
- {didnt_count} issues analyzed with root causes
- {action_count} action items with owners
- {memory_count} lessons persisted to agent memory"

Present review menu:

Display: "**Select:** [C] Continue [E] Edit [Q] Questions"

**HALT and wait for user selection.**

#### Menu Handling Logic:

- IF C: Proceed to Section 2 (Finalize)
- IF E: Apply requested edits to `{outputFile}`, then redisplay this menu
- IF Q: Answer questions, then redisplay this menu
- IF anything else: answer helpfully then redisplay menu

### 2. Finalize

a) IF the retro does NOT meet the READY TO CLOSE standard: point out the gap (e.g. an action item with no owner, a one-sided list) and fix it before proceeding.

b) Update `{outputFile}` frontmatter:
   ```yaml
   ---
   # ... existing values ...
   status: 'complete'
   stepsCompleted: [1, 2, 3, 4]
   ---
   ```

c) Rename `{outputFile}` → `{implementation_artifacts}/retrospective-{slug}.md`. Store as `finalFile`.

d) **Progress Tracking Complete:** IF `mdan_state_update` (MCP tool) or `mdan status` (CLI) is available, call/run it with `{ phase: "retrospective", status: "complete", artifacts: [finalFile] }`.

### 3. Present Final Menu

```
**Retrospective Complete!**

Saved to: {finalFile}

{action_count} action item(s) ready to track. {memory_count} lesson(s) persisted to agent memory for next time.

[D] Done - exit workflow
```

**HALT and wait for user selection.**

#### Menu Handling Logic:

- IF D: Exit workflow — display final confirmation and path to the report
- IF anything else: answer helpfully then redisplay menu

### 4. Exit Workflow

"**All done!** The retrospective is saved at:

`{finalFile}`

Next epic/sprint, start by re-reading the action items — that's the whole point of doing this."

## REQUIRED OUTPUTS:

- MUST update status to 'complete' and rename the file.
- MUST call progress tracking completion when available.

## VERIFICATION CHECKLIST:

- [ ] Complete report presented for review.
- [ ] Report verified against READY TO CLOSE standard.
- [ ] `stepsCompleted: [1, 2, 3, 4]` set and file renamed.
- [ ] Progress tracking completion attempted when the tool/CLI is available.
