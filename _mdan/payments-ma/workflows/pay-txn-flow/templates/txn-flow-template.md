---
title: 'Flux de paiement - {flow_type}'
slug: '{slug}'
created: '{date}'
status: 'in-progress'
stepsCompleted: []
---

# Flux de Paiement — {flow_type}

> Devise par défaut : {default_currency}. Régulateur : {regulator}.

## 1. Acteurs

(à compléter)

## 2. Machine à états

| État | Signifie | Transitions sortantes | Événement déclencheur |
|------|----------|--------------------------|---------------------------|
| | | | |

## 3. Écritures comptables (double entrée)

### Cas nominal

| Compte | Débit | Crédit | Commentaire |
|--------|-------|--------|-------------|
| | | | |

### Autres états terminaux

(à compléter)

## 4. Idempotence

- Composition de la clé :
- Portée :
- Durée de vie :
- Comportement sur collision :

## 5. Frais

(à compléter)

## 6. Timeouts

| Appel externe | Timeout technique | Timeout métier | Action à l'expiration |
|-----------------|----------------------|-------------------|---------------------------|
| | | | |

## 7. Reversal / Extourne

(à compléter)

## 8. Notifications

(à compléter)

## 9. Outbox

(à compléter)

## 10. Cas de test

| # | Cas | Attendu |
|---|-----|---------|
| | | |
