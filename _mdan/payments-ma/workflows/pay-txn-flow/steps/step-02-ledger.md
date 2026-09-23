---
name: 'step-02-ledger'
description: 'Écritures double entrée, idempotence et frais'
nextStepFile: './step-03-failure.md'
wipFile: '{implementation_artifacts}/payments-ma-txn-flow-{slug}-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 2: Ledger, Idempotence & Frais

**Progress: Step 2 of 4** - Next: Échecs, reversal & outbox

## SÉQUENCE D'INSTRUCTIONS

### 1. Écritures en double entrée

Pour le cas nominal (état `COMPLETED`), produire la table des écritures. Exemple pour un cash-in de 500 {default_currency} avec 5 {default_currency} de frais :

| Compte | Débit | Crédit | Commentaire |
|--------|-------|--------|-------------|
| Compte de suspens / canal cash-in | 500 | | Entrée de fonds externe |
| Wallet du client | | 495 | Crédité net des frais |
| Compte revenus frais | | 5 | Frais perçus |

Répéter pour chaque état terminal pertinent : `COMPLETED`, `FAILED` (si des fonds avaient été réservés, préciser l'écriture de libération), `REVERSED` (écriture miroir de l'écriture nominale, jamais une suppression/modification de l'écriture originale).

**Règle d'or :** aucune écriture n'est jamais éditée ou supprimée après commit ; une correction est toujours une nouvelle écriture (extourne = écriture inverse), pour garder un historique auditable.

### 2. Clé d'idempotence

Définir :
- **Composition** : par ex. `hash(initiator_id, flow_type, amount, external_reference, client_request_id)` ou un `Idempotency-Key` fourni par le client émetteur.
- **Portée** : unique par (établissement, type de flux, fenêtre de temps) ou globale ?
- **Durée de vie** : combien de temps la clé est-elle retenue pour détecter un replay (ex : 24h à 7 jours selon le flux) ?
- **Comportement sur collision** : retourner le résultat de la première exécution (même statut, même payload), jamais ré-exécuter le mouvement.

### 3. Frais

- Qui paie (payeur, bénéficiaire, partagé) ?
- Le frais est-il prélevé à l'initiation (réservé avec le montant) ou au settlement ?
- En cas d'extourne : le frais est-il remboursé ? Politique à documenter explicitement (ex : frais non remboursables si le service a été rendu, remboursables si erreur système).

### 4. Mettre à jour le WIP

Ajouter les sections "Écritures comptables", "Idempotence", "Frais" au `{wipFile}`, `stepsCompleted: [1, 2]`.

### 5. Checkpoint

Afficher : "**Sélectionner :** [P] Party Mode [C] Continuer vers Échecs, reversal & outbox (Step 3 of 4)"

HALT et attendre.

- IF P : suivre `{party_mode_exec}`, réafficher ce menu.
- IF C : mettre à jour `{wipFile}`, si `mdan_state_update` disponible l'appeler `{ workflow: "pay-txn-flow", step: 2 }`, puis lire fully et suivre `{nextStepFile}`.

## VÉRIFICATION

- [ ] Écritures en double entrée pour au moins 3 états terminaux (COMPLETED, FAILED avec fonds réservés, REVERSED)
- [ ] Clé d'idempotence avec composition, portée et durée de vie définies
- [ ] Politique de frais en cas d'extourne explicitée
