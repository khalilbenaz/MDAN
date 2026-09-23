# ISO 8583 — Mémo (MTI, Data Elements, Codes Réponse)

Mémo de référence rapide pour intégrations switch/acquéreur (ex : CMI, GSIMT) au Maroc. C'est un point de départ générique, pas une spécification normative complète — toujours confirmer les Data Elements propriétaires et les codes réponse exacts avec la documentation technique du switch/acquéreur réellement intégré.

## 1. MTI (Message Type Indicator) courants

| MTI | Nom | Usage |
|-----|-----|-------|
| 0100 / 0110 | Authorization Request / Response | Demande d'autorisation avant capture (achat carte, retrait GAB) |
| 0200 / 0210 | Financial Request / Response | Transaction financière avec capture immédiate |
| 0220 / 0230 | Financial Advice / Response | Notification a posteriori d'une transaction déjà exécutée (ex : terminal offline) |
| 0400 / 0410 | Reversal Request / Response | Demande d'annulation d'une transaction précédente |
| 0420 / 0430 | Reversal Advice / Response | Notification qu'une annulation a déjà été appliquée localement |
| 0800 / 0810 | Network Management Request / Response | Sign-on/sign-off, echo test, échange de clés |

Convention de lecture : le 1er chiffre = version ISO 8583, le 2e = classe de message (1=autorisation, 2=financier, 4=reversal, 8=network mgmt), le 3e = origine (0=acquéreur), le 4e = fonction (0=request, 1=response, 2=advice).

## 2. Data Elements (DE) les plus utilisés

| DE | Nom | Format | Note |
|----|-----|--------|------|
| DE2 | Primary Account Number (PAN) | LLVAR n..19 | Ne jamais logger en clair — troncature/masquage systématique (cf. PCI DSS) |
| DE3 | Processing Code | n6 | Type d'opération (ex : `000000` = achat, `010000` = retrait) |
| DE4 | Amount, Transaction | n12 | Montant en centimes, sans séparateur |
| DE7 | Transmission Date & Time | n10 (MMDDhhmmss) | Horodatage d'émission du message |
| DE11 | STAN (System Trace Audit Number) | n6 | Doit être unique par connexion/journée comptable |
| DE12 / DE13 | Local Transaction Time / Date | n6 / n4 | |
| DE22 | POS Entry Mode | n3 | Mode de saisie (puce, bande, sans contact, saisie manuelle) |
| DE32 | Acquiring Institution ID | LLVAR n..11 | |
| DE37 | Retrieval Reference Number (RRN) | an12 | Clé de corrélation métier stable entre requête/réponse/advice/reversal |
| DE38 | Authorization ID Response | an6 | Présent sur réponse approuvée |
| DE39 | Response Code | an2 | Voir §3 |
| DE41 | Card Acceptor Terminal ID | ans8 | |
| DE42 | Card Acceptor ID Code | ans15 | |
| DE49 | Currency Code, Transaction | n3 (ISO 4217) | `504` = MAD |
| DE90 | Original Data Elements | n42 | Référence la transaction d'origine sur un reversal/advice (MTI+STAN+date+heure d'origine) |

## 3. Codes réponse (DE39) courants

| Code | Signification | Traiter comme |
|------|----------------|------------------|
| `00` | Approuvé | Succès |
| `05` | Refus générique (do not honor) | Échec définitif |
| `12` | Transaction invalide | Échec définitif (erreur de format/paramétrage) |
| `13` | Montant invalide | Échec définitif |
| `14` | Numéro de carte invalide | Échec définitif |
| `51` | Fonds insuffisants | Échec définitif |
| `54` | Carte expirée | Échec définitif |
| `57` | Transaction non permise pour ce compte | Échec définitif |
| `61` | Dépasse le plafond de retrait | Échec définitif |
| `62` | Carte restreinte | Échec définitif |
| `91` | Émetteur ou switch injoignable | **Incertain** — traiter comme timeout, pas comme un refus |
| `96` | Erreur système / dysfonctionnement | **Incertain** — déclencher status inquiry ou reversal, pas de conclusion automatique |

Règle générale : tout code hors de la liste blanche des refus définitifs connus doit être traité par défaut comme **incertain**, jamais comme un succès implicite.

## 4. Reversal & Advice — rappel

- **0400 (Reversal Request)** : émis quand une transaction doit être annulée avant confirmation définitive (timeout local, erreur détectée après envoi). Référence l'original via DE90.
- **0420 (Reversal Advice)** : notifie qu'une annulation a déjà été appliquée côté émetteur (ex : après un timeout où le terminal a annulé unilatéralement) — le récepteur doit l'accepter même s'il pensait la transaction encore valide.
- Un reversal ne doit jamais être silencieusement ignoré : si la transaction d'origine est introuvable côté récepteur, c'est un cas à escalader, pas à rejeter sans trace.

## 5. Idempotence protocolaire

- **STAN (DE11)** : unique par connexion et par journée comptable ; sa réutilisation avant expiration de fenêtre signale un problème de génération côté émetteur.
- **RRN (DE37)** : clé de corrélation métier stable à travers tout le cycle de vie (requête → réponse → advice → reversal) ; toujours la propager et l'utiliser pour dédupliquer un message reçu deux fois.

## 6. Pour aller plus loin

Utiliser ce mémo comme aide-mémoire d'implémentation, mais toujours valider MTI/DE/codes réponse exacts avec :
- La spécification technique du switch/acquéreur cible (ex : cahier des charges technique CMI)
- Les DE propriétaires additionnels que le partenaire peut exiger (souvent DE48, DE54, DE62, DE63…)
