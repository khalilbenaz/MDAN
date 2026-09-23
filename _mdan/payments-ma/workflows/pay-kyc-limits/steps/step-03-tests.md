---
name: 'step-03-tests'
description: 'Cas de test, quality gate et finalisation du document'
wipFile: '{implementation_artifacts}/payments-ma-kyc-limits-{slug}-wip.md'
outputFile: '{implementation_artifacts}/payments-ma-kyc-limits-{slug}.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 3: Tests & Finalisation

**Progress: Step 3 of 3** - Dernière étape

## RÈGLES

- MUST NOT skip steps.
- ✅ Parler en `{communication_language}`, rédiger le document en `{document_output_language}`.

## SÉQUENCE D'INSTRUCTIONS

### 1. Générer les cas de test

Produire au minimum ces cas (adapter aux paliers réellement définis) :

| # | Cas | Palier | Attendu |
|---|-----|--------|---------|
| 1 | Cash-in exactement au plafond de solde | N | Accepté, solde = plafond |
| 2 | Cash-in dépassant le plafond de solde de 1 unité | N | Rejeté, aucune écriture partielle |
| 3 | Somme de sorties du mois atteignant le plafond mensuel puis une sortie supplémentaire | N | Les sorties ≤ plafond acceptées, la suivante rejetée |
| 4 | Deux mouvements concurrents proches du plafond (race condition) | N | Un seul accepté, l'autre rejeté proprement, pas de dépassement |
| 5 | Downgrade avec solde existant supérieur au nouveau plafond | N → N-1 | Compte non débité automatiquement ; solde gelé au-delà du nouveau plafond jusqu'à consommation, notification envoyée |
| 6 | Upgrade validé pendant qu'une transaction est en cours | N → N+1 | Le plafond appliqué à la transaction en cours est celui en vigueur au moment de l'initiation |
| 7 | Palier expiré (pièce d'identité périmée) | N | Compte rétrogradé automatiquement au palier de base, notification envoyée |

### 2. Quality Gate

Vérifier avant de finaliser :
- [ ] Au moins 2 paliers KYC définis, chacun avec preuve d'identité explicite
- [ ] Tous les plafonds soit confirmés par l'utilisateur, soit marqués "à vérifier auprès de la circulaire BAM en vigueur"
- [ ] Upgrade et downgrade tous les deux documentés
- [ ] Table des points d'enforcement complète
- [ ] Au moins 5 cas de test couvrant limite nominale, dépassement, downgrade, concurrence
- [ ] Aucune perte silencieuse d'argent en cas de downgrade

### 3. Finaliser le document

a) Copier `{wipFile}` vers `{outputFile}`.
b) Mettre à jour le frontmatter : `status: 'completed'`, `stepsCompleted: [1, 2, 3]`.
c) Si l'outil MCP `mdan_state_update` est disponible, l'appeler `{ workflow: "pay-kyc-limits", status: "completed", artifacts: ["{outputFile}"] }`.

### 4. Rapport final

Afficher à `{user_name}` :
- Chemin du document final
- Nombre de paliers définis
- Rappel : "Les plafonds marqués 'à vérifier auprès de la circulaire BAM en vigueur' doivent être validés avant mise en production."

## SUCCÈS / ÉCHEC

### ✅ SUCCÈS
- Document final écrit avec tous les paliers, règles et tests
- Aucun chiffre réglementaire présenté comme certain sans confirmation

### ❌ ÉCHEC
- Un plafond BAM inventé sans mention de vérification
- Un cas de downgrade sans traitement explicite du solde existant
