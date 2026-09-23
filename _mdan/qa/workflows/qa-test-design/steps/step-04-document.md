---
name: 'step-04-document'
description: 'Finalize the test design document and register it in the context graph'
wipFile: '{mdan_output}/test-design-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 4: Document & Register

**Progress: Step 4 of 4** - Final Step

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## CONTEXT:

- Requires the leveled table from Step 3.
- Criteria: the doc MUST meet the **READY FOR REVIEW** standard defined in `wizard.md`.

## SEQUENCE OF INSTRUCTIONS

### 1. Present Complete Test Design

Read `{wipFile}` completely, extract `slug` and `target_id` from frontmatter. Display the complete document for review.

**Present review menu:**

Display: "**Select:** [C] Continue [E] Edit [P] Party Mode"

HALT and wait.

- IF E: apply requested edits to `{wipFile}`, loop until satisfied, then redisplay menu.
- IF P: read fully and follow `{party_mode_exec}`, update if accepted, redisplay menu.
- IF C: proceed to Section 2.

### 2. Finalize

a) Update `{wipFile}` frontmatter: `status: 'ready-for-review'`, `stepsCompleted: [1, 2, 3, 4]`.

b) Rename `{wipFile}` → `{mdan_output}/test-design-{slug}.md`. Store as `finalFile`.

### 3. Register in the Context Graph

If MCP tools are available:

a) `mdan_graph_add_node { id: "test-design-{slug}", type: "artifact", path: "<relative path to finalFile>", workflow: "qa-test-design", agent: "test-architect" }`

b) For each story/epic node this design covers (use `target_id` and any per-scenario AC/requirement refs captured in Step 1), `mdan_graph_add_edge { source: "test-design-{slug}", target: "<story-or-requirement-node-id>", relation: "derived_from" }`. If a referenced node doesn't exist yet in the graph, add it first with `mdan_graph_add_node { id, type: "artifact" }` (path optional) so the edge has a valid target.

c) `mdan_state_update { workflow: "qa-test-design", action: "complete", artifacts: ["{finalFile}"] }`.

If MCP tools are unavailable, tell the user which node/edge calls they should run once tools are connected — do not silently skip registration without telling them.

### 4. Present Final Menu

```
**Test Design Complete!**

Saved to: {finalFile}
Registered in context graph as: test-design-{slug}

Priorities: {p0_count} P0, {p1_count} P1, {p2_count} P2, {p3_count} P3
Level mix: {unit_pct}% unit / {integration_pct}% integration / {e2e_pct}% E2E / {contract_count} contract

---

**Next Steps:**

[T] qa-atdd — generate the failing acceptance tests for the P0/P1 scenarios now
[X] qa-traceability — fold this design into the requirements traceability matrix
[D] Done — exit workflow
[P] Party Mode — get expert feedback
```

HALT and wait.

- IF T: tell the user to run the `qa-atdd` workflow, passing `{finalFile}` as input.
- IF X: tell the user to run the `qa-traceability` workflow, passing `{finalFile}` as input.
- IF P: read fully and follow `{party_mode_exec}`, redisplay menu after.
- IF D: exit — display final confirmation and path.

---

## REQUIRED OUTPUTS:

- MUST update status to `ready-for-review` and rename file to `test-design-{slug}.md`.
- MUST register the node (and edges) in the context graph when MCP tools are available.

## VERIFICATION CHECKLIST:

- [ ] Complete design presented for review.
- [ ] `stepsCompleted: [1, 2, 3, 4]` set and file renamed.
- [ ] Node registered with `derived_from` edges to every covered story/requirement.
