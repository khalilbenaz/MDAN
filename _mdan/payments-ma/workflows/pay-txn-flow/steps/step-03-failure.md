---
name: 'step-03-failure'
description: 'Timeouts, reversal/extourne, notifications, outbox'
nextStepFile: './step-04-tests.md'
wipFile: '{implementation_artifacts}/payments-ma-txn-flow-{slug}-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 3: Échecs, Timeouts, Reversal & Outbox

**Progress: Step 3 of 4** - Next: Tests & finalisation

## SÉQUENCE D'INSTRUCTIONS

### 1. Timeouts sur appels externes

Pour chaque appel externe identifié au Step 1 (switch, banque, partenaire), documenter :
- Timeout technique (ex : 30s) ET timeout métier (délai après lequel on considère l'opération incertaine, ex : 5 min sans callback)
- Action à l'expiration : passer en état `UNKNOWN`, déclencher une requête de statut (status inquiry, ex : équivalent ISO 8583 DE 24 = 0100/reversal, ou webhook de statut partenaire)
- Politique par défaut si le statut reste indéterminé après N tentatives : **ne jamais assumer succès par défaut** ; documenter si le défaut est "considérer échoué et rembourser" ou "escalader en revue manuelle" selon le flux.

### 2. Reversal / Extourne

- **Extourne système** (automatique, ex : timeout confirmé échoué après réservation) : préciser le déclencheur, le délai, le job responsable.
- **Extourne métier** (a posteriori, ex : réclamation client, chargeback partenaire) : préciser le processus (voir workflow `pay-recon` pour le rapprochement), qui autorise, quelles données sont exigées (référence originale, motif).
- Dans les deux cas : l'extourne est une **nouvelle écriture miroir**, jamais une modification de l'écriture d'origine (cf. Step 2). Le mouvement original reste consultable.
- Préciser le marqueur utilisé pour distinguer un mouvement normal d'une extourne dans le système (ex : type de mouvement `EXT`, référence croisée vers le `RequestId`/`ReferenceId` d'origine).

### 3. Notifications

Pour chaque état terminal, préciser : canal (push, SMS, email), contenu minimal (montant, référence, statut), délai cible.

### 4. Pattern Outbox

- Toute notification externe ou événement à publier (vers un topic, un webhook, un système de notification) est écrit dans une table `outbox` **dans la même transaction DB** que l'écriture comptable.
- Un worker séparé lit l'`outbox` et publie, avec retry et idempotence côté consommateur (le message peut être livré plus d'une fois).
- Ne jamais appeler un système externe (notification, event bus) directement dans le handler qui écrit le ledger : si l'appel échoue après le commit, l'état devient incohérent sans le pattern outbox.

### 5. Mettre à jour le WIP

Ajouter "Timeouts", "Reversal/Extourne", "Notifications", "Outbox" au `{wipFile}`, `stepsCompleted: [1, 2, 3]`.

### 6. Checkpoint

Afficher : "**Sélectionner :** [P] Party Mode [C] Continuer vers Tests & finalisation (Step 4 of 4)"

HALT et attendre.

- IF P : suivre `{party_mode_exec}`, réafficher ce menu.
- IF C : mettre à jour `{wipFile}`, si `mdan_state_update` disponible l'appeler `{ workflow: "pay-txn-flow", step: 3 }`, puis lire fully et suivre `{nextStepFile}`.

## VÉRIFICATION

- [ ] Timeout technique ET métier définis pour chaque appel externe
- [ ] État `UNKNOWN`/incertain traité sans hypothèse de succès par défaut
- [ ] Extourne modélisée comme écriture miroir, jamais comme modification
- [ ] Pattern outbox appliqué pour toute notification/événement externe
