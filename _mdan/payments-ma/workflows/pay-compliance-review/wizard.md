---
name: pay-compliance-review
description: 'Revue réglementaire d''une feature ou d''un PRD contre une checklist BAM/AML(ANRF)/CNDP/PCI DSS, avec rapport d''écarts (gap report). Use when the user says "revue conformité", "compliance review", "checklist BAM" or "audit réglementaire".'
main_config: '{project-root}/_mdan/mdan/config.yaml'
module_config: '{project-root}/_mdan/payments-ma/config.yaml'
party_mode_exec: '{project-root}/_mdan/mdan/workflows/special/party-mode/wizard.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Wizard: Revue de Conformité BAM/AML/CNDP/PCI

**Objectif :** Passer une feature ou un PRD au crible d'une checklist réglementaire couvrant Bank Al-Maghrib (BAM, établissements de paiement/monnaie électronique), AML/CFT (ANRF), protection des données (loi 09-08 / CNDP) et PCI DSS (si flux carte), et produire un rapport d'écarts (gap report) actionnable.

**Ton rôle :** Officier de conformité BAM. Constat factuel, jamais de verdict définitif sur un point réglementaire incertain — toujours "à vérifier auprès de la circulaire BAM en vigueur" ou "à faire trancher par le service juridique/conformité".

## ARCHITECTURE DU WIZARD

- **Step-File Architecture**, **State Tracking** dans le frontmatter WIP.
- **Memory** : si `mdan_state_update` (MCP) est disponible, l'appeler `{ workflow: "pay-compliance-review", status: "started", step: 1 }` au démarrage, `{ step: n }` à chaque step, `{ status: "completed", artifacts: [...] }` à la fin.

## INITIALISATION

### 1. Charger la configuration
Charger `{main_config}` puis `{module_config}`.

### 2. Lancer le premier step
Lire et exécuter : `{project-root}/_mdan/payments-ma/workflows/pay-compliance-review/steps/step-01-intake.md`

## STEPS

| Step | Fichier | Contenu |
|------|---------|---------|
| 01 | step-01-intake.md | Cadrage de la feature/PRD, périmètre réglementaire applicable |
| 02 | step-02-checklist.md | Passage de la checklist BAM/AML/CNDP/PCI |
| 03 | step-03-gaps.md | Rapport d'écarts, priorisation, quality gate, finalisation |

## QUALITY GATE (fin de wizard)

- [ ] Périmètre réglementaire applicable explicité (BAM oui/non, AML/CFT oui/non, CNDP oui/non, PCI DSS oui/non, et pourquoi)
- [ ] Checklist passée en entier, chaque item marqué Conforme / Non conforme / À vérifier
- [ ] Rapport d'écarts avec sévérité (bloquant / majeur / mineur) et action recommandée pour chaque écart
- [ ] Aucun item marqué "Conforme" sans justification (référence code, doc, contrôle)
