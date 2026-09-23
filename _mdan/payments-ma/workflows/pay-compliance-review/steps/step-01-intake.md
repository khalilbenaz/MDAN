---
name: 'step-01-intake'
description: 'Cadrage de la feature/PRD et périmètre réglementaire applicable'
nextStepFile: './step-02-checklist.md'
templateFile: '../templates/compliance-review-template.md'
wipFile: '{implementation_artifacts}/payments-ma-compliance-review-{slug}-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 1: Cadrage & Périmètre Réglementaire

**Progress: Step 1 of 3** - Next: Passage de la checklist

## SÉQUENCE D'INSTRUCTIONS

### 1. Obtenir la feature/PRD à revoir

Demander à l'utilisateur de fournir ou décrire la feature/PRD (fonctionnalité, flux d'argent concerné, données personnelles traitées, présence de flux carte).

### 2. Déterminer le périmètre réglementaire applicable

| Cadre | Applicable si... |
|-------|---------------------|
| BAM (établissement de paiement / monnaie électronique) | La feature touche l'émission de monnaie électronique, un wallet, un plafond, l'agrément d'un partenaire |
| AML/CFT (ANRF) | La feature implique un mouvement de fonds identifiable à un client (quasi toujours pour un produit de paiement) |
| CNDP (loi 09-08) | La feature collecte, stocke ou transmet des données à caractère personnel (identité, coordonnées, données de transaction) |
| PCI DSS | La feature manipule, stocke ou transmet un PAN (numéro de carte) ou des données sensibles associées |

Pour chaque cadre, noter Applicable / Non applicable avec une justification courte.

### 3. Initialiser le WIP

Copier `{templateFile}` vers `{wipFile}`, `stepsCompleted: [1]`, remplir "Feature/PRD" et "Périmètre réglementaire".

### 4. Checkpoint

"**Sélectionner :** [P] Party Mode [C] Continuer vers la checklist (Step 2 of 3)"

HALT et attendre.

- IF P : suivre `{party_mode_exec}`, réafficher.
- IF C : mettre à jour `{wipFile}`, si `mdan_state_update` disponible `{ workflow: "pay-compliance-review", step: 1 }`, puis lire fully `{nextStepFile}`.

## VÉRIFICATION

- [ ] Feature/PRD résumée
- [ ] Les 4 cadres (BAM, AML/CFT, CNDP, PCI DSS) tranchés Applicable/Non applicable avec justification
