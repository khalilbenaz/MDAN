---
name: 'step-03-link-graph'
description: 'Finalize the acceptance test set and link it to the story node in the context graph'
wipFile: '{mdan_output}/atdd-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 3: Link & Register

**Progress: Step 3 of 3** - Final Step

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 1. Present the Complete Set

Read `{wipFile}` completely, extract `slug` and `story_id`. Present the full list of generated tests with their AC tags for final review.

Display: "**Select:** [C] Continue [E] Edit [P] Party Mode"

HALT and wait.

- IF E: apply edits, loop until satisfied, redisplay menu.
- IF P: read and follow `{party_mode_exec}`, redisplay menu after.
- IF C: proceed.

### 2. Finalize

a) Update `{wipFile}` frontmatter: `status: 'ready-for-dev'`, `stepsCompleted: [1, 2, 3]`.

b) Rename `{wipFile}` → `{mdan_output}/atdd-{slug}.md`. Store as `finalFile`.

### 3. Register in the Context Graph

If MCP tools are available:

a) `mdan_graph_add_node { id: "atdd-{slug}", type: "artifact", path: "<finalFile relative path>", workflow: "qa-atdd", agent: "test-architect" }`

b) `mdan_graph_add_edge { source: "atdd-{slug}", target: "{story_id}", relation: "derived_from" }` — the acceptance tests are derived from the story's ACs. If `{story_id}` isn't yet a graph node, add it first.

c) `mdan_state_update { workflow: "qa-atdd", action: "complete", artifacts: ["{finalFile}"] }`.

If unavailable, tell the user the exact calls to run later.

### 4. Final Message

```
**ATDD Set Complete!**

{test_count} failing acceptance tests generated for {story_id}, saved at: {finalFile}
Registered as: atdd-{slug} (derived_from {story_id})

Hand this to implementation: the story is done when every one of these tests passes
and no existing test regresses. Do not modify the tests to make them pass — modify the code.
```

---

## REQUIRED OUTPUTS:

- MUST update status to `ready-for-dev` and rename to `atdd-{slug}.md`.
- MUST register node + `derived_from` edge to the story when MCP tools are available.

## VERIFICATION CHECKLIST:

- [ ] `stepsCompleted: [1, 2, 3]` set and file renamed.
- [ ] Node registered and linked to the story node.
