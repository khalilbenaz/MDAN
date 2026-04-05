# Turn Protocol — Structured Speaking Turns

## Purpose

Ensures orderly multi-agent communication with clear turn boundaries, preventing agents from talking over each other or monopolizing the conversation.

## Protocol Rules

### Turn Structure

Each turn consists of:
1. **Speaker identification**: Icon + Name + Role
2. **Turn type**: What kind of contribution this is
3. **Content**: The actual contribution (bounded by constraints)
4. **Turn marker**: Signal that the turn is complete

### Turn Format

```
[TURN: {speaker} | {role} | {type}]

{Icon} **{Agent Name}** ({role}):

{Content — max 150 words for arguments, max 50 words for reactions}

[/TURN]
```

### Turn Types

| Type | Description | Word Limit | Used In |
|------|-------------|------------|---------|
| `proposition` | Initial argument for a position | 150 | Debate Round 1 |
| `rebuttal` | Direct response to opposing argument | 150 | Debate Round 2 |
| `counter` | Final counter-argument | 150 | Debate Round 3 |
| `ruling` | Arbitrator's decision | 200 | Debate Arbitration |
| `position` | Agent's stance on topic | 100 | Consensus Phase 1 |
| `concession` | What agent is willing to give up | 75 | Consensus Phase 3 |
| `synthesis` | Merged position | 200 | Consensus Phase 4 |
| `reaction` | Quick response or agreement | 50 | Discussion |
| `question` | Question to user or another agent | 50 | Any mode |

### Turn Order

**Debate Mode:**
1. Proponent → Opponent → Arbitrator (per round)
2. Strict rotation, no interruptions
3. Arbitrator always speaks last in each round

**Consensus Mode:**
1. Agents speak in order of relevance to current sub-topic
2. Facilitator may reorder based on who has most to contribute
3. All agents must speak in each phase

**Discussion Mode:**
1. Most relevant agent speaks first
2. Others react or build on points
3. Natural flow with facilitator guidance

### Constraints

- No agent may speak twice consecutively (except arbitrator summarizing)
- Each turn must be self-contained (no "as I was saying...")
- Questions to the user ALWAYS end the current round
- Agents must reference at least one other agent's point when rebutting
- Topic drift triggers facilitator intervention after 2 off-topic turns

### Turn Markers for LLM

When generating multi-agent responses, use these internal markers:

```
<!-- TURN_START: agent="{name}" role="{role}" type="{type}" -->
{content}
<!-- TURN_END -->
```

These markers help maintain structure but are NOT shown to the user.


## Communication Rules — MANDATORY

- Ultra-concise. No filler, no preamble, no pleasantries.
- Never say "happy to help", "sure!", "great question", "let me", or similar.
- Tool first, talk second. Act before explaining.
- Result first. Lead with outcome, not process.
- Stop when done. No summary, no recap, no trailing commentary.
- No politeness wrappers. Direct and blunt.
- Minimum words. If one word works, do not use ten.
- No unsolicited explanations.
- No emoji unless asked.
