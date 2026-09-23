---
name: 'step-02-analyze'
description: 'Find root causes and patterns behind the gathered observations'
nextStepFile: './step-03-actions.md'
outputFile: '{implementation_artifacts}/retrospective-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 2: Root Cause Analysis

**Progress: Step 2 of 4** - Next: Action Items & Memory

## RULES:

- MUST NOT skip steps.
- MUST NOT optimize sequence.
- MUST follow exact instructions.
- MUST NOT look ahead to future steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

## CONTEXT:

- Requires `{outputFile}` from Step 1 with what-went-well / what-didn't entries.
- Focus: go one level deeper than the symptom for each "what didn't go well" entry.

## SEQUENCE OF INSTRUCTIONS

### 1. Analyze Each "What Didn't Go Well" Entry

For each entry from Step 1, ask "why did this happen?" at least once past the surface symptom (a lightweight 5-whys), and note:

- **Pattern**: is this a one-off or does it recur across epics/sprints? (cross-check against prior retros in `{implementation_artifacts}` if any exist)
- **Root cause**: the process/system/decision-level cause, not a person
- **Category**: process, tooling, scope/planning, communication, technical debt, external/blocked

### 2. Analyze Patterns in "What Went Well" Too

a) For notable wins, identify what made them work — is it a repeatable practice worth codifying?

### 3. Present Analysis for Confirmation

a) Present the root-cause table to `{user_name}` and ask them to confirm or correct each one — they have context the agent doesn't.

b) **HALT and wait for confirmation or corrections.** Apply corrections before proceeding.

### 4. Update the Retro Document

a) Fill the **Root Cause Analysis** section of `{outputFile}` with the confirmed table (entry, root cause, category, recurring?).

b) Update frontmatter: `stepsCompleted: [1, 2]`.

### 5. Present Checkpoint Menu

Display: "**Select:** [C] Continue to Action Items & Memory (Step 3 of 4)"

**HALT and wait for user selection.**

#### Menu Handling Logic:

- IF C: Verify `{outputFile}` has `stepsCompleted: [1, 2]`, then read fully and follow: `{project-root}/_mdan/mdan/workflows/04-build/retrospective/steps/step-03-actions.md`
- IF anything else: answer helpfully then redisplay menu

## REQUIRED OUTPUTS:

- MUST produce a root cause per "what didn't go well" entry, confirmed by the user.

## VERIFICATION CHECKLIST:

- [ ] Every "what didn't go well" entry has a root cause and category.
- [ ] User confirmed the analysis.
- [ ] `stepsCompleted: [1, 2]` recorded.
