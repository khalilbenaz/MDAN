---
name: 'step-04-gate-decision'
description: 'Issue the PASS/CONCERNS/FAIL coverage gate decision and register the matrix in the context graph'
wipFile: '{mdan_output}/traceability-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 4: Gate Decision & Register

**Progress: Step 4 of 4** - Final Step

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 1. Apply the Gate Formula

- **FAIL**: at least one **Blocking** gap exists (P0/P1 requirement uncovered, or a security/compliance/data-integrity NFR uncovered).
- **CONCERNS**: no Blocking gaps, but one or more **Notable** gaps exist, or Blocking gaps exist with a documented, user-approved waiver (waiver must name who approved it and why).
- **PASS**: no Blocking or Notable gaps. Minor gaps are recorded but do not block.

### 2. Present the Decision

Present the full matrix + gap list + decision. Display: "**Select:** [C] Continue [E] Edit [W] Waive a blocking gap [P] Party Mode"

HALT and wait.

- IF E: apply edits, redisplay.
- IF W: ask for the gap id, the approver, and the reason; record it in the **Waivers** section; recompute the decision; redisplay.
- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: proceed.

### 3. Finalize

a) Update `{wipFile}` frontmatter: `status: 'gated'`, `gate_decision: 'PASS'|'CONCERNS'|'FAIL'`, `stepsCompleted: [1, 2, 3, 4]`.

b) Rename `{wipFile}` → `{mdan_output}/traceability-{slug}.md`. Store as `finalFile`.

### 4. Register in the Context Graph

If MCP tools are available:

a) `mdan_graph_add_node { id: "traceability-{slug}", type: "artifact", path: "<finalFile relative path>", workflow: "qa-traceability", agent: "test-architect" }`

b) For each requirement/story node referenced, `mdan_graph_add_edge { source: "traceability-{slug}", target: "<node-id>", relation: "references" }`.

c) `mdan_state_update { workflow: "qa-traceability", action: "complete", artifacts: ["{finalFile}"] }`.

### 5. Final Message

```
**Traceability Matrix Complete — Gate: {gate_decision}**

Saved to: {finalFile}
{requirement_count} requirements | {covered_count} covered | {partial_count} partial | {uncovered_count} uncovered
Blocking gaps: {blocking_count} | Notable: {notable_count} | Minor: {minor_count}

{if FAIL: "Do not ship until Blocking gaps are resolved or explicitly waived."}
{if CONCERNS: "Shippable with acknowledged risk — review the Notable gaps before deciding."}
{if PASS: "Coverage supports a release decision. Run qa-release-gate next to aggregate with NFR/test-design/defects."}
```

---

## REQUIRED OUTPUTS:

- MUST issue an explicit PASS/CONCERNS/FAIL decision with reasoning.
- MUST register the node in the context graph when MCP tools are available.

## VERIFICATION CHECKLIST:

- [ ] Gate formula applied exactly (no Blocking gap ignored without a recorded waiver).
- [ ] `stepsCompleted: [1, 2, 3, 4]` set, file renamed, node registered.
