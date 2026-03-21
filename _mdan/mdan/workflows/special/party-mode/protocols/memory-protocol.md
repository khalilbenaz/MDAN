# Memory Protocol — Agent Memory Accumulation

## Purpose

Defines how agent sidecars accumulate memory across Party Mode sessions, creating persistent context that makes future sessions more informed and contextual.

## Memory Lifecycle

### 1. Session Start — Memory Loading

When Party Mode initializes:

```
FOR each participating agent:
  IF sidecar file exists:
    LOAD sidecar from _mdan/state/sidecars/{agent-name}.sidecar.json
    INJECT into agent context:
      "📝 Your memories from previous sessions:"
      FOR each memory in sidecar.memories (last 10):
        "- [{type}] {content} (confidence: {confidence})"
      "🤝 Relationship notes:"
      FOR each relationship type:
        "{type}: {agent-names}"
  ELSE:
    CREATE empty sidecar structure
    NOTE: "First session for this agent — no prior memories"
```

### 2. During Session — Memory Collection

Automatically identify memory-worthy moments:

**Triggers for new memories:**
- Agent makes a strong argument that wins a debate → `observation`
- Agent discovers a project constraint → `context`
- Agent expresses a clear preference → `preference`
- A decision is reached → `decision`
- Agent explicitly agrees/disagrees with another → update `relationships`

**Memory format:**
```json
{
  "type": "observation|preference|context|decision",
  "content": "Concise description (max 100 chars)",
  "source_session": "ISO date of current session",
  "confidence": 0.5-1.0
}
```

**Confidence scoring:**
- 1.0: Explicit decision or stated fact
- 0.8: Strong argument that went unchallenged
- 0.6: Observation from discussion
- 0.5: Inference or assumption

### 3. Session End — Memory Persistence

When Party Mode exits gracefully:

```
FOR each participating agent:
  UPDATE sidecar:
    INCREMENT sessions_participated
    SET last_updated = now()

    ADD new memories from this session (max 5 per session)
    IF total memories > 50:
      PRUNE lowest confidence memories to keep 50

    UPDATE relationships:
      IF agent agreed with another agent 2+ times → add to agrees_with
      IF agent disagreed with another agent 2+ times → add to disagrees_with
      IF agents' expertise complemented each other → add to complements

    ADD decision_history entries for any decisions this session

  SAVE to _mdan/state/sidecars/{agent-name}.sidecar.json
```

### 4. Memory Decay

Memories lose confidence over time:
- After 5 sessions without reinforcement: confidence -= 0.1
- Below 0.3 confidence: memory is pruned
- Explicitly referenced memories get confidence boost (+0.1)

### 5. Cross-Session Context

When an agent's sidecar contains relevant context for the current discussion:
- The facilitator may prompt: "{Agent}, based on your experience from previous sessions..."
- This allows natural integration of persistent memory into conversation

## Integration with MDAN-STATE

After saving sidecars, update `_mdan/state/MDAN-STATE.json`:
```json
{
  "agent_sidecars": {
    "{agent-name}": {
      "path": "_mdan/state/sidecars/{agent-name}.sidecar.json",
      "last_updated": "ISO date",
      "memory_count": 15,
      "sessions": 3
    }
  }
}
```
