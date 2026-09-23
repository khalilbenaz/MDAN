---
name: 'step-03-gaps'
description: 'Rapport d''écarts, priorisation, quality gate et finalisation'
wipFile: '{implementation_artifacts}/payments-ma-compliance-review-{slug}-wip.md'
outputFile: '{implementation_artifacts}/payments-ma-compliance-review-{slug}.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 3: Rapport d'Écarts & Finalisation

**Progress: Step 3 of 3** - Dernière étape

## SÉQUENCE D'INSTRUCTIONS

### 1. Construire le rapport d'écarts (gap report)

Pour chaque item "Non conforme" ou "À vérifier" du Step 2, produire une ligne :

| Cadre | Item | Statut | Sévérité | Risque | Action recommandée | Propriétaire suggéré |
|-------|------|--------|-----------|--------|------------------------|--------------------------|
| | | Non conforme / À vérifier | Bloquant / Majeur / Mineur | | | |

Règles de sévérité :
- **Bloquant** : empêche la mise en production (ex : PAN stocké en clair, absence de traçabilité AML)
- **Majeur** : doit être corrigé avant le prochain audit/reporting réglementaire
- **Mineur** : amélioration recommandée, non bloquante

### 2. Quality Gate

- [ ] Périmètre réglementaire tranché (Step 1)
- [ ] Checklist complète, chaque item statué avec preuve si "Conforme" (Step 2)
- [ ] Rapport d'écarts avec sévérité et action pour chaque écart
- [ ] Aucun item réglementaire tranché de façon définitive sans mention "à vérifier auprès de la circulaire BAM en vigueur" ou "à faire trancher par le service juridique/conformité" quand l'incertitude existe

### 3. Finaliser

a) Copier `{wipFile}` vers `{outputFile}`, `status: 'completed'`, `stepsCompleted: [1, 2, 3]`.
b) Si `mdan_state_update` disponible : `{ workflow: "pay-compliance-review", status: "completed", artifacts: ["{outputFile}"] }`.

### 4. Rapport final

Afficher à `{user_name}` : chemin du document, nombre d'écarts par sévérité, et rappeler que ce rapport n'est pas un avis juridique définitif.

## SUCCÈS / ÉCHEC

### ✅ SUCCÈS
Tous les items statués, écarts priorisés avec action claire, aucune affirmation réglementaire présentée comme certaine sans base.

### ❌ ÉCHEC
Un item marqué "Conforme" sans preuve, ou un point réglementaire incertain tranché comme un fait établi.
