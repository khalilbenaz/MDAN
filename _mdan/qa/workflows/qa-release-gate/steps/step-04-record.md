---
name: 'step-04-record'
description: 'Finalize the release decision record and register it in the context graph'
wipFile: '{mdan_output}/release-gate-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 4: Record & Register

**Progress: Step 4 of 4** - Final Step

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 1. Finalize the Document

a) Read `{wipFile}` completely, extract `slug` and `release_scope`.

b) Update `{wipFile}` frontmatter: `status: 'decided'`, `stepsCompleted: [1, 2, 3, 4]`.

c) Rename `{wipFile}` → `{mdan_output}/release-decision-{slug}.md`. Store as `finalFile`.

### 2. Create the Decision Record

If MCP tools are available, call `mdan_create_decision_record` with the outcome (`PASS`/`CONCERNS`/`FAIL`), the justification, and `impacts` set to the ids of every artifact node this decision covers (test-design, traceability, NFR, ci-gates nodes collected in Step 1). This makes the release decision itself a queryable graph node — a future `qa-release-gate` run, or `mdan_graph_impact` on any of these artifacts, will surface it.

If `mdan_create_decision_record` is unavailable, fall back to:

a) `mdan_graph_add_node { id: "release-decision-{slug}", type: "decision", path: "<finalFile relative path>", workflow: "qa-release-gate", agent: "test-architect" }`

b) For each covered artifact, `mdan_graph_add_edge { source: "release-decision-{slug}", target: "<artifact-node-id>", relation: "references" }`.

### 3. Close Out State Tracking

If MCP tools are available, call `mdan_state_update { workflow: "qa-release-gate", action: "complete", artifacts: ["{finalFile}"] }`.

### 4. Final Message

```
**Release Gate Decision: {gate_decision}**

Scope: {release_scope}
Saved to: {finalFile}
Registered as a Decision Record in the context graph.

{if FAIL: "DO NOT SHIP. Blocking items: {list}."}
{if CONCERNS: "Shippable with acknowledged, documented risk: {list}. Get explicit sign-off from {user_name} or the release owner before shipping."}
{if PASS: "Cleared to ship. All aggregated artifacts current and verified, no blocking defects."}
```

HALT — this is the terminal step. Do not auto-continue into any other workflow.

---

## REQUIRED OUTPUTS:

- MUST finalize the decision document and rename it.
- MUST register (or attempt to register) the decision as a graph node, preferring `mdan_create_decision_record`.

## VERIFICATION CHECKLIST:

- [ ] `stepsCompleted: [1, 2, 3, 4]` set and file renamed.
- [ ] Decision registered in the context graph (or the user told explicitly it wasn't, and why).
- [ ] Final message states unambiguously: ship, ship-with-risk, or do-not-ship.
