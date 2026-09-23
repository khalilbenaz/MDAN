---
name: 'step-03-gaps'
description: 'Summarize coverage gaps and their severity'
wipFile: '{mdan_output}/traceability-wip.md'
nextStepFile: './step-04-gate-decision.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 3: Gap Analysis

**Progress: Step 3 of 4** - Next: Gate Decision

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 1. Extract Every Non-"Covered" Row

Pull every row from the matrix that is Partial, Uncovered, Untestable-as-specified, or Not implemented into a gap list.

### 2. Rate Each Gap's Severity

Reuse the qa-test-design risk vocabulary for consistency — if a `test-design-*` node exists for the requirement's story, pull its priority (P0-P3) directly instead of re-scoring. Otherwise score quickly:

- **Blocking** — gap on an FR/NFR that is P0/P1 risk, or any NFR tagged security/compliance/data-integrity, regardless of priority.
- **Notable** — gap on a P2 risk requirement, or a Partial coverage on a P0/P1 (some but not all ACs covered).
- **Minor** — gap on a P3 risk requirement, or cosmetic/non-critical NFR.

### 3. Group and Present

Present the gap list grouped by severity, each entry with: requirement id, one-line reason, and a concrete next action ("write integration test for X", "clarify AC with PM", "implement missing story").

### 4. Update WIP File

a) Write the gap list into the **Gap Analysis** section of `{wipFile}`.

b) Update frontmatter: `stepsCompleted: [1, 2, 3]`.

### 5. Checkpoint Menu

Display: "**Select:** [P] Party Mode [C] Continue to Gate Decision (Step 4 of 4)"

HALT and wait.

- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: verify `stepsCompleted: [1, 2, 3]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-traceability/steps/step-04-gate-decision.md`
- Other: answer, redisplay.

---

## VERIFICATION CHECKLIST:

- [ ] Every non-Covered row appears in the gap list, none dropped silently.
- [ ] Each gap severity-rated with a stated reason, not a guess.
- [ ] `stepsCompleted: [1, 2, 3]` set.
