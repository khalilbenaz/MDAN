---
name: 'step-02-build-matrix'
description: 'Attach concrete test evidence to each requirement using the context graph and repository search'
wipFile: '{mdan_output}/traceability-wip.md'
nextStepFile: './step-03-gaps.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 2: Build the Coverage Matrix

**Progress: Step 2 of 4** - Next: Gap Analysis

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 1. Find Test Evidence per Story

For each story from Step 1, find the tests that verify it, in priority order:

1. **Graph-backed**: if a `test-design-*` or `atdd-*` node exists linked to the story with `derived_from`, use `mdan_graph_impact` to list it and its downstream test artifacts — this is the strongest evidence.
2. **Naming convention**: search the test suite for files/describe-blocks referencing the story id or AC ids (e.g. grep for the story id string).
3. **Manual mapping**: if neither exists, ask the user to point at the relevant test file(s), or mark the cell as unverified.

### 2. Build the Matrix Row per Requirement

For each requirement id, produce one row:

`FR/NFR id | Requirement summary | Story id(s) | Test evidence (file:test-name) | Level | Coverage status`

**Coverage status** — apply exactly one:

- **Covered**: named test(s) exist, pass, and directly assert the requirement's behavior.
- **Partial**: some ACs of the requirement have test evidence, others don't — list which.
- **Uncovered**: story exists but no test evidence found.
- **Untestable-as-specified**: the requirement is too vague to derive a test from (flag for the PRD author, don't silently skip).
- **Not implemented**: no story exists (carried over from Step 1's orphan flag).

### 3. Cross-Check with Staleness

If MCP tools are available, call `mdan_graph_stale` once. For any changed artifact that is upstream of a requirement/story/test node in this matrix, downgrade its status by one notch (Covered → Partial) and note "stale — re-verify" — the test may no longer reflect the current spec even if it still passes.

### 4. Update WIP File

a) Write the full matrix into the **Coverage Matrix** section of `{wipFile}`.

b) Update frontmatter: `stepsCompleted: [1, 2]`.

### 5. Checkpoint Menu

Display: "**Select:** [P] Party Mode [C] Continue to Gap Analysis (Step 3 of 4)"

HALT and wait.

- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: verify `stepsCompleted: [1, 2]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-traceability/steps/step-03-gaps.md`
- Other: answer, redisplay.

---

## VERIFICATION CHECKLIST:

- [ ] Every requirement row has a coverage status from the fixed vocabulary (no free text substitutes).
- [ ] Test evidence is a concrete file:test reference wherever status is Covered/Partial.
- [ ] Stale upstream artifacts downgraded and flagged.
- [ ] `stepsCompleted: [1, 2]` set.
