# MDAN Debate Protocol v3.0

## Différence avec MDAN Party Mode

| Aspect | MDAN Party Mode | MDAN Debate Protocol |
|--------|----------------|---------------------|
| Structure | Conversation libre | Protocole formel en 5 rounds |
| Déclenchement | Manuel uniquement | Auto quand conflit détecté |
| Sortie | Pas de format défini | Décision documentée dans MDAN-STATE |
| Intégration | Externe aux wizards | Intégré dans les wizards |
| Arbitrage | L'utilisateur seul | Scoring + utilisateur |

## Quand déclencher un debate

### Automatique (dans les wizards)
- Architecture wizard : choix de stack technique
- Architecture wizard : choix de patterns
- PRD wizard : priorisation des features
- Sprint planning : allocation des stories

### Manuel
- Commande `/debate {sujet}` à tout moment
- Depuis le Party Mode quand une question ne converge pas

## Protocole en 5 rounds

### Round 1 — Ouverture (chaque agent : 1 paragraphe)
Chaque agent invoqué présente sa position initiale avec justification.

### Round 2 — Challenge (chaque agent : 1 paragraphe)
Chaque agent identifie la faiblesse principale de la position adverse.

### Round 3 — Données (chaque agent : bullet points)
Chaque agent apporte des preuves concrètes (patterns, benchmarks, risques chiffrés).

### Round 4 — Synthèse (chaque agent : 1 phrase)
Chaque agent reformule sa position finale en intégrant les objections.

### Round 5 — Scoring
Le moteur attribue un score basé sur :
- Pertinence des arguments (alignement avec le PRD)
- Praticité (faisabilité dans le contexte du projet)
- Risque identifié (l'agent qui anticipe le mieux les problèmes)

### Résolution
L'utilisateur tranche. La décision est enregistrée dans MDAN-STATE :
```json
{
  "debates": [{
    "topic": "Framework frontend : React vs Vue",
    "participants": ["architect", "dev", "ux-designer"],
    "positions": {...},
    "decision": "React — pour l'écosystème et l'expertise de l'équipe",
    "decided_by": "user",
    "date": "2026-03-20"
  }]
}
```
