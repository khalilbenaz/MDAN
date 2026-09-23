---
name: 'step-01-states'
description: 'Type de flux et machine à états'
nextStepFile: './step-02-ledger.md'
templateFile: '../templates/txn-flow-template.md'
wipFile: '{implementation_artifacts}/payments-ma-txn-flow-{slug}-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 1: Type de Flux & Machine à États

**Progress: Step 1 of 4** - Next: Ledger & idempotence

## SÉQUENCE D'INSTRUCTIONS

### 1. Identifier le type de flux

Demander : lequel de ces flux (ou un autre) ?
- Cash-in (dépôt : agent, carte, virement entrant)
- Cash-out (retrait : agent, GAB, virement sortant)
- P2P (wallet à wallet, même établissement ou interopérable)
- Paiement marchand (QR code, en ligne)
- Paiement de facture (bill payment, régie/opérateur)
- Virement sortant (vers compte bancaire RIB/IBAN)

### 2. Acteurs et systèmes impliqués

Lister : initiateur, bénéficiaire, systèmes internes (wallet service, ledger), systèmes externes (switch CMI, partenaire agent, banque destinataire, opérateur facture).

### 3. Machine à états

Construire la table des états. Base minimale à adapter :

| État | Signifie | Transitions sortantes | Événement déclencheur |
|------|----------|--------------------------|---------------------------|
| `INITIATED` | Demande reçue, pas encore validée | → `PENDING_VALIDATION` ou `REJECTED` | Validation plafonds/KYC (voir workflow `pay-kyc-limits`) |
| `PENDING_VALIDATION` | Contrôles internes en cours (plafond, solde, fraude) | → `RESERVED` ou `REJECTED` | Résultat des contrôles |
| `RESERVED` | Fonds réservés côté payeur (hold), pas encore transférés | → `SETTLING` ou `EXPIRED` | Envoi vers le système externe / job interne |
| `SETTLING` | Appel externe (switch, banque, partenaire) en cours | → `COMPLETED`, `FAILED`, ou `UNKNOWN` (timeout) | Réponse externe ou timeout |
| `UNKNOWN` | Timeout sans réponse définitive | → `COMPLETED` ou `FAILED` (via requête de statut ou reversal) | Requête de statut / job de réconciliation |
| `COMPLETED` | Fonds transférés, écritures définitives | → `REVERSED` (si extourne demandée a posteriori) | - |
| `FAILED` | Échec, aucune écriture définitive OU réservation libérée | (terminal) | - |
| `REVERSED` | Extourne appliquée après un `COMPLETED` | (terminal) | Extourne manuelle ou automatique |
| `REJECTED` | Rejeté avant toute réservation de fonds | (terminal) | - |
| `EXPIRED` | Réservation expirée sans settlement | → `FAILED` (libération des fonds) | Timeout de réservation |

Adapter cette table au flux réellement choisi (retirer les états non pertinents, par ex. pas de `SETTLING` externe pour un P2P intra-wallet synchrone).

### 4. Initialiser le WIP

Copier `{templateFile}` vers `{wipFile}`, frontmatter `stepsCompleted: [1]`, remplir section "Machine à états" et "Acteurs".

### 5. Checkpoint

Afficher : "**Sélectionner :** [P] Party Mode [C] Continuer vers Ledger & idempotence (Step 2 of 4)"

HALT et attendre.

- IF P : suivre `{party_mode_exec}`, réafficher ce menu.
- IF C : mettre à jour `{wipFile}` (`stepsCompleted: [1]`), si `mdan_state_update` disponible l'appeler `{ workflow: "pay-txn-flow", step: 1 }`, puis lire fully et suivre `{nextStepFile}`.

## VÉRIFICATION

- [ ] Type de flux identifié et acteurs listés
- [ ] Machine à états complète avec au moins un état d'échec et un état d'incertitude (timeout/`UNKNOWN`)
- [ ] `{wipFile}` créé
