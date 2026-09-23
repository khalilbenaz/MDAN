# How to: customize an agent

Every agent (persona, principles, menu) can be adjusted without touching the shipped source file, in three layers merged in order — later wins:

1. **shipped** — `_mdan/_config/agents/<module>-<agent>.customize.yaml`, the template that ships with the agent.
2. **team** — `_mdan/custom/<agent>.yaml`, versioned (commit it, your team shares it).
3. **user** — `_mdan/custom/<agent>.user.yaml`, git-ignored (`_mdan/custom/.gitignore`), personal to you.

The merge is a deep merge: arrays are concatenated (without duplicating identical entries), objects merge key by key, and an empty value in a later layer never erases a value from an earlier one. Reinstalling or updating MDAN never touches `_mdan/custom/`.

## Via MCP

```
mdan_customize_agent {
  agent: "architect",
  layer: "team",
  communication_style: "Direct, no hedging, always propose two options",
  principles: ["Prefer boring technology"],
  memories: ["This project targets Azure, not AWS"]
}
```

Fields you can set: `displayName`, `communication_style`, `principles[]`, `critical_actions[]` (run right after the agent activates), `memories[]` (permanent facts, distinct from the decaying memory sidecars — see [concepts](../explanation/concepts.md#agent-memory-sidecars)), and `menu[]` (each entry: `trigger`, `description`, `exec` or `workflow`).

The change applies the next time the agent is loaded (`mdan_consult_agent`, a `/mdan-agent-*` slash command, or party mode) — no rebuild needed.

## By hand

Write YAML directly to `_mdan/custom/<agent>.yaml` (team) or `_mdan/custom/<agent>.user.yaml` (personal), following the same shape MDAN would generate. Example — make the architect agent push back harder on scope:

```yaml
# _mdan/custom/architect.yaml
persona:
  principles:
    - "Push back on scope creep in every architecture review"
menu:
  - trigger: "threat-model"
    description: "Run a quick STRIDE pass on the current design"
    workflow: "qa-nfr-assessment"
```

## Layer precedence example

If the shipped template sets `communication_style: "Balanced, pragmatic"` and your team layer sets `communication_style: "Direct, no hedging"`, the agent uses the team value. If you then add a personal layer with a different style, yours wins for you only — teammates without that file still see the team style.
