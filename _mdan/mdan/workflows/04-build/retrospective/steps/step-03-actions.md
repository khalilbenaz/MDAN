---
name: 'step-03-actions'
description: 'Define action items and persist durable lessons as agent memories'
nextStepFile: './step-04-report.md'
outputFile: '{implementation_artifacts}/retrospective-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 3: Action Items & Memory

**Progress: Step 3 of 4** - Next: Final Report

## RULES:

- MUST NOT skip steps.
- MUST NOT optimize sequence.
- MUST follow exact instructions.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

## CONTEXT:

- Requires `{outputFile}` from Step 2 with confirmed root causes.
- Focus: every root cause becomes an owned action item, and every durable lesson gets persisted so it survives context resets.

## SEQUENCE OF INSTRUCTIONS

### 1. Turn Root Causes Into Action Items

a) For each root cause from Step 2, propose one concrete action item: what changes, who/what agent owns it, and how we'd know it worked next time.

b) For notable "what went well" patterns worth keeping, propose one action item to codify the practice (e.g. "add this pattern to project-context.md").

c) Present the action items list to `{user_name}` for confirmation or edits.

d) **HALT and wait for confirmation.**

### 2. Persist Durable Lessons as Agent Memories

a) For each confirmed action item and root cause, determine which agent(s) it's most relevant to (analyst, pm, architect, dev, ux-designer, scrum-master, tech-writer, security).

b) **IF an MCP memory tool is available:** call `mdan_memory_remember { agent: "<agent-id>", content: "<lesson, phrased as an actionable fact — e.g. 'Story estimates for payment flows run ~2x over; pad by 100% or split earlier'>" }` for each durable lesson. Confirm each call succeeded.

c) **ELSE:** note in the report that memory persistence was skipped (MCP tool unavailable) and that the lessons only live in this document — flag this to the user.

### 3. Update the Retro Document

a) Fill the **Action Items** section of `{outputFile}` with owner and success signal per item.

b) Fill the **Memories Persisted** section with the list of `{agent, lesson}` pairs that were (or were not) stored.

c) Update frontmatter: `stepsCompleted: [1, 2, 3]`.

### 4. Present Checkpoint Menu

Display: "**Select:** [C] Continue to Final Report (Step 4 of 4)"

**HALT and wait for user selection.**

#### Menu Handling Logic:

- IF C: Verify `{outputFile}` has `stepsCompleted: [1, 2, 3]`, then read fully and follow: `{project-root}/_mdan/mdan/workflows/04-build/retrospective/steps/step-04-report.md`
- IF anything else: answer helpfully then redisplay menu

## REQUIRED OUTPUTS:

- MUST produce at least one owned action item per confirmed root cause.
- MUST attempt to persist durable lessons via `mdan_memory_remember` when available, and record which were stored.

## VERIFICATION CHECKLIST:

- [ ] Every root cause has an action item with an owner.
- [ ] Memory persistence attempted (or explicitly flagged as skipped) for each durable lesson.
- [ ] `stepsCompleted: [1, 2, 3]` recorded.
