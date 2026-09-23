---
name: 'step-02-stale-check'
description: 'Use the context graph to find artifacts downstream of changed specs that were not re-verified'
wipFile: '{mdan_output}/release-gate-wip.md'
nextStepFile: './step-03-decision.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 2: Staleness Check (MDAN's Differentiator)

**Progress: Step 2 of 4** - Next: Decision

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## CONTEXT:

- This is the step generic release checklists cannot do: MDAN's context graph tracks which artifacts derive from which specs, so a spec change that nobody re-verified downstream is caught automatically instead of relying on someone remembering.

## SEQUENCE OF INSTRUCTIONS

### 1. Run the Staleness Query

If MCP tools are available, call `mdan_graph_stale`. It returns every artifact whose source file changed since it was registered, and the downstream nodes that depend on it and therefore need review.

If MCP tools are NOT available, tell the user explicitly: "Staleness check skipped — MCP tools unavailable. This is a real gap: I cannot verify whether any of {list the artifacts collected in Step 1} still reflect the current specs. Confirm manually or connect MCP before trusting this gate." Record this as a limitation in the WIP file and proceed with what's known.

### 2. Classify Each Stale Result

For each `(changed, stale)` pair returned:

- If the stale downstream artifact is one of this release's aggregated artifacts (test-design/traceability/NFR/test-review from Step 1) → **Blocking** until re-verified: the artifact's PASS verdict cannot be trusted as-is.
- If the stale artifact is out of this release's scope → note it but don't block (flag for a future release gate).

### 3. Decide Re-verification Path

For each Blocking stale item, present options to the user:

- **[R] Re-run** the relevant qa-* workflow now (test-design/traceability/nfr-assessment) to re-verify against the changed spec.
- **[W] Waive** with a named approver and reason (e.g. "spec change was cosmetic wording only, confirmed by {approver}").

Resolve every Blocking item before moving on — do not silently carry an unresolved staleness item into the decision step.

### 4. Update WIP File

a) Write the staleness findings + resolutions into the **Staleness Check** section of `{wipFile}`.

b) Update frontmatter: `stepsCompleted: [1, 2]`.

### 5. Checkpoint Menu

Display: "**Select:** [P] Party Mode [C] Continue to Decision (Step 3 of 4)"

HALT and wait.

- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: verify `stepsCompleted: [1, 2]`, then read fully and follow: `{project-root}/_mdan/qa/workflows/qa-release-gate/steps/step-03-decision.md`
- Other: answer, redisplay.

---

## VERIFICATION CHECKLIST:

- [ ] `mdan_graph_stale` run (or its absence explicitly flagged as a limitation).
- [ ] Every Blocking stale item resolved (re-verified or waived with approver+reason) before proceeding.
- [ ] `stepsCompleted: [1, 2]` set.
