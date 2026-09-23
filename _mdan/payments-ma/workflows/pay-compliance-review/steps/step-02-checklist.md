---
name: 'step-02-checklist'
description: 'Passage de la checklist BAM/AML/CNDP/PCI'
nextStepFile: './step-03-gaps.md'
wipFile: '{implementation_artifacts}/payments-ma-compliance-review-{slug}-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 2: Checklist Réglementaire

**Progress: Step 2 of 3** - Next: Rapport d'écarts & finalisation

## SÉQUENCE D'INSTRUCTIONS

Pour chaque cadre marqué "Applicable" au Step 1, passer les items ci-dessous. Marquer chaque item **Conforme** (avec preuve : référence code/doc/contrôle), **Non conforme**, ou **À vérifier** (si la réponse dépend d'un texte réglementaire non confirmé).

### 1. BAM — Établissement de paiement / monnaie électronique

- [ ] Les paliers KYC et plafonds sont définis et documentés (voir workflow `pay-kyc-limits`)
- [ ] Les plafonds appliqués correspondent à des valeurs confirmées ou marquées "à vérifier auprès de la circulaire BAM en vigueur"
- [ ] Les points d'enforcement des plafonds sont dans le code, pas seulement dans une procédure
- [ ] Les reportings réglementaires périodiques attendus par BAM sont identifiés (à confirmer avec le service conformité)

### 2. AML/CFT (ANRF)

- [ ] Les transactions au-dessus des seuils définis déclenchent une alerte/analyse (seuils à confirmer avec conformité)
- [ ] Un mécanisme de déclaration de soupçon (DS) vers l'ANRF est identifié dans le processus (même si géré hors système)
- [ ] Les mouvements sont traçables : qui, quand, combien, vers/depuis qui
- [ ] Les listes de sanctions/PEP (personnes politiquement exposées) sont vérifiées à l'onboarding ou explicitement hors périmètre de cette feature

### 3. CNDP (loi 09-08)

- [ ] Les données personnelles collectées sont minimisées au strict nécessaire pour la finalité déclarée
- [ ] Une base légale/finalité est identifiée pour chaque catégorie de donnée collectée
- [ ] Les données sont chiffrées au repos et en transit pour les catégories sensibles (identité, données financières)
- [ ] Un mécanisme de purge/rétention est défini (durée de conservation)
- [ ] Si transfert de données hors Maroc : mécanisme de conformité identifié (à faire trancher par le service juridique)

### 4. PCI DSS (si flux carte / PAN)

- [ ] Le PAN n'est jamais stocké en clair (tokenisation ou troncature)
- [ ] Le PAN n'apparaît jamais dans les logs applicatifs
- [ ] Le scope PCI (systèmes qui touchent au PAN) est identifié et isolé du reste de l'architecture
- [ ] Les échanges contenant des données carte sont chiffrés en transit (TLS)

### 5. Mettre à jour le WIP

Ajouter la checklist remplie au `{wipFile}`, `stepsCompleted: [1, 2]`.

### 6. Checkpoint

"**Sélectionner :** [P] Party Mode [C] Continuer vers le rapport d'écarts (Step 3 of 3)"

HALT et attendre.

- IF P : suivre `{party_mode_exec}`, réafficher.
- IF C : mettre à jour `{wipFile}`, si `mdan_state_update` disponible `{ workflow: "pay-compliance-review", step: 2 }`, puis lire fully `{nextStepFile}`.

## VÉRIFICATION

- [ ] Tous les items des cadres applicables sont marqués Conforme/Non conforme/À vérifier
- [ ] Chaque item "Conforme" a une preuve citée
