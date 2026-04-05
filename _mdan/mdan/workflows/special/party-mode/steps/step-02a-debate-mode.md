**🗣️ LANGUE OBLIGATOIRE: Tu DOIS répondre en MIX FRANÇAIS-DARIJA MAROCAINE. Exemple: "Daba ghadi nchofo..." / "Khassna ndiro..." / "Hadi hiya..."**
# Step 2A: Debate Mode — Structured Argumentation

## MANDATORY EXECUTION RULES (READ FIRST):

- ✅ DEBATE MODE requires exactly 3 roles: PROPONENT, OPPONENT, ARBITRATOR
- 🎯 FOLLOW the structured round protocol strictly
- 📋 PRODUCE a Decision Record at the end
- 🔍 REGISTER the decision in the Context Graph if available
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style

## DEBATE STRUCTURE:

### 1. Debate Setup

**Select participants based on topic relevance:**

- **Proponent** 🟢: Agent best suited to ARGUE FOR the position
- **Opponent** 🔴: Agent best suited to ARGUE AGAINST or present alternatives
- **Arbitrator** ⚖️: Agent with broadest perspective to judge (default: mdan-master)

**Present setup to user:**
"⚔️ **DEBATE MODE ACTIVATED**

**Topic:** {{topic}}

**Participants:**
- 🟢 **Proponent:** [Icon] [Agent Name] — Will argue FOR
- 🔴 **Opponent:** [Icon] [Agent Name] — Will argue AGAINST/present alternatives
- ⚖️ **Arbitrator:** [Icon] [Agent Name] — Will judge and decide

**Debate Format:** 3 rounds maximum, then arbitration

[C] Start the debate | [X] Change participants"

### 2. Round Protocol

Execute rounds following `../protocols/turn-protocol.md`:

**Round 1 — Opening Statements:**
- 🟢 Proponent presents their position (max 3 key arguments)
- 🔴 Opponent presents counter-position (max 3 key arguments)
- ⚖️ Arbitrator summarizes both positions, identifies key points of contention

**Round 2 — Rebuttal:**
- 🟢 Proponent rebuts opponent's arguments directly
- 🔴 Opponent rebuts proponent's arguments directly
- ⚖️ Arbitrator identifies where arguments converge or remain contested

**Round 3 — Final Arguments:**
- 🟢 Proponent makes final case, addressing remaining objections
- 🔴 Opponent makes final case, addressing remaining objections
- ⚖️ Arbitrator prepares ruling

**After each round, present:**
"📊 **Round {{n}} Complete**
[C] Continue to next round | [J] Jump to arbitration | [U] User input"

### 3. Arbitration

The Arbitrator delivers a structured ruling:

"⚖️ **ARBITRATION — [Arbitrator Name]**

**Decision:** [Clear statement of the decision]

**Rationale:**
1. [Key reasoning point 1]
2. [Key reasoning point 2]
3. [Key reasoning point 3]

**Confidence:** [High/Medium/Low] ([0-1 score])

**Dissent:** [Summary of the losing side's strongest unresolved argument]

**Conditions/Caveats:** [Any conditions on the decision]"

### 4. Decision Record Generation

Generate a Decision Record following `../templates/decision-record.md`:

- Auto-assign next DR-XXX ID
- Capture all rounds, arguments, and the arbitration
- Calculate confidence score based on argument strength and consensus
- Note any dissenting opinion

**Save Decision Record to:** `{project-root}/mdan_output/decisions/{{DR-ID}}.json`

### 5. Context Graph Registration

If context graph is available (`_mdan/state/context-graph.json`):
- Add decision as node (type: "decision")
- Link to input artifacts that triggered the debate (relation: "derived_from")
- Link to downstream artifacts the decision impacts (relation: "impacts")

### 6. Post-Debate Options

"✅ **Debate Complete — Decision Record {{DR-ID}} saved**

[D] Start another debate | [S] Switch to Discussion mode | [N] Switch to Consensus mode | [E] Exit Party Mode"

## SUCCESS METRICS:
✅ Three-role debate structure maintained throughout
✅ Structured rounds followed in order
✅ Decision Record generated with all required fields
✅ Context Graph updated if available
✅ Each agent stayed fully in character

## FAILURE MODES:
❌ Agents breaking character or role-switching mid-debate
❌ Skipping rounds or not following protocol
❌ No Decision Record produced
❌ Generic arguments not grounded in agent expertise


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
