# Agent Sidecar Template

## Purpose

Agent sidecars provide persistent memory for each agent across Party Mode sessions.
They accumulate observations, preferences, and learned context.

## Storage Location

`{project-root}/_mdan/state/sidecars/{agent-name}.sidecar.json`

## Schema

```json
{
  "agent": "agent-name",
  "displayName": "Agent Display Name",
  "created_at": "ISO date",
  "last_updated": "ISO date",
  "sessions_participated": 0,
  "memories": [
    {
      "type": "observation|preference|context|decision",
      "content": "What the agent observed or learned",
      "source_session": "session-id or date",
      "confidence": 0.8
    }
  ],
  "relationships": {
    "agrees_with": ["agent-names the agent often aligns with"],
    "disagrees_with": ["agent-names the agent often opposes"],
    "complements": ["agent-names that provide complementary expertise"]
  },
  "decision_history": [
    {
      "dr_id": "DR-001",
      "role": "proponent|opponent|arbitrator|participant",
      "position": "Brief summary of their position",
      "outcome": "won|lost|compromised"
    }
  ]
}
```

## Loading Protocol

When Party Mode starts with sidecar-enabled agents:
1. Check if `_mdan/state/sidecars/{agent-name}.sidecar.json` exists
2. If yes, load and inject into agent context: "Your persistent memory from previous sessions: [memories]"
3. If no, create new empty sidecar

## Saving Protocol

When Party Mode exits:
1. For each participating agent, update their sidecar:
   - Increment `sessions_participated`
   - Add new observations from this session
   - Update `relationships` based on interactions
   - Add any decision history entries
   - Update `last_updated`
2. Save to `_mdan/state/sidecars/{agent-name}.sidecar.json`

## Memory Types

- **observation**: Something the agent noticed about the project or discussion
- **preference**: A preference the agent has developed (e.g., "prefers microservices over monolith")
- **context**: Project-specific context the agent should remember
- **decision**: A decision the agent participated in and its outcome
