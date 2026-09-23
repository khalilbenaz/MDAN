---
name: 'step-01-collect-requirements'
description: 'Collect every FR/NFR id from the PRD and every story that claims to implement them'
templateFile: '../templates/traceability-matrix-template.md'
wipFile: '{mdan_output}/traceability-wip.md'
nextStepFile: './step-02-build-matrix.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 1: Collect Requirements & Stories

**Progress: Step 1 of 4** - Next: Build Matrix

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 0. Check for Work in Progress

Check `{wipFile}`; if present, offer resume/archive (same pattern as `{project-root}/_mdan/qa/workflows/qa-test-design/steps/step-01-scope.md`). HALT and wait.

### 1. Locate the PRD

Ask for the PRD path if not obvious, or search `{planning_artifacts}`/`mdan_output` for a PRD-like document. Extract every requirement id (`FR-xxx` functional, `NFR-xxx` non-functional). If the PRD uses a different id scheme, ask the user to confirm the pattern before proceeding — do not invent ids.

### 2. Locate the Stories/Epics

For each requirement id, find the story/epic(s) that claim to implement it (explicit reference in the story text, or — preferably — a `derived_from`/`input_to` edge in the context graph if MCP tools are available: call `mdan_graph_impact { nodeId: "<requirement-node-id>" }` and read the Downstream section). Record story id ↔ requirement id pairs.

### 3. Flag Orphans Early

a) Requirements with zero stories → flag immediately as **uncovered at the story level** (this alone is enough to drive the matrix's FAIL/CONCERNS rows later; no test can cover work that was never built).

b) Stories that don't map to any requirement id → note them separately (not necessarily a problem — could be technical debt/infra work — but call it out so the user can confirm it's intentional).

### 4. Save Progress

a) Copy `{templateFile}` to `{wipFile}`.

b) Fill frontmatter (`title`, `slug`, `prd_ref`, `created`, `status: in-progress`, `stepsCompleted: [1]`).

c) Fill **Requirements Inventory** and **Requirement → Story Mapping** sections.

### 5. Checkpoint Menu

Display: "**Select:** [P] Party Mode [C] Continue to Build Matrix (Step 2 of 4)"

HALT and wait.

- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: verify `stepsCompleted: [1]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-traceability/steps/step-02-build-matrix.md`
- Other: answer, redisplay.

---

## VERIFICATION CHECKLIST:

- [ ] Every FR/NFR id from the PRD extracted, none skipped.
- [ ] Story mapping attempted via context graph where available, not guesswork.
- [ ] Orphan requirements and orphan stories both flagged.
- [ ] `stepsCompleted: [1]` set.
