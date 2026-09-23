---
name: 'step-03-reporting'
description: 'Reporting, quality gate et finalisation'
wipFile: '{implementation_artifacts}/payments-ma-recon-{slug}-wip.md'
outputFile: '{implementation_artifacts}/payments-ma-recon-{slug}.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 3: Reporting & Finalisation

**Progress: Step 3 of 3** - Dernière étape

## SÉQUENCE D'INSTRUCTIONS

### 1. Définir le reporting

Le rapport EOD doit contenir au minimum :

| Métrique | Détail |
|----------|--------|
| Volume rapproché | Nombre d'opérations matchées avec succès / total |
| Taux de matching | % d'opérations rapprochées automatiquement |
| Montant total des écarts | Somme des écarts ouverts, par catégorie |
| Âge des écarts ouverts | Distribution (J, J+1, J+2, > SLA) |
| Écarts résolus automatiquement | Nombre + montant, avec référence des règles appliquées |
| Écarts en revue manuelle | Nombre + montant + propriétaire assigné |
| Tendance | Comparaison au jour précédent / à la moyenne mobile 7 jours |

Préciser le destinataire de ce rapport (ops, conformité, direction financière) et sa fréquence (quotidien à J+1 matin typiquement).

### 2. Quality Gate

- [ ] Sources et clés de matching définies (Step 1)
- [ ] Catégories d'écart avec décision auto vs manuel (Step 2)
- [ ] Aucun statut ambigu résolu par défaut (Step 2)
- [ ] Reporting avec métriques ci-dessus

### 3. Finaliser

a) Copier `{wipFile}` vers `{outputFile}`, `status: 'completed'`, `stepsCompleted: [1, 2, 3]`.
b) Si `mdan_state_update` disponible : `{ workflow: "pay-recon", status: "completed", artifacts: ["{outputFile}"] }`.

### 4. Rapport final

Afficher à `{user_name}` le chemin du document et un résumé (nombre de sources, nombre de catégories d'écart, SLA).

## SUCCÈS / ÉCHEC

### ✅ SUCCÈS
Toutes les catégories d'écart ont une décision explicite, le reporting est actionnable, aucun cas ambigu n'est résolu par hypothèse.

### ❌ ÉCHEC
Un statut ambigu (timeout, code générique) classé par défaut comme réussi ou échoué sans revue.
