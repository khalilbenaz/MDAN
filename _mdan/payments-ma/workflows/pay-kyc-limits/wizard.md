---
name: pay-kyc-limits
description: 'Concevoir les paliers KYC et plafonds (solde, entrée/sortie mensuel, par transaction) d''un wallet marocain, les règles d''upgrade/downgrade, les points d''enforcement et les tests. Use when the user says "paliers KYC", "plafonds wallet", "design wallet limits" or "KYC tiers".'
main_config: '{project-root}/_mdan/mdan/config.yaml'
module_config: '{project-root}/_mdan/payments-ma/config.yaml'
party_mode_exec: '{project-root}/_mdan/mdan/workflows/special/party-mode/wizard.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Wizard: Paliers KYC & Plafonds Wallet (Maroc)

**Objectif :** Concevoir de bout en bout les paliers KYC d'un wallet marocain — niveau de preuve d'identité, plafonds de solde et de mouvement, règles de transition — dans le respect de la réglementation Bank Al-Maghrib (BAM) sur la monnaie électronique.

**Ton rôle :** Officier de conformité BAM collaborant avec l'utilisateur pour produire une spécification de paliers implémentable et auditable.

## RÉFÉRENCE INDICATIVE (à confirmer)

Les établissements de paiement marocains distinguent classiquement 4 paliers de wallet, avec des plafonds de solde/transaction croissants selon le niveau de KYC (identité déclarative → identité vérifiée en agence/à distance → compte bancarisé). Des ordres de grandeur souvent cités sont **1 000 / 4 000 / 20 000 / 100 000 MAD**. Ces chiffres NE DOIVENT JAMAIS être présentés comme définitifs : toujours écrire "à vérifier auprès de la circulaire BAM en vigueur" et demander à l'utilisateur de confirmer les valeurs exactes avant de figer une spec.

## ARCHITECTURE DU WIZARD

- **Step-File Architecture** : chaque step est un fichier isolé chargé Just-In-Time, jamais de saut d'étape.
- **State Tracking** : la progression est stockée dans le frontmatter du fichier WIP (`stepsCompleted`).
- **Memory** : si l'outil MCP `mdan_state_update` est disponible, l'appeler `{ workflow: "pay-kyc-limits", status: "started", step: 1 }` au démarrage, `{ step: n }` à chaque step complété, et `{ status: "completed", artifacts: [...] }` à la fin. Si l'outil est indisponible, continuer sans bloquer.

## INITIALISATION

### 1. Charger la configuration
Charger `{main_config}` (variables globales : `{user_name}`, `{communication_language}`, `{document_output_language}`) puis `{module_config}` (variables : `{default_currency}`, `{regulator}`).

### 2. État mémoire (si disponible)
Si l'outil MCP `mdan_state_update` est disponible, l'appeler avec `{ workflow: "pay-kyc-limits", status: "started", step: 1 }`.

### 3. Lancer le premier step
Lire et exécuter : `{project-root}/_mdan/payments-ma/workflows/pay-kyc-limits/steps/step-01-tiers.md`

## STEPS

| Step | Fichier | Contenu |
|------|---------|---------|
| 01 | step-01-tiers.md | Cadrage produit, définition des paliers KYC et plafonds |
| 02 | step-02-enforcement.md | Règles d'upgrade/downgrade, points d'enforcement technique |
| 03 | step-03-tests.md | Cas de test, quality gate, finalisation |

## QUALITY GATE (fin de wizard)

- [ ] Au moins 2 paliers KYC définis, chacun avec preuve d'identité requise explicite
- [ ] Plafonds de solde, d'entrée mensuelle, de sortie mensuelle et par transaction définis pour chaque palier (ou marqués "à vérifier auprès de la circulaire BAM en vigueur")
- [ ] Règles d'upgrade ET de downgrade spécifiées (déclencheur, délai, effet sur le solde en cas de dépassement du nouveau plafond)
- [ ] Points d'enforcement technique listés (où dans le code/l'architecture le plafond est vérifié)
- [ ] Au moins 5 cas de test couvrant limites nominales, dépassement, palier expiré, concurrence
- [ ] Document sauvegardé dans `{implementation_artifacts}`
