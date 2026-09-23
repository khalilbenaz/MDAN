---
name: 'step-01-tiers'
description: 'Cadrage produit et définition des paliers KYC + plafonds'
nextStepFile: './step-02-enforcement.md'
templateFile: '../templates/kyc-limits-template.md'
wipFile: '{implementation_artifacts}/payments-ma-kyc-limits-{slug}-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 1: Paliers KYC & Plafonds

**Progress: Step 1 of 3** - Next: Enforcement & Upgrade/Downgrade

## RÈGLES

- MUST NOT skip steps ni sauter en avant.
- MUST vérifier tout chiffre réglementaire (plafond, seuil) : s'il n'est pas confirmé par l'utilisateur ou une source citée, écrire "à vérifier auprès de la circulaire BAM en vigueur".
- ✅ Parler en `{communication_language}`, rédiger le document en `{document_output_language}`.

## SÉQUENCE D'INSTRUCTIONS

### 0. Reprise de travail en cours

a) Vérifier si un fichier WIP `{implementation_artifacts}/payments-ma-kyc-limits-*-wip.md` existe déjà pour ce projet.
b) Si oui, proposer de reprendre à l'étape indiquée dans `stepsCompleted`, sinon continuer.

### 1. Cadrer le produit

Demander à l'utilisateur :
- Quel produit ? (wallet grand public, wallet marchand, compte de paiement)
- Combien de paliers KYC souhaite-t-il (typiquement 2 à 4) ?
- Quel canal d'onboarding par palier (déclaratif app, agence physique, e-KYC à distance, compte bancaire lié) ?

### 2. Table des paliers (référence de départ)

Présenter cette table de référence INDICATIVE et demander à l'utilisateur de la confirmer ou l'ajuster — jamais l'affirmer comme un fait réglementaire figé :

| Palier | Preuve d'identité | Plafond solde | Plafond entrée/mois | Plafond sortie/mois | Plafond par transaction |
|--------|--------------------|----------------|----------------------|-----------------------|---------------------------|
| 1 (déclaratif) | Numéro de téléphone + déclaration | 1 000 MAD* | 1 000 MAD* | 1 000 MAD* | 500 MAD* |
| 2 (identité de base) | CIN scannée, non vérifiée en agence | 4 000 MAD* | 4 000 MAD* | 4 000 MAD* | 2 000 MAD* |
| 3 (identité vérifiée) | CIN vérifiée en agence ou e-KYC avec liveness | 20 000 MAD* | 20 000 MAD* | 20 000 MAD* | 10 000 MAD* |
| 4 (bancarisé) | Compte bancaire lié (RIB/IBAN vérifié) | 100 000 MAD* | 100 000 MAD* | 100 000 MAD* | 50 000 MAD* |

`*` = valeur indicative à vérifier auprès de la circulaire BAM en vigueur ; ne jamais livrer une spec finale sans confirmation explicite de l'utilisateur ou citation d'une source.

### 3. Capturer les décisions

Pour chaque palier retenu, capturer :
- **Nom / code interne** du palier
- **Preuve d'identité requise** (document, canal, niveau de vérification)
- **Plafond de solde instantané**
- **Plafond d'entrée mensuel** (cash-in + réception P2P + crédits marchands)
- **Plafond de sortie mensuel** (cash-out + P2P sortant + paiements marchands + factures)
- **Plafond par transaction unitaire**
- **Devise** : `{default_currency}` sauf indication contraire

### 4. Initialiser le fichier WIP

a) Copier le template depuis `{templateFile}`.
b) Écrire dans `{wipFile}` avec le frontmatter :
   ```yaml
   ---
   title: 'Paliers KYC - {product_name}'
   slug: '{slug}'
   created: '{date}'
   status: 'in-progress'
   stepsCompleted: [1]
   tiers: []
   ---
   ```
c) Remplir la section "Paliers" avec les décisions capturées à l'étape 3.

### 5. Checkpoint

Afficher : "**Sélectionner :** [P] Party Mode [C] Continuer vers Enforcement & Upgrade/Downgrade (Step 2 of 3)"

HALT et attendre la sélection utilisateur.

- IF P : lire et suivre `{party_mode_exec}`, puis réafficher ce menu.
- IF C : mettre à jour `stepsCompleted` à `[1]` dans `{wipFile}`, si `mdan_state_update` disponible l'appeler `{ workflow: "pay-kyc-limits", step: 1 }`, puis lire fully et suivre `{nextStepFile}`.

## VÉRIFICATION

- [ ] Au moins 2 paliers capturés avec preuve d'identité explicite
- [ ] Chaque plafond marqué "à vérifier auprès de la circulaire BAM en vigueur" si non confirmé par l'utilisateur
- [ ] `{wipFile}` créé avec `stepsCompleted: [1]`
