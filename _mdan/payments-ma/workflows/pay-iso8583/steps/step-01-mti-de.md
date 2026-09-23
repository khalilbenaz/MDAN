---
name: 'step-01-mti-de'
description: 'Cas d''usage, MTI et table de mapping des Data Elements'
nextStepFile: './step-02-responses.md'
templateFile: '../templates/iso8583-spec-template.md'
wipFile: '{implementation_artifacts}/payments-ma-iso8583-{slug}-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 1: MTI & Data Elements

**Progress: Step 1 of 3** - Next: Codes réponse, reversal & advice

## SÉQUENCE D'INSTRUCTIONS

### 1. Identifier le cas d'usage

Demander : quelle opération est concernée ? (achat carte, retrait GAB, annulation, remboursement, requête de statut/status check). Quel rôle joue le système (émetteur, acquéreur, agrégateur/switch) ?

### 2. Sélectionner la famille de MTI

Rappeler à l'utilisateur les familles courantes (voir aussi `{project-root}/_mdan/payments-ma/data/iso8583-cheatsheet.md`) :

| MTI | Nom | Usage |
|-----|-----|-------|
| 0100 / 0110 | Authorization Request / Response | Demande d'autorisation (achat, retrait) |
| 0200 / 0210 | Financial Request / Response | Transaction financière (souvent capture immédiate) |
| 0220 / 0230 | Financial Advice / Response | Notification d'une transaction déjà exécutée offline |
| 0400 / 0410 | Reversal Request / Response | Annulation d'une transaction précédente |
| 0420 / 0430 | Reversal Advice / Response | Notification d'une annulation déjà appliquée |
| 0800 / 0810 | Network Management Request / Response | Sign-on, echo test, key exchange |

### 3. Table de mapping des Data Elements (DE)

Construire la table pour CHAQUE MTI retenu. Base minimale à compléter/adapter :

| DE | Nom | Format | Obligatoire | Exemple |
|----|-----|--------|--------------|---------|
| DE2 | Primary Account Number (PAN) | LLVAR n..19 | Selon canal (masqué en log) | `520000xxxxxx0001` |
| DE3 | Processing Code | n6 | Oui | `000000` (achat) |
| DE4 | Amount, Transaction | n12 | Oui | `000000050000` (500.00) |
| DE7 | Transmission Date & Time | n10 (MMDDhhmmss) | Oui | `0923143000` |
| DE11 | STAN (System Trace Audit Number) | n6 | Oui, unique par connexion/jour | `000123` |
| DE12/DE13 | Local Time / Date | n6 / n4 | Selon profil | |
| DE22 | POS Entry Mode | n3 | Selon canal | `051` (chip) |
| DE37 | Retrieval Reference Number (RRN) | an12 | Oui, clé de corrélation métier | `609112345678` |
| DE38 | Authorization ID Response | an6 | Sur réponse succès | `A1B2C3` |
| DE39 | Response Code | an2 | Oui sur réponse | `00` |
| DE41 | Card Acceptor Terminal ID | ans8 | Oui | `TERM0001` |
| DE42 | Card Acceptor ID Code | ans15 | Oui | `MERCH000000001` |
| DE49 | Currency Code, Transaction | n3 (ISO 4217) | Oui | `504` (MAD) |
| DE90 | Original Data Elements | n42 | Sur reversal/advice | MTI+STAN+date+heure d'origine |

Adapter en ajoutant les DE spécifiques au switch/acquéreur cible (ex : DE48, DE54, DE62 propriétaires) — toujours vérifier la spec technique réelle du partenaire, ce mémo est un point de départ, pas une norme figée.

### 4. Initialiser le WIP

Copier `{templateFile}` vers `{wipFile}`, `stepsCompleted: [1]`, remplir "Cas d'usage", "MTI" et "Table DE".

### 5. Checkpoint

"**Sélectionner :** [P] Party Mode [C] Continuer vers Codes réponse, reversal & advice (Step 2 of 3)"

HALT et attendre.

- IF P : suivre `{party_mode_exec}`, réafficher.
- IF C : mettre à jour `{wipFile}`, si `mdan_state_update` disponible `{ workflow: "pay-iso8583", step: 1 }`, puis lire fully `{nextStepFile}`.

## VÉRIFICATION

- [ ] Cas d'usage et rôle système identifiés
- [ ] Au moins 1 famille de MTI (requête + réponse) documentée
- [ ] Table de DE couvrant au minimum DE2, DE3, DE4, DE7, DE11, DE37, DE39, DE41, DE42, DE49
