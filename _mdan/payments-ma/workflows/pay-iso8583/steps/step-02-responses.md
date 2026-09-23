---
name: 'step-02-responses'
description: 'Codes réponse, reversal, advice'
nextStepFile: './step-03-vectors.md'
wipFile: '{implementation_artifacts}/payments-ma-iso8583-{slug}-wip.md'
---

**Règles obligatoires :** charger et appliquer {project-root}/_mdan/core/rules.md (langue + style de communication).

# Step 2: Codes Réponse, Reversal & Advice

**Progress: Step 2 of 3** - Next: Vecteurs de test & finalisation

## SÉQUENCE D'INSTRUCTIONS

### 1. Codes réponse (DE39)

Documenter, pour l'interface concernée, au minimum :

| DE39 | Signification | Action système |
|------|----------------|-------------------|
| `00` | Approuvé | Compléter l'écriture, créditer/débiter |
| `05` | Refus générique (do not honor) | Rejeter, ne rien écrire en compte |
| `51` | Fonds insuffisants | Rejeter avant tout débit |
| `54` | Carte/compte expiré | Rejeter |
| `57` | Transaction non permise pour ce compte | Rejeter |
| `61` | Dépasse le plafond de retrait | Rejeter (voir aussi `pay-kyc-limits` si wallet) |
| `91` | Émetteur/switch injoignable | Traiter comme timeout → statut incertain, pas un refus définitif |
| `96` | Erreur système | Traiter comme incertain, déclencher status inquiry ou reversal |

Compléter avec les codes propres au switch/acquéreur réel visé.

### 2. Reversal (0400/0420)

- **0400 (Reversal Request)** : émis par l'acquéreur/émetteur quand une transaction doit être annulée avant confirmation définitive (ex : timeout, erreur locale après envoi). Contient DE90 (Original Data Elements) pour référencer la transaction d'origine.
- **0420 (Reversal Advice)** : notifie que l'annulation a DÉJÀ été appliquée localement (ex : après un timeout où le terminal a annulé unilatéralement) — le destinataire doit l'accepter même s'il avait déjà traité l'opération.
- Règle : un reversal ne doit jamais être rejeté silencieusement — s'il ne peut pas être appliqué (transaction d'origine introuvable), documenter la procédure d'escalade (voir workflow `pay-recon`).

### 3. Advice financier (0220/0230)

Utilisé quand une transaction a été exécutée offline (ex : terminal déconnecté) et doit être notifiée a posteriori. Le récepteur doit l'accepter en confiance (le montant a déjà été engagé côté porteur) sauf contrôle de sécurité explicite.

### 4. Idempotence protocolaire

- Un même **STAN (DE11)** ne doit jamais être réutilisé pour une nouvelle transaction avant expiration de la fenêtre (typiquement la journée comptable ou le cycle de connexion).
- Le **RRN (DE37)** est la clé de corrélation métier stable entre requête, réponse, advice et reversal — toujours la propager.
- Documenter le comportement si un message arrive en double (même STAN + même RRN) : renvoyer la réponse déjà connue, ne jamais retraiter.

### 5. Mettre à jour le WIP

Ajouter "Codes réponse", "Reversal/Advice", "Idempotence protocolaire" au `{wipFile}`, `stepsCompleted: [1, 2]`.

### 6. Checkpoint

"**Sélectionner :** [P] Party Mode [C] Continuer vers Vecteurs de test & finalisation (Step 3 of 3)"

HALT et attendre.

- IF P : suivre `{party_mode_exec}`, réafficher.
- IF C : mettre à jour `{wipFile}`, si `mdan_state_update` disponible `{ workflow: "pay-iso8583", step: 2 }`, puis lire fully `{nextStepFile}`.

## VÉRIFICATION

- [ ] Codes réponse couvrant succès + au moins 3 refus + au moins 1 code "incertain" (timeout/erreur système)
- [ ] Reversal ET advice traités séparément avec règle de non-rejet silencieux
- [ ] Règle d'unicité STAN et de propagation RRN documentée
