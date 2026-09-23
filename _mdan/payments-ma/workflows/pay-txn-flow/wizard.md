---
name: pay-txn-flow
description: 'Concevoir un flux de mouvement d''argent (cash-in, cash-out, P2P, paiement marchand, facture, virement) : états, écritures en double entrée, idempotency keys, timeouts, reversal/extourne, frais, notifications, outbox. Use when the user says "flux de paiement", "design payment flow", "cash-in cash-out" or "transaction flow".'
main_config: '{project-root}/_mdan/mdan/config.yaml'
module_config: '{project-root}/_mdan/payments-ma/config.yaml'
party_mode_exec: '{project-root}/_mdan/mdan/workflows/special/party-mode/wizard.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Wizard: Flux de Mouvement d'Argent

**Objectif :** Spécifier un flux de paiement (cash-in, cash-out, P2P, paiement marchand, paiement de facture, virement sortant) de façon implémentable : machine à états, écritures comptables en double entrée, clé d'idempotence, gestion des timeouts, chemin de reversal/extourne, frais, notifications et publication d'événements via le pattern outbox.

**Ton rôle :** Architecte systèmes de paiement collaborant avec l'utilisateur pour produire une spec de flux complète et testable.

## ARCHITECTURE DU WIZARD

- **Step-File Architecture** : un step = un fichier, chargé Just-In-Time, jamais de saut.
- **State Tracking** : progression dans le frontmatter du fichier WIP.
- **Memory** : si `mdan_state_update` (MCP) est disponible, l'appeler `{ workflow: "pay-txn-flow", status: "started", step: 1 }` au démarrage, `{ step: n }` à chaque step, `{ status: "completed", artifacts: [...] }` à la fin. Sinon continuer sans bloquer.

## INITIALISATION

### 1. Charger la configuration
Charger `{main_config}` (`{user_name}`, `{communication_language}`, `{document_output_language}`, `{implementation_artifacts}`) puis `{module_config}` (`{default_currency}`, `{regulator}`).

### 2. État mémoire (si disponible)
Si `mdan_state_update` est disponible, l'appeler `{ workflow: "pay-txn-flow", status: "started", step: 1 }`.

### 3. Lancer le premier step
Lire et exécuter : `{project-root}/_mdan/payments-ma/workflows/pay-txn-flow/steps/step-01-states.md`

## STEPS

| Step | Fichier | Contenu |
|------|---------|---------|
| 01 | step-01-states.md | Type de flux, machine à états, acteurs |
| 02 | step-02-ledger.md | Écritures double entrée, idempotence, frais |
| 03 | step-03-failure.md | Timeouts, reversal/extourne, notifications, outbox |
| 04 | step-04-tests.md | Cas de test, quality gate, finalisation |

## QUALITY GATE (fin de wizard)

- [ ] Machine à états complète (états + transitions + événements déclencheurs)
- [ ] Écritures en double entrée pour le cas nominal ET pour chaque cas d'échec/reversal
- [ ] Clé d'idempotence définie (composition, portée, durée de vie)
- [ ] Chemin de timeout et de reversal/extourne documenté pour chaque appel externe
- [ ] Frais modélisés (qui paie, quand, réversible ou non en cas d'extourne)
- [ ] Publication d'événements via outbox (pas d'appel externe dans la transaction DB)
- [ ] Au moins 6 cas de test couvrant nominal, timeout, duplication, extourne partielle
