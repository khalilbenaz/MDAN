---
name: 'step-03-report'
description: 'Produce the prioritized remediation report and register it in the context graph'
wipFile: '{mdan_output}/test-review-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 3: Report & Remediation

**Progress: Step 3 of 3** - Final Step

## RULES:

- MUST NOT skip steps.
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## SEQUENCE OF INSTRUCTIONS

### 1. Compute the Overall Score

Sum the 5 dimension scores (max 20). Band it:

| Total | Band |
|---|---|
| 17-20 | Excellent — maintain, spot-check periodically |
| 12-16 | Good — targeted fixes needed, not urgent |
| 7-11 | At Risk — schedule remediation this sprint, suite is actively costing velocity/trust |
| 0-6 | Failing — treat as tech debt with an owner and deadline; consider blocking new feature work on the worst offenders |

### 2. Prioritize Remediation

Rank remediation items by: (a) tests covering P0/P1 risk that also scored low (fix first — these are load-bearing and unreliable), (b) flaky tests with a diagnosed cause (cheap, high-value fixes), (c) everything else. Each item: `Test/file | Dimension(s) failed | Root cause | Suggested fix | Priority`.

### 3. Present and Confirm

Display the full report. "**Select:** [C] Continue [E] Edit [P] Party Mode"

HALT and wait.

- IF E: apply edits, redisplay.
- IF P: read and follow `{party_mode_exec}`, redisplay after.
- IF C: proceed.

### 4. Finalize

a) Update `{wipFile}` frontmatter: `status: 'reviewed'`, `overall_score: '{total}/20'`, `stepsCompleted: [1, 2, 3]`.

b) Rename `{wipFile}` → `{mdan_output}/test-review-{slug}.md`. Store as `finalFile`.

### 5. Register in the Context Graph

If MCP tools are available:

a) `mdan_graph_add_node { id: "test-review-{slug}", type: "artifact", path: "<finalFile relative path>", workflow: "qa-test-review", agent: "test-architect" }`

b) If the review covered tests linked to a known story/test-design node, `mdan_graph_add_edge { source: "test-review-{slug}", target: "<node-id>", relation: "references" }`.

c) `mdan_state_update { workflow: "qa-test-review", action: "complete", artifacts: ["{finalFile}"] }`.

### 6. Final Message

```
**Test Review Complete — Score: {total}/20 ({band})**

Saved to: {finalFile}
Top remediation priorities:
{top_3_items}

{total_flaky_count} flaky tests diagnosed. See report for root causes and fixes.
```

---

## REQUIRED OUTPUTS:

- MUST produce a banded overall score and a prioritized remediation list.
- MUST register the node when MCP tools are available.

## VERIFICATION CHECKLIST:

- [ ] Overall score computed and banded.
- [ ] Remediation list prioritized by risk, not just alphabetically/by file.
- [ ] `stepsCompleted: [1, 2, 3]` set, file renamed, node registered.
