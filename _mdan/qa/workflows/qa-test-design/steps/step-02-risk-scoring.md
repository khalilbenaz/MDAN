---
name: 'step-02-risk-scoring'
description: 'Score every scenario by probability x impact and derive its P0-P3 priority'
wipFile: '{mdan_output}/test-design-wip.md'
nextStepFile: './step-03-test-levels.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 2: Risk Scoring (Probability x Impact)

**Progress: Step 2 of 4** - Next: Test Level Mapping

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## CONTEXT:

- Requires `{wipFile}` with the scenario list from Step 1.
- Objective: turn a subjective "this feels important" into a defensible, comparable number.

## SEQUENCE OF INSTRUCTIONS

### 1. Score Each Scenario

For every scenario in the list, assign:

**Probability (1-5)** — likelihood this fails in production if untested:

| Score | Meaning |
|---|---|
| 5 | Near-certain: new/rewritten code, complex logic, known-fragile area, high change frequency |
| 4 | Likely: moderately complex logic, several edge cases, external dependency involved |
| 3 | Possible: standard CRUD/business logic, moderate complexity |
| 2 | Unlikely: simple, well-trodden code path, framework-handled |
| 1 | Rare: trivial, static, or already covered by an existing regression suite |

**Impact (1-5)** — consequence if it fails and reaches production:

| Score | Meaning |
|---|---|
| 5 | Data loss/corruption, security breach, financial/regulatory exposure, total outage |
| 4 | Core user journey broken (checkout, login, payment), no workaround |
| 3 | Feature broken but workaround exists, or partial degradation |
| 2 | Cosmetic/minor UX issue, non-blocking |
| 1 | Negligible, internal-only, or affects an unused code path |

**Risk score = Probability x Impact** (range 1-25).

Present the scored table: `# | Scenario | Probability | Impact | Score | Priority`.

### 2. Derive Priority

Apply the standard MDAN QA thresholds (override in `{project-root}/_mdan/qa/config.yaml` via `risk_threshold_p0` etc. if the user wants stricter/looser gates):

| Score range | Priority | Meaning |
|---|---|---|
| 15-25 | **P0** | Must test before every release. Blocks the release gate if untested or failing. |
| 10-14 | **P1** | Must test before release. Blocking unless explicitly waived with a documented reason. |
| 5-9 | **P2** | Should test. Gap is a CONCERNS on the release gate, not a FAIL. |
| 1-4 | **P3** | Nice to have. Document as a known gap; do not block on it. |

### 3. Sanity-Check the Distribution

a) If more than ~30% of scenarios land P0, push back: ask the user which of them are actually P1 — an over-inflated P0 list defeats prioritization.

b) If zero scenarios are P0/P1 for a story that touches money, auth, or data integrity, flag it explicitly: "This touches {sensitive area} but nothing scored P0/P1 — double-check the impact scores."

### 4. Update WIP File

a) Write the scored table into the **Risk Scoring** section of `{wipFile}`.

b) Update frontmatter: `stepsCompleted: [1, 2]`.

### 5. Present Checkpoint Menu

Display: "**Select:** [P] Party Mode [C] Continue to Test Level Mapping (Step 3 of 4)"

HALT and wait.

- IF P: Read fully and follow `{party_mode_exec}`, process feedback, update WIP if accepted, redisplay menu.
- IF C: Verify `stepsCompleted: [1, 2]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-test-design/steps/step-03-test-levels.md`
- Other input: answer, then redisplay menu.

---

## VERIFICATION CHECKLIST:

- [ ] Every scenario has probability, impact, score, priority.
- [ ] Distribution sanity-checked (no P0 inflation, no missed P0 on sensitive areas).
- [ ] `stepsCompleted: [1, 2]` set.
