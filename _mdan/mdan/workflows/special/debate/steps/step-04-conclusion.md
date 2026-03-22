**🗣️ LANGUE OBLIGATOIRE: Tu DOIS répondre en MIX FRANÇAIS-DARIJA MAROCAINE. Exemple: "Daba ghadi nchofo..." / "Khassna ndiro..." / "Hadi hiya..."**
# Step 4: Debate Conclusion and Exit

## MANDATORY EXECUTION RULES (READ FIRST):

- ✅ YOU ARE CONCLUDING THE DEBATE with gratitude and clarity
- 🎯 PROVIDE AGENT REACTIONS to the decision (in-character)
- 📋 SUMMARIZE THE DEBATE VALUE — what was gained from the structured process
- 🔍 SUGGEST NEXT STEPS based on the decision made
- 💬 MAINTAIN POSITIVE ATMOSPHERE throughout conclusion
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

## EXECUTION PROTOCOLS:

- 🎯 Generate characteristic agent reactions to the decision
- ⚠️ Complete workflow exit after conclusion
- 💾 Update frontmatter with final workflow completion
- 📖 Suggest relevant next wizards based on the decision
- 🚫 FORBIDDEN to reopen the debate or second-guess the decision

## YOUR TASK:

Conclude the debate gracefully with agent reactions, summary, and next step suggestions.

## CONCLUSION SEQUENCE:

### 1. Agent Reactions to Decision

If a decision was made:

"⚔️ **DÉBAT TERMINÉ — RÉACTIONS** ⚔️

Les agents réagissent à la décision..."

**Winning side agent:**

"🟢/🔴 [Icon] **[Agent Name]**: [Gracious acceptance, in-character. Acknowledges it was a close debate. May highlight what to watch out for during implementation.]"

**Losing side agent:**

"🔴/🟢 [Icon] **[Agent Name]**: [Graceful acceptance, in-character. Acknowledges the decision while noting the trade-offs to monitor. Professional, not bitter.]"

**Arbitrator:**

"⚖️ [Icon] **[Agent Name]**: [Balanced reaction, notes the quality of the debate process, may suggest mitigation strategies for accepted risks.]"

If no decision was made (user exited early):

"Ma kayn ta problème! Le débat 3tak des perspectives jdad. Ila bghiti trje3 l had le sujet, la décision tqder takhodha f chi waqt akhor."

### 2. Debate Value Summary

"**📊 Résumé dial le Débat:**

| Métrique | Valeur |
|----------|--------|
| **Sujet** | [Topic] |
| **Rounds joués** | [X/3] |
| **Arguments PROPONENT** | [Count] |
| **Arguments OPPONENT** | [Count] |
| **Décision** | [Decision or 'Pas encore'] |
| **Decision Record** | [DR-XXX or 'N/A'] |
| **Confidence** | [Score or N/A] |

**Valeur ajoutée:** Had le débat structuré 3tak une vue complète men angles différents, w khedak tchouf les trade-offs qbel ma tcommiti."

### 3. Next Step Suggestions

"**Ash dir daba?**

Had la décision ghadi t'impacti le projet. Voici les options logiques:

1. **`/mdan-create-architecture`** — Ila la décision kayn fiha architecture, validi l'impact technique
2. **`/mdan-create-epics-and-stories`** — Ila bghi t'qessem le travail lli khroj men had la décision
3. **`/mdan-dev-story`** — Ila bghi tbda l'implémentation directement
4. **`/mdan-debate`** — Ila 3ndek décision khra bghiti les agents ydébatiw 3liha
5. **`/mdan-party-mode`** — Ila bghiti discussion libre m3a ga3 les agents

Kteb la commande ⬇️"

### 4. Complete Workflow Exit

**Frontmatter Update:**

```yaml
---
stepsCompleted: [1, 2, 3, 4]
workflowType: 'debate'
user_name: '{{user_name}}'
date: '{{date}}'
agents_loaded: true
debate_active: false
workflow_completed: true
decision_made: true/false
---
```

## SUCCESS METRICS:

✅ Agent reactions are in-character and graceful (both sides)
✅ Debate value summary provides clear metrics
✅ Next step suggestions are relevant to the decision
✅ Positive atmosphere maintained, no second-guessing
✅ Frontmatter properly updated with completion

## FAILURE MODES:

❌ Sore loser behavior from losing agent
❌ Reopening debate or challenging the decision
❌ Missing debate summary or metrics
❌ Not suggesting relevant next steps

## RETURN PROTOCOL:

If this workflow was invoked from within a parent workflow:

1. Identify the parent workflow step that invoked the debate
2. Re-read that file to restore context
3. Resume from where the parent workflow directed you
4. Present any menus the parent workflow requires after debate completion

Do not continue conversationally — explicitly return to parent workflow control flow.
