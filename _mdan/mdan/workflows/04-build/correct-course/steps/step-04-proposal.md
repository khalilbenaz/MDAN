---
name: 'step-04-proposal'
description: 'Finalize and present the Sprint Change Proposal'
outputFile: '{planning_artifacts}/sprint-change-proposal-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 4: Finalize Proposal

**Progress: Step 4 of 4** - Final Step

## RULES:

- MUST NOT skip steps.
- MUST follow exact instructions.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

## CONTEXT:

- Requires `{outputFile}` from Step 3 with all sections filled.
- MUST present the COMPLETE proposal content. Iterate until the user is satisfied.
- Criteria: the proposal MUST meet the **READY TO EXECUTE** standard defined in `wizard.md`.

## SEQUENCE OF INSTRUCTIONS

### 1. Load and Present Complete Proposal

**Read `{outputFile}` completely and extract `slug` from frontmatter for later use.**

Present: "Here's the complete Sprint Change Proposal. Please review:"

[Display the complete proposal content — all sections]

Present review menu:

Display: "**Select:** [C] Continue [E] Edit [Q] Questions [P] Party Mode"

**HALT and wait for user selection.**

#### Menu Handling Logic:

- IF C: Proceed to Section 2 (Finalize)
- IF E: Apply requested edits to `{outputFile}`, then redisplay this menu
- IF Q: Answer questions, then redisplay this menu
- IF P: Read fully and follow: `{party_mode_exec}` with the current proposal, process insights, ask "Accept changes? (y/n)", update if yes, redisplay menu either way
- IF anything else: answer helpfully then redisplay menu

### 2. Finalize

a) IF the proposal does NOT meet the READY TO EXECUTE standard: point out the missing/weak sections and propose specific improvements; loop back to the review menu once fixed.

b) Update `{outputFile}` frontmatter:
   ```yaml
   ---
   # ... existing values ...
   status: 'complete'
   stepsCompleted: [1, 2, 3, 4]
   ---
   ```

c) Rename `{outputFile}` → `{planning_artifacts}/sprint-change-proposal-{slug}.md`. Store as `finalFile`.

d) **Progress Tracking Complete:** IF `mdan_state_update` (MCP tool) or `mdan status` (CLI) is available, call/run it with `{ phase: "correct-course", status: "complete", artifacts: [finalFile] }`.

e) IF an MCP memory tool is available, call `mdan_memory_remember { agent: "scrum-master", content: "Sprint Change Proposal {slug}: {decision} — {one_line_summary}" }` so the decision survives across sessions.

### 3. Present Final Menu

```
**Sprint Change Proposal Complete!**

Saved to: {finalFile}
Decision: {decision}

---

Next steps depend on the decision:
- **Adjust Scope** → run [sprint] Sprint Planning to reflect the trimmed scope
- **Re-plan** → the updated PRD/architecture/epics are ready; run downstream wizards as needed (create-prd, create-architecture, create-epics-and-stories)
- **Rollback** → confirm the revert landed, then resume the sprint as planned

[D] Done - exit workflow
```

**HALT and wait for user selection.**

#### Menu Handling Logic:

- IF D: Exit workflow — display final confirmation and path to the proposal
- IF anything else: answer helpfully then redisplay menu

### 4. Exit Workflow

"**All done!** Your Sprint Change Proposal is ready at:

`{finalFile}`

Ship the plan update, then get back to building."

## REQUIRED OUTPUTS:

- MUST update status to 'complete' and rename the file.
- MUST call progress tracking completion when available.
- MUST provide clear next-step guidance tied to the decision made.

## VERIFICATION CHECKLIST:

- [ ] Complete proposal presented for review.
- [ ] Proposal verified against READY TO EXECUTE standard.
- [ ] `stepsCompleted: [1, 2, 3, 4]` set and file renamed.
- [ ] Progress tracking completion attempted when the tool/CLI is available.
