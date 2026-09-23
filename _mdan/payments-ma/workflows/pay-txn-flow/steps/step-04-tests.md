---
name: 'step-04-tests'
description: 'Cas de test, quality gate et finalisation'
wipFile: '{implementation_artifacts}/payments-ma-txn-flow-{slug}-wip.md'
outputFile: '{implementation_artifacts}/payments-ma-txn-flow-{slug}.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 4: Tests & Finalisation

**Progress: Step 4 of 4** - Dernière étape

## SÉQUENCE D'INSTRUCTIONS

### 1. Générer les cas de test

| # | Cas | Attendu |
|---|-----|---------|
| 1 | Flux nominal complet | État final `COMPLETED`, écritures correctes, notification envoyée |
| 2 | Timeout sur l'appel externe, puis callback tardif "succès" | Réconciliation détecte le succès tardif, transition `UNKNOWN → COMPLETED`, pas de double crédit |
| 3 | Timeout sur l'appel externe, puis callback tardif "échec" | `UNKNOWN → FAILED`, réservation libérée |
| 4 | Retry client avec la même clé d'idempotence après succès | Retourne le résultat original, aucune nouvelle écriture |
| 5 | Retry client avec la même clé d'idempotence pendant que le premier appel est encore `SETTLING` | Le retry attend/retourne l'état courant, ne déclenche pas un second appel externe |
| 6 | Extourne demandée sur une opération `COMPLETED` | Écriture miroir créée, solde correct, opération originale toujours consultable, marqueur d'extourne posé |
| 7 | Deux mouvements concurrents qui consomment le même solde | Un seul passe si le solde ne suffit pas pour les deux, pas de solde négatif |

### 2. Quality Gate

- [ ] Machine à états complète (Step 1)
- [ ] Écritures double entrée pour au moins 3 états terminaux (Step 2)
- [ ] Idempotence définie avec composition/portée/durée de vie (Step 2)
- [ ] Timeout + reversal/extourne documentés (Step 3)
- [ ] Pattern outbox appliqué (Step 3)
- [ ] Au moins 6 cas de test incluant timeout, retry et extourne

### 3. Finaliser

a) Copier `{wipFile}` vers `{outputFile}`, `status: 'completed'`, `stepsCompleted: [1, 2, 3, 4]`.
b) Si `mdan_state_update` disponible : `{ workflow: "pay-txn-flow", status: "completed", artifacts: ["{outputFile}"] }`.

### 4. Rapport final

Afficher à `{user_name}` le chemin du document final et un résumé (type de flux, nombre d'états, nombre de cas de test).

## SUCCÈS / ÉCHEC

### ✅ SUCCÈS
Document complet, aucune écriture comptable jamais éditée/supprimée dans la spec, timeout et extourne couverts.

### ❌ ÉCHEC
Absence de gestion du timeout, appel externe dans la même transaction que l'écriture DB (violation du pattern outbox), ou extourne modélisée comme modification de l'écriture d'origine.
