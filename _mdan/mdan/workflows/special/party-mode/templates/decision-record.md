# Decision Record Template

## Schema

A Decision Record captures the outcome of a structured Debate or Consensus session.

### JSON Format

```json
{
  "id": "DR-XXX",
  "topic": "The question or decision being addressed",
  "mode": "debate|consensus",
  "participants": {
    "proponent": { "name": "agent-name", "displayName": "Name", "icon": "emoji" },
    "opponent": { "name": "agent-name", "displayName": "Name", "icon": "emoji" },
    "arbitrator": { "name": "agent-name", "displayName": "Name", "icon": "emoji" }
  },
  "rounds": [
    {
      "round": 1,
      "speaker": "agent-name",
      "role": "proponent|opponent|arbitrator|participant",
      "type": "proposition|rebuttal|counter|position|concession|synthesis",
      "content": "The argument or position text"
    }
  ],
  "decision": "Clear statement of the final decision",
  "rationale": "Why this decision was reached",
  "confidence": 0.85,
  "dissent": "Summary of dissenting opinion, if any",
  "date": "ISO date string",
  "registered_in_graph": true,
  "graph_node_id": "dr-xxx"
}
```

### Markdown Output Format

When presenting to the user:

```
## 📋 Decision Record: {{id}}

**Date:** {{date}}
**Mode:** {{mode}}
**Topic:** {{topic}}

### Participants
{{#each participants}}
- {{icon}} **{{displayName}}** ({{role}})
{{/each}}

### Debate Rounds
{{#each rounds}}
**Round {{round}} — {{speaker}} ({{type}}):**
{{content}}
{{/each}}

### Decision
{{decision}}

### Rationale
{{rationale}}

### Confidence: {{confidence}}

### Dissent
{{dissent}}
```

### ID Assignment

Decision Record IDs are sequential: DR-001, DR-002, etc.
To determine the next ID:
1. Scan `{project-root}/mdan_output/decisions/` for existing DR-*.json files
2. Find the highest number
3. Increment by 1
4. If no existing records, start at DR-001
