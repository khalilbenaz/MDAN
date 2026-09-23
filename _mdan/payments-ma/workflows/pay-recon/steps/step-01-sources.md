---
name: 'step-01-sources'
description: 'Sources à rapprocher et clés de matching'
nextStepFile: './step-02-breaks.md'
templateFile: '../templates/recon-template.md'
wipFile: '{implementation_artifacts}/payments-ma-recon-{slug}-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 1: Sources & Clés de Matching

**Progress: Step 1 of 3** - Next: Catégories d'écart & auto-résolution

## SÉQUENCE D'INSTRUCTIONS

### 1. Identifier les sources

Au minimum 3 sources typiques d'un rapprochement EOD pour un établissement de paiement marocain :

| Source | Nature | Format typique | Fréquence |
|--------|--------|------------------|-----------|
| Ledger core | Vérité interne, écritures comptables du système | Extraction DB / vue dédiée | Continu, snapshot EOD |
| Switch (CMI/GSIMT) ou acquéreur | Transactions carte traitées côté réseau | Fichier plat / CSV EOD | Quotidien |
| Partenaire (agent, banque, opérateur facture) | Opérations exécutées côté tiers | Fichier plat, API, ou table de statuts | Quotidien ou temps réel |

Demander à l'utilisateur de préciser les sources réelles de son système, leur format exact, et surtout **quelle source fait foi** pour quel type de donnée (ex : montant = core, statut carte = switch).

### 2. Définir la ou les clés de matching

- **Clé primaire** : ex. référence unique (RRN, ReferenceId, ou identifiant de transaction commun aux 3 sources)
- **Clé de secours** : si la référence n'est pas fiable entre systèmes, définir une clé composite (montant + date + identifiant compte/carte + fenêtre de temps)
- **Tolérances** : préciser la tolérance de montant (normalement 0, sauf frais arrondis documentés) et la fenêtre de temps acceptée entre les timestamps des différentes sources

### 3. Cas d'ambiguïté à traiter explicitement

- Deux opérations de même montant, même jour, sur le même compte, avec des références différentes entre sources → comment les distinguer sans mismatcher ?
- Une opération présente sur une source mais absente sur une autre — dans quel sens est-ce anormal (ex : présente au switch mais absente au core = risque de perte de revenu ; présente au core mais absente au switch = risque de double engagement) ?

### 4. Initialiser le WIP

Copier `{templateFile}` vers `{wipFile}`, `stepsCompleted: [1]`, remplir "Sources" et "Clés de matching".

### 5. Checkpoint

"**Sélectionner :** [P] Party Mode [C] Continuer vers Catégories d'écart & auto-résolution (Step 2 of 3)"

HALT et attendre.

- IF P : suivre `{party_mode_exec}`, réafficher.
- IF C : mettre à jour `{wipFile}`, si `mdan_state_update` disponible `{ workflow: "pay-recon", step: 1 }`, puis lire fully `{nextStepFile}`.

## VÉRIFICATION

- [ ] Au moins 3 sources identifiées avec la source qui fait foi par type de donnée
- [ ] Clé(s) de matching primaire et de secours définies avec tolérances explicites
- [ ] Au moins 2 cas d'ambiguïté traités
