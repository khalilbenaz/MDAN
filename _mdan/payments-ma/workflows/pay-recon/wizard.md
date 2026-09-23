---
name: pay-recon
description: 'Concevoir un rapprochement de fin de journée (EOD) entre le ledger core, le switch et les fichiers partenaires : sources, règles de matching, catégories d''écart, auto-résolution, reporting. Use when the user says "rapprochement EOD", "reconciliation design", "EOD reconciliation" or "règles de matching".'
main_config: '{project-root}/_mdan/mdan/config.yaml'
module_config: '{project-root}/_mdan/payments-ma/config.yaml'
party_mode_exec: '{project-root}/_mdan/mdan/workflows/special/party-mode/wizard.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Wizard: Rapprochement EOD (End of Day)

**Objectif :** Concevoir un rapprochement de fin de journée entre le grand livre interne (core ledger), le fichier du switch/acquéreur et les fichiers partenaires (agents, banques, opérateurs), avec des règles de matching, une classification des écarts (breaks), une stratégie d'auto-résolution et un reporting exploitable.

**Ton rôle :** Responsable rapprochement & règlement, factuelle, orientée preuve chiffrée.

## ARCHITECTURE DU WIZARD

- **Step-File Architecture**, **State Tracking** dans le frontmatter WIP.
- **Memory** : si `mdan_state_update` (MCP) est disponible, l'appeler `{ workflow: "pay-recon", status: "started", step: 1 }` au démarrage, `{ step: n }` à chaque step, `{ status: "completed", artifacts: [...] }` à la fin.

## INITIALISATION

### 1. Charger la configuration
Charger `{main_config}` puis `{module_config}`.

### 2. Lancer le premier step
Lire et exécuter : `{project-root}/_mdan/payments-ma/workflows/pay-recon/steps/step-01-sources.md`

## STEPS

| Step | Fichier | Contenu |
|------|---------|---------|
| 01 | step-01-sources.md | Sources à rapprocher, clés de matching |
| 02 | step-02-breaks.md | Catégories d'écart, stratégie d'auto-résolution |
| 03 | step-03-reporting.md | Reporting, quality gate, finalisation |

## QUALITY GATE (fin de wizard)

- [ ] Au moins 3 sources identifiées (ledger core, switch, partenaire) avec format de chaque fichier/flux
- [ ] Clé(s) de matching définie(s) et testée(s) sur un cas d'ambiguïté (ex : montant identique, référence différente)
- [ ] Au moins 4 catégories d'écart avec règle de traitement (auto-résolu vs revue manuelle)
- [ ] Statuts ambigus (timeout, code d'erreur générique) explicitement classés "à investiguer", jamais par défaut "réussi" ou "échoué"
- [ ] Reporting avec au moins : nombre d'opérations rapprochées, montant total des écarts, âge des écarts ouverts
