---
name: 'step-03-decision'
description: 'Apply the aggregate gate formula and issue the go/no-go verdict'
wipFile: '{mdan_output}/release-gate-wip.md'
nextStepFile: './step-04-record.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 3: Decision

**Progress: Step 3 of 4** - Next: Record & Register

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 1. Apply the Aggregate Gate Formula

**FAIL** if ANY of:
- Any aggregated artifact (traceability/NFR) verdict is FAIL and unresolved/unwaived.
- Any unresolved Blocking staleness item from Step 2 remains.
- Any open defect is Critical/High severity AND blocks a P0/P1 flow with no workaround.
- A required artifact is Missing for something touching a P0/P1 flow (e.g. no traceability matrix run for a payment feature).

**CONCERNS** if, with no FAIL condition met, ANY of:
- Any aggregated artifact verdict is CONCERNS.
- Open defects exist that are Medium severity or blocked-but-workaround-exists.
- A non-critical artifact is Missing (documented as a known gap).
- A Blocking staleness item was resolved via waiver rather than re-verification.

**PASS** otherwise — all aggregated verdicts PASS, no unresolved staleness, no blocking open defects.

### 2. Compute and Justify

State explicitly which condition drove the verdict — never "overall it feels CONCERNS." Every FAIL/CONCERNS decision must cite the specific artifact, defect id, or staleness item responsible.

### 3. Present and Confirm

Display the full aggregation + decision. "**Select:** [C] Continue [E] Edit [W] Add/adjust a waiver [P] Party Mode"

HALT and wait.

- IF E: apply edits, redisplay.
- IF W: capture approver + reason, recompute, redisplay.
- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: proceed.

### 4. Update WIP File

a) Write the decision + justification into the **Gate Decision** section of `{wipFile}`.

b) Update frontmatter: `gate_decision: 'PASS'|'CONCERNS'|'FAIL'`, `stepsCompleted: [1, 2, 3]`.

### 5. Checkpoint Menu

Display: "**Select:** [C] Continue to Record & Register (Step 4 of 4)"

HALT and wait.

- IF C: verify `stepsCompleted: [1, 2, 3]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-release-gate/steps/step-04-record.md`
- Other: answer, redisplay.

---

## VERIFICATION CHECKLIST:

- [ ] Decision follows the formula exactly (no override without a documented, approved waiver).
- [ ] Justification cites specific artifacts/defects/staleness items, not vague impressions.
- [ ] `stepsCompleted: [1, 2, 3]` set.
