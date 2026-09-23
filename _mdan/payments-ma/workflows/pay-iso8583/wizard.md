---
name: pay-iso8583
description: 'Spécifier une interface ISO 8583 avec un switch (CMI/GSIMT ou acquéreur) : MTI, table de mapping des Data Elements, codes réponse, gestion reversal/advice, vecteurs de test. Use when the user says "ISO 8583", "interface switch carte", "DE mapping" or "spec switch".'
main_config: '{project-root}/_mdan/mdan/config.yaml'
module_config: '{project-root}/_mdan/payments-ma/config.yaml'
party_mode_exec: '{project-root}/_mdan/mdan/workflows/special/party-mode/wizard.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Wizard: Spécification d'Interface ISO 8583

**Objectif :** Spécifier une interface ISO 8583 avec un switch/acquéreur (ex : CMI, GSIMT) pour un ou plusieurs types d'opérations carte (achat, retrait, annulation, remboursement) : MTI utilisés, table de mapping des Data Elements (DE), codes réponse attendus, gestion des reversal/advice, et vecteurs de test.

**Ton rôle :** Architecte systèmes de paiement, précis sur le protocole. Se référer à `{project-root}/_mdan/payments-ma/data/iso8583-cheatsheet.md` comme mémo, sans jamais le considérer comme une source normative complète (toujours vérifier la spécification du switch/acquéreur cible).

## ARCHITECTURE DU WIZARD

- **Step-File Architecture**, **State Tracking** dans le frontmatter WIP.
- **Memory** : si `mdan_state_update` (MCP) est disponible, l'appeler `{ workflow: "pay-iso8583", status: "started", step: 1 }` au démarrage, `{ step: n }` à chaque step, `{ status: "completed", artifacts: [...] }` à la fin.

## INITIALISATION

### 1. Charger la configuration
Charger `{main_config}` puis `{module_config}`.

### 2. Charger le mémo ISO 8583
Lire `{project-root}/_mdan/payments-ma/data/iso8583-cheatsheet.md` pour rappel des MTI/DE/codes réponse courants.

### 3. Lancer le premier step
Lire et exécuter : `{project-root}/_mdan/payments-ma/workflows/pay-iso8583/steps/step-01-mti-de.md`

## STEPS

| Step | Fichier | Contenu |
|------|---------|---------|
| 01 | step-01-mti-de.md | Cas d'usage, MTI utilisés, table de mapping des DE |
| 02 | step-02-responses.md | Codes réponse, reversal, advice |
| 03 | step-03-vectors.md | Vecteurs de test, quality gate, finalisation |

## QUALITY GATE (fin de wizard)

- [ ] Au moins 1 famille de MTI documentée (ex : 0100/0110, 0200/0210, 0400/0410, 0420/0430)
- [ ] Table de mapping des DE avec au minimum : DE2, DE3, DE4, DE7, DE11, DE37, DE38, DE39, DE41, DE42, DE49
- [ ] Codes réponse (DE39) documentés avec au moins succès + 3 refus courants
- [ ] Reversal (0400/0420) et advice traités séparément du flux nominal
- [ ] Au moins 4 vecteurs de test (succès, refus, timeout+reversal, duplication STAN)
