---
name: 'step-03-test-levels'
description: 'Assign the cheapest test level that still catches each failure mode'
wipFile: '{mdan_output}/test-design-wip.md'
nextStepFile: './step-04-document.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 3: Test Level Mapping

**Progress: Step 3 of 4** - Next: Document & Register

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## CONTEXT:

- Requires the scored scenario table from Step 2.
- Objective: pick the cheapest test level that would actually catch the failure — never default to E2E out of laziness.

## SEQUENCE OF INSTRUCTIONS

### 1. Apply the Level Selection Heuristic

For each scenario, choose ONE primary level using this decision order (stop at the first match):

1. **Unit** — if the failure mode is pure logic/computation/validation with no I/O (a function, a class method, a pricing formula, a state-machine transition). Fast, deterministic, cheapest to maintain. Default choice for P2/P3.
2. **Contract** — if the failure mode is at a service boundary (API request/response shape, event schema, message payload) shared between two independently deployed components. Prevents "works on my machine, breaks in prod" integration drift without needing both services running.
3. **Integration** — if the failure mode only manifests when the code talks to a real (or realistically faked) collaborator: database, cache, queue, filesystem, another internal service. Use for repository/DAL logic, transaction boundaries, migration correctness.
4. **E2E** — reserve for the smallest possible set: the critical user journeys where the thing under test is the integration of the whole stack through the UI/API surface a real user hits (login, checkout, payment capture). Slow, flaky-prone, expensive to maintain — never use E2E to compensate for missing unit coverage.

### 2. Respect the Pyramid

a) Tally the level distribution. Target shape (adjust for risk profile, but justify deviations explicitly):

```
Unit         ~70%   (fast feedback, cheap to write/maintain)
Integration  ~20%   (boundary correctness)
E2E          ~10%   (critical journeys only)
Contract     as needed at each external/internal service boundary, independent of the pyramid
```

b) If E2E exceeds ~15% of the scenario count, push back — ask which of them could be integration or unit instead, and name the specific assertion that requires the full stack.

c) Every **P0** scenario MUST have at least: 1 unit test (if logic exists) + integration or E2E coverage of the end-to-end effect. A P0 covered ONLY by a mocked unit test is a gap — flag it.

### 3. Update the Table

Extend the scored table with a `Level` column and a one-line `Test Idea` (preconditions → action → expected result) for every P0/P1 scenario. P2/P3 get level + a short note only.

### 4. Update WIP File

a) Write the extended table into the **Test Level Mapping** section of `{wipFile}`.

b) Update frontmatter: `stepsCompleted: [1, 2, 3]`.

### 5. Present Checkpoint Menu

Display: "**Select:** [P] Party Mode [C] Continue to Document & Register (Step 4 of 4)"

HALT and wait.

- IF P: Read fully and follow `{party_mode_exec}`, update WIP if accepted, redisplay menu.
- IF C: Verify `stepsCompleted: [1, 2, 3]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-test-design/steps/step-04-document.md`
- Other input: answer, then redisplay menu.

---

## VERIFICATION CHECKLIST:

- [ ] Every scenario has a level assigned via the decision order (not by default).
- [ ] Pyramid distribution checked, deviations justified.
- [ ] Every P0 has unit + integration/E2E coverage or a documented exception.
- [ ] `stepsCompleted: [1, 2, 3]` set.
