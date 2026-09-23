---
name: 'step-02-enforcement'
description: 'Règles upgrade/downgrade et points d''enforcement technique'
nextStepFile: './step-03-tests.md'
wipFile: '{implementation_artifacts}/payments-ma-kyc-limits-{slug}-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 2: Enforcement, Upgrade & Downgrade

**Progress: Step 2 of 3** - Next: Tests & finalisation

## RÈGLES

- MUST NOT skip steps.
- MUST s'appuyer sur les paliers capturés au Step 1 (déjà en mémoire).
- ✅ Parler en `{communication_language}`, rédiger le document en `{document_output_language}`.

## SÉQUENCE D'INSTRUCTIONS

### 1. Règles d'upgrade (montée de palier)

Pour chaque transition de palier N → N+1, capturer :
- **Déclencheur** : action utilisateur (soumission CIN, rendez-vous agence, liaison RIB) ou automatique (score de confiance)
- **Validation** : qui/quoi valide (agent back-office, service e-KYC tiers, règle automatique) et le délai cible (SLA)
- **Effet immédiat** : le nouveau plafond s'applique-t-il instantanément ou après validation asynchrone ? Que se passe-t-il pour les transactions en cours pendant la transition ?
- **Traçabilité** : quel événement/log doit être écrit pour l'audit BAM/ANRF (qui a validé, quand, sur quelle pièce)

### 2. Règles de downgrade (perte de palier)

Capturer, pour chaque cas :
- **Déclencheur** : expiration de pièce d'identité, détection de fraude, décision de conformité, inactivité prolongée
- **Effet sur le solde existant** : si le solde dépasse le nouveau plafond, le compte est-il gelé, le surplus est-il bloqué (non retirable tant que non consommé), ou un remboursement est-il déclenché ? — **ne jamais permettre une perte silencieuse d'argent client**
- **Notification** : canal et délai de préavis à l'utilisateur avant application

### 3. Points d'enforcement technique

Lister, avec le composant concerné :

| Point de contrôle | Composant | Ce qui est vérifié | Comportement si dépassement |
|--------------------|-----------|----------------------|-------------------------------|
| Avant crédit (cash-in, réception P2P) | Service Wallet / Ledger | Plafond de solde + plafond d'entrée mensuel glissant | Rejet avec code métier explicite, pas de crédit partiel |
| Avant débit (cash-out, paiement marchand, virement) | Service Wallet / Ledger | Solde disponible + plafond de sortie mensuel + plafond par transaction | Rejet avant toute écriture en base (pas d'extourne nécessaire) |
| À l'inscription / upgrade | Service KYC | Palier cible cohérent avec preuve d'identité fournie | Refus d'activation du nouveau palier |
| Job périodique | Batch de réconciliation | Cohérence entre solde réel et plafond du palier courant (dérive après downgrade) | Alerte + gel conservatoire si écart |

### 4. Idempotence et concurrence

- Les vérifications de plafond doivent être faites **dans la même transaction** que l'écriture du mouvement (lock pessimiste sur le solde ou contrainte SQL), jamais en best-effort avant un appel asynchrone séparé.
- Documenter le comportement en cas de deux mouvements simultanés proches du plafond (ex : deux cash-in de 600 MAD sur un plafond de 1 000 MAD).

### 5. Mettre à jour le WIP

Ajouter au `{wipFile}` les sections "Upgrade/Downgrade" et "Points d'enforcement", mettre à jour `stepsCompleted` à `[1, 2]`.

### 6. Checkpoint

Afficher : "**Sélectionner :** [P] Party Mode [C] Continuer vers Tests & finalisation (Step 3 of 3)"

HALT et attendre la sélection utilisateur.

- IF P : lire et suivre `{party_mode_exec}`, puis réafficher ce menu.
- IF C : mettre à jour `{wipFile}`, si `mdan_state_update` disponible l'appeler `{ workflow: "pay-kyc-limits", step: 2 }`, puis lire fully et suivre `{nextStepFile}`.

## VÉRIFICATION

- [ ] Upgrade ET downgrade documentés pour chaque transition de palier
- [ ] Comportement du solde en cas de downgrade sous plafond explicité (jamais de perte silencieuse d'argent)
- [ ] Table des points d'enforcement remplie avec composant + comportement de rejet
- [ ] Idempotence/concurrence adressées
