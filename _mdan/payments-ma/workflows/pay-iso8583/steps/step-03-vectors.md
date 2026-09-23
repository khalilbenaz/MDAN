---
name: 'step-03-vectors'
description: 'Vecteurs de test, quality gate et finalisation'
wipFile: '{implementation_artifacts}/payments-ma-iso8583-{slug}-wip.md'
outputFile: '{implementation_artifacts}/payments-ma-iso8583-{slug}.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 3: Vecteurs de Test & Finalisation

**Progress: Step 3 of 3** - Dernière étape

## SÉQUENCE D'INSTRUCTIONS

### 1. Générer les vecteurs de test

Pour chaque vecteur, préciser MTI, DE clés (DE3, DE4, DE11, DE37, DE39) et le comportement système attendu :

| # | Scénario | MTI | DE39 attendu | Comportement système |
|---|----------|-----|----------------|---------------------------|
| 1 | Achat approuvé | 0200 → 0210 | 00 | Capture, écriture ledger, notification |
| 2 | Achat refusé (fonds insuffisants) | 0200 → 0210 | 51 | Aucune écriture, notification d'échec |
| 3 | Timeout sur la réponse, puis reversal envoyé | 0200 (pas de réponse) → 0400 → 0410 | - / 00 | État `UNKNOWN` interne, reversal émis, réservation libérée après confirmation |
| 4 | Reversal advice reçu pour une transaction déjà connue | 0420 → 0430 | 00 | Annulation appliquée même si déjà traitée localement, jamais rejetée |
| 5 | Rejeu du même message (même STAN + RRN) | 0200 (dupliqué) | 00 (identique) | Réponse renvoyée à l'identique, aucun second débit |
| 6 | Message reçu avec un DE obligatoire manquant | 0200 | - | Rejet protocolaire avant tout traitement métier, log d'erreur de format |

### 2. Quality Gate

- [ ] MTI et table DE complètes (Step 1)
- [ ] Codes réponse + reversal/advice traités (Step 2)
- [ ] Idempotence protocolaire (STAN/RRN) documentée (Step 2)
- [ ] Au moins 4 vecteurs de test incluant succès, refus, timeout+reversal, duplication

### 3. Finaliser

a) Copier `{wipFile}` vers `{outputFile}`, `status: 'completed'`, `stepsCompleted: [1, 2, 3]`.
b) Si `mdan_state_update` disponible : `{ workflow: "pay-iso8583", status: "completed", artifacts: ["{outputFile}"] }`.

### 4. Rapport final

Afficher à `{user_name}` le chemin du document et rappeler : "Cette spec s'appuie sur un mémo ISO 8583 générique — toujours confirmer les DE propriétaires et les codes réponse exacts avec la spécification technique du switch/acquéreur cible avant intégration."

## SUCCÈS / ÉCHEC

### ✅ SUCCÈS
Table DE complète, reversal/advice non rejetés silencieusement, vecteurs de test couvrant le nominal et l'incertain.

### ❌ ÉCHEC
Absence de gestion du timeout/reversal, ou code `91`/`96` traité comme un refus définitif au lieu d'un statut incertain.
