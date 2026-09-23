---
name: 'step-03-update'
description: 'Update PRD, architecture, and epics to reflect the chosen path'
nextStepFile: './step-04-proposal.md'
outputFile: '{planning_artifacts}/sprint-change-proposal-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 3: Update Affected Artifacts

**Progress: Step 3 of 4** - Next: Finalize Proposal

## RULES:

- MUST NOT skip steps.
- MUST NOT optimize sequence.
- MUST follow exact instructions.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

## CONTEXT:

- Requires `{outputFile}` from Step 2 with the decision recorded.
- Focus: make the plan tell the truth again. Only touches artifacts named in the Step 1 impact list.
- If the decision was Rollback with nothing to update in PRD/architecture/epics, this step still runs — to record what was reverted and confirm no residual inconsistency remains.

## SEQUENCE OF INSTRUCTIONS

### 1. List Concrete Edits

a) For each artifact in the Step 1 impact list, propose the specific edit needed (section, old text → new text, or new section to add). No vague intentions — a fresh reader must be able to apply the edit without guessing.

b) Present the list of proposed edits to `{user_name}` for confirmation before touching any file:

```
**Proposed edits:**
1. {artifact_path} — {change_description}
2. {artifact_path} — {change_description}
...

Proceed with these edits? [Y] Apply [E] Edit the list [S] Skip actual file edits, just document them in the proposal
```

c) **HALT and wait for user selection.**

### 2. Apply the Edits

a) **IF [Y]:** Apply each edit to its target file directly. After each edit, confirm the file was changed and show the diff-relevant snippet.

b) **IF [E]:** Revise the list per user feedback, then re-present the menu in Section 1.

c) **IF [S]:** Do not touch the target files — record the intended edits in the proposal as follow-up actions for the user to apply manually.

### 3. Record in the Proposal

a) Fill the **Artifact Updates** section of `{outputFile}` with the list of edits and their status (`applied` or `documented-only`).

b) IF a Context Graph is available (via MCP `mdan_graph_add_node` / `mdan_graph_add_edge` or `mdan graph` CLI), register this change as a decision node linked to the artifacts it impacted.

c) Update frontmatter: `stepsCompleted: [1, 2, 3]`.

### 4. Present Checkpoint Menu

Display: "**Select:** [C] Continue to Finalize Proposal (Step 4 of 4)"

**HALT and wait for user selection.**

#### Menu Handling Logic:

- IF C: Verify `{outputFile}` has `stepsCompleted: [1, 2, 3]`, then read fully and follow: `{project-root}/_mdan/mdan/workflows/04-build/correct-course/steps/step-04-proposal.md`
- IF anything else: answer helpfully then redisplay menu

## REQUIRED OUTPUTS:

- MUST list a concrete edit for every artifact in the impact list.
- MUST record whether each edit was applied or left for the user.

## VERIFICATION CHECKLIST:

- [ ] Every impacted artifact from Step 1 has a corresponding edit entry (applied or documented).
- [ ] `stepsCompleted: [1, 2, 3]` recorded.
