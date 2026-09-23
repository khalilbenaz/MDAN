---
name: 'step-02-breaks'
description: 'Catégories d''écart et stratégie d''auto-résolution'
nextStepFile: './step-03-reporting.md'
wipFile: '{implementation_artifacts}/payments-ma-recon-{slug}-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 2: Catégories d'Écart & Auto-résolution

**Progress: Step 2 of 3** - Next: Reporting & finalisation

## SÉQUENCE D'INSTRUCTIONS

### 1. Catégoriser les écarts (breaks)

Table de référence à adapter aux sources réelles :

| Catégorie | Description | Cause typique | Traitement |
|-----------|--------------|------------------|-------------|
| Présent core, absent switch | Écriture interne sans confirmation externe | Timeout non réconcilié, statut jamais reçu | Revue manuelle : vérifier auprès du partenaire avant d'extourner |
| Présent switch, absent core | Opération confirmée côté réseau mais jamais écrite en interne | Bug applicatif, message perdu | Priorité haute : créer l'écriture manquante après vérification, risque de perte de revenu/service non facturé |
| Montant différent | Même référence, montants différents entre sources | Frais non alignés, arrondi, double frais | Revue manuelle avec règle de tolérance documentée |
| Statut ambigu (ex : code 502/timeout/erreur générique) | Le partenaire ne confirme ni succès ni échec net | Panne réseau, erreur technique partenaire | **Ne jamais classer par défaut réussi ou échoué** : catégorie "à investiguer", avec délai de résolution cible |
| Doublon apparent | Deux entrées qui matchent la même clé de secours | Vraie duplication technique OU deux opérations légitimes proches | Vérifier via une clé plus fine avant toute action |
| Extourne non reflétée | Une extourne existe sur une source mais pas sur l'autre | Timing de traitement, job d'extourne en échec | Revue manuelle prioritaire (impact client direct) |

### 2. Stratégie d'auto-résolution

Pour chaque catégorie, définir : est-elle **auto-résolvable** (règle déterministe, ex : écart de montant = frais connu et documenté) ou **doit-elle aller en revue manuelle** ?

- Documenter les règles d'auto-résolution comme du code : condition exacte, action exacte, log de traçabilité de la résolution automatique (jamais de correction automatique silencieuse sans log).
- Toute résolution automatique qui touche à l'argent (extourne, ré-écriture) doit être **rejouable** et **traçable** : script/job identifié, date, montant, référence.

### 3. SLA de résolution

Définir un délai cible par catégorie (ex : "présent switch absent core" = J+1 max, "statut ambigu" = J+3 max avant escalade).

### 4. Mettre à jour le WIP

Ajouter "Catégories d'écart" et "Auto-résolution" au `{wipFile}`, `stepsCompleted: [1, 2]`.

### 5. Checkpoint

"**Sélectionner :** [P] Party Mode [C] Continuer vers Reporting & finalisation (Step 3 of 3)"

HALT et attendre.

- IF P : suivre `{party_mode_exec}`, réafficher.
- IF C : mettre à jour `{wipFile}`, si `mdan_state_update` disponible `{ workflow: "pay-recon", step: 2 }`, puis lire fully `{nextStepFile}`.

## VÉRIFICATION

- [ ] Au moins 4 catégories d'écart définies
- [ ] Chaque catégorie a une décision explicite auto-résolution vs revue manuelle
- [ ] Aucun statut ambigu classé par défaut comme réussi ou échoué
- [ ] SLA de résolution par catégorie
