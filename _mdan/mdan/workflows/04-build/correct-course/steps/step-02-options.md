---
name: 'step-02-options'
description: 'Evaluate the three recovery options and recommend one'
nextStepFile: './step-03-update.md'
outputFile: '{planning_artifacts}/sprint-change-proposal-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 2: Options Evaluation

**Progress: Step 2 of 4** - Next: Update Artifacts

## RULES:

- MUST NOT skip steps.
- MUST NOT optimize sequence.
- MUST follow exact instructions.
- MUST NOT look ahead to future steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

## CONTEXT:

- Requires `{outputFile}` from Step 1 with the trigger and impact analysis.
- Focus: turn the impact analysis into exactly one recommended path.

## SEQUENCE OF INSTRUCTIONS

### 1. Evaluate the Three Standard Options

For each of the three options below, write 2-4 sentences grounded in the Step 1 impact analysis — not generic pros/cons:

a) **Adjust Scope** — Trim or reshuffle the current epic/sprint so the plan still holds without touching PRD/architecture. What exactly would be cut or deferred?

b) **Re-plan** — Update PRD, architecture, and/or epics to reflect the new reality, then re-run sprint planning. Which specific sections of which documents need to change?

c) **Rollback** — Revert the decision or work that caused the drift and return to the last known-good state. What would be reverted, and what would be lost?

### 2. Recommend One Path

a) **Pick the option that best fits the evidence** — smallest disruption that still tells the truth about the new situation. State the recommendation plainly with the reasoning.

b) **Present to the user:**

```
**Impact:** {impact_summary}

**Options:**
[A] Adjust Scope — {adjust_scope_summary}
[R] Re-plan — {replan_summary}
[B] Rollback — {rollback_summary}

**Recommendation:** {recommended_option} — {why}

Which do you want to go with? [A/R/B] or describe a hybrid.
```

c) **HALT and wait for the user's decision.**

d) **If the user picks a hybrid or disagrees**, capture their reasoning and the resulting path — do not argue, document their decision.

### 3. Update the Proposal

a) Fill in the **Options Considered** and **Decision** sections of `{outputFile}` with the three write-ups and the chosen path (with rationale).

b) Update frontmatter: `stepsCompleted: [1, 2]`, and add `decision: '<A|R|B|hybrid>'`.

### 4. Present Checkpoint Menu

Display: "**Select:** [P] Party Mode (stress-test the decision) [C] Continue to Update Artifacts (Step 3 of 4)"

**HALT and wait for user selection.**

#### Menu Handling Logic:

- IF P: Read fully and follow: `{party_mode_exec}` with the current decision, process collaborative insights, ask "Accept changes? (y/n)", update `{outputFile}` if yes, redisplay menu either way
- IF C: Verify `{outputFile}` has `stepsCompleted: [1, 2]`, then read fully and follow: `{project-root}/_mdan/mdan/workflows/04-build/correct-course/steps/step-03-update.md`
- IF anything else: answer helpfully then redisplay menu

## REQUIRED OUTPUTS:

- MUST document all three options with reasoning tied to the impact analysis.
- MUST record the user's decision.

## VERIFICATION CHECKLIST:

- [ ] All three options evaluated, not just the recommended one.
- [ ] User made and confirmed a decision.
- [ ] `stepsCompleted: [1, 2]` recorded.
