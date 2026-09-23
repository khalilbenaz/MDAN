---
name: 'step-01-trigger'
description: 'Capture the triggering issue and run impact analysis on affected artifacts'
nextStepFile: './step-02-options.md'
outputFile: '{planning_artifacts}/sprint-change-proposal-wip.md'
templateFile: '../templates/change-proposal-template.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 1: Trigger & Impact Analysis

**Progress: Step 1 of 4** - Next: Options Evaluation

## RULES:

- MUST NOT skip steps.
- MUST NOT optimize sequence.
- MUST follow exact instructions.
- MUST NOT look ahead to future steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

## CONTEXT:

- Variables from `wizard.md` are available in memory.
- Focus: nail down exactly what changed and what it touches, before proposing anything.

## SEQUENCE OF INSTRUCTIONS

### 0. Check for Work in Progress

a) Check if `{outputFile}` exists.

b) **IF IT EXISTS:**

1. Read the frontmatter and extract `title`, `slug`, `stepsCompleted`.
2. Present:

```
Hey {user_name}! Found a sprint change proposal in progress:

**{title}** - Step {lastStep} of 4 complete

Is this what you're here to continue?

[Y] Yes, pick up where I left off
[N] No, archive it and start a new one
```

3. **HALT and wait for user selection.**
4. **[Y]:** Jump to the step matching `stepsCompleted` (same mapping pattern as quick-spec: `[1]` → step-02, `[1,2]` → step-03, `[1,2,3]` → step-04).
5. **[N]:** Rename `{outputFile}` to `{planning_artifacts}/sprint-change-proposal-{slug}-archived-{date}.md` and continue below.

### 1. Capture the Triggering Issue

a) **Ask the user:** "Khbar {user_name}! Chnou li tbeddel? Explain what happened — a blocked dependency, a new constraint, a pivot, scope discovered too late, or anything else that breaks the current plan."

b) **Push for specifics.** A vague "the scope grew" is not enough — get the concrete evidence: which story, which file, which requirement, which conversation.

### 2. Impact Analysis

a) **Identify likely affected artifacts:** scan `{planning_artifacts}` and `{implementation_artifacts}` for PRD, architecture, epics/stories files related to the trigger.

b) **IF the `mdan_graph_impact` MCP tool is available:** call it with the artifact(s) identified in (a) to get the downstream impact list from the Context Graph.

c) **ELSE IF the `mdan impact <artifact>` or `mdan stale` CLI command is available:** run it (e.g. `mdan impact <artifact>` or `mdan stale`) and read its output.

d) **ELSE:** manually trace references — grep the PRD/architecture/epics for mentions of the affected area, and list every document, story, or decision that assumed the old state.

e) **Build the impact list:** for each affected artifact, note the artifact path and a one-line description of what is now inconsistent.

### 3. Initialize the Sprint Change Proposal

a) Copy `{templateFile}` to `{outputFile}`.

b) Fill in frontmatter:
   ```yaml
   ---
   title: '{title}'
   slug: '{slug}'
   created: '{date}'
   status: 'in-progress'
   stepsCompleted: [1]
   ---
   ```

c) Fill the **Triggering Issue** and **Impact Analysis** sections with what was captured above.

d) Report to `{user_name}`:

"Documented the trigger and impact. **{impact_count} artifact(s) affected**: {impact_summary}."

### 4. Present Checkpoint Menu

Display: "**Select:** [P] Party Mode (get other agents' read on the impact) [C] Continue to Options Evaluation (Step 2 of 4)"

**HALT and wait for user selection.**

#### Menu Handling Logic:

- IF P: Read fully and follow: `{party_mode_exec}` with the current impact analysis, process collaborative insights, ask "Accept changes? (y/n)", update `{outputFile}` if yes, redisplay menu either way
- IF C: Verify `{outputFile}` has `stepsCompleted: [1]`, then read fully and follow: `{project-root}/_mdan/mdan/workflows/04-build/correct-course/steps/step-02-options.md`
- IF anything else: answer helpfully then redisplay menu

## REQUIRED OUTPUTS:

- MUST initialize `{outputFile}` with trigger + impact analysis and `stepsCompleted: [1]`.

## VERIFICATION CHECKLIST:

- [ ] WIP check performed first.
- [ ] Triggering issue captured with concrete evidence.
- [ ] Impact analysis run via MCP tool, CLI, or manual trace — and documented.
- [ ] User selected [C] to continue.
