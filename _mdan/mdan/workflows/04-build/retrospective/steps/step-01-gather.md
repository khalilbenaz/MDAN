---
name: 'step-01-gather'
description: 'Scope the retro and gather what went well / what did not'
nextStepFile: './step-02-analyze.md'
outputFile: '{implementation_artifacts}/retrospective-wip.md'
templateFile: '../templates/retro-template.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 1: Scope & Gather

**Progress: Step 1 of 4** - Next: Root Cause Analysis

## RULES:

- MUST NOT skip steps.
- MUST NOT optimize sequence.
- MUST follow exact instructions.
- MUST NOT look ahead to future steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

## CONTEXT:

- Variables from `wizard.md` are available in memory.
- Focus: scope the retro (which epic/sprint) and collect raw, specific observations before analyzing anything.

## SEQUENCE OF INSTRUCTIONS

### 0. Check for Work in Progress

a) Check if `{outputFile}` exists.

b) **IF IT EXISTS:** present the same continue/archive menu pattern as other MDAN wizards (title + last completed step; [Y] continue at the right step, [N] archive to `{implementation_artifacts}/retrospective-{slug}-archived-{date}.md` and start fresh). **HALT and wait for selection** before proceeding.

### 1. Scope the Retro

a) **Ask:** "Salam {user_name}! Anta l'epic wla le sprint li bghina ndiro lih retro? (nom ou référence)"

b) **Capture:** `title` (e.g. "Epic 3 — Payments"), `slug` (url-safe).

c) **Ground the retro in real data:** scan `{implementation_artifacts}` and `{planning_artifacts}` for the epic/sprint's stories, sprint-status, and any correct-course proposals filed during it. Skim for objective facts (story count, cycle time signals, number of correct-course events) to inform, not replace, the human input below.

### 2. Gather "What Went Well"

a) **Ask:** "Chno mcha mzyan f had l'epic/sprint? Give me specific moments, decisions, or patterns — not generalities."

b) **Push for specificity.** If the user says "the team worked well together", ask for the concrete instance that proves it.

c) Capture as a list of specific entries.

### 3. Gather "What Didn't Go Well"

a) **Ask:** "W chno li 3atlna wla khass ye-improuva? Same rule — specific, with evidence, no blame on individuals."

b) **Redirect blame to process:** if the user names a person, gently redirect: "Fhemt, wach ymkn ndiro focus 3la le process wla la décision li deffet l had l'mochkil, bla ma nsemmiw chi wahed?"

c) Capture as a list of specific entries with, where relevant, the artifact/story it relates to.

### 4. Initialize the Retro Document

a) Copy `{templateFile}` to `{outputFile}`.

b) Fill frontmatter:
   ```yaml
   ---
   title: '{title}'
   slug: '{slug}'
   created: '{date}'
   status: 'in-progress'
   stepsCompleted: [1]
   ---
   ```

c) Fill **Scope**, **What Went Well**, and **What Didn't Go Well** sections.

### 5. Present Checkpoint Menu

Display: "**Select:** [P] Party Mode (bring other agents' perspectives) [C] Continue to Root Cause Analysis (Step 2 of 4)"

**HALT and wait for user selection.**

#### Menu Handling Logic:

- IF P: Read fully and follow: `{party_mode_exec}` with the current gathered items, process insights, ask "Accept additions? (y/n)", update `{outputFile}` if yes, redisplay menu either way
- IF C: Verify `{outputFile}` has `stepsCompleted: [1]`, then read fully and follow: `{project-root}/_mdan/mdan/workflows/04-build/retrospective/steps/step-02-analyze.md`
- IF anything else: answer helpfully then redisplay menu

## REQUIRED OUTPUTS:

- MUST initialize `{outputFile}` with scope, what-went-well, and what-didn't-go-well, all with specific entries.

## VERIFICATION CHECKLIST:

- [ ] WIP check performed first.
- [ ] Retro scoped to a specific epic/sprint.
- [ ] Both sections have specific, evidence-backed entries.
- [ ] No individual blamed by name.
