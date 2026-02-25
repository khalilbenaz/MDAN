# Gestion des Débits Multiples - Guide Helpdesk

## 1. Contexte

Ce système permet de détecter et traiter les cas où les comptes clients ont été débités plusieurs fois (2, 4, voire 5 fois).

## 2. Problématique

### Types de problèmes détectés

| Type | Description | Action |
|------|-------------|--------|
| **Doublons** | Plusieurs débits pour même opération | Extourner + rembourser |
| **Débits non-tracés** | Écart entre solde théorique et réel | Ajuster le balance |

### Règles de détection

- **Doublons** : Même `ContractId` + `ReferenceId` + `OperationId` + `Amount`
- **Dernière transaction** : Celle avec le plus grand `AvailableBalance` (solde AVANT)
- **Statuts à extourner** : `000` (OK) et `002` (étape simulation)
- **Contrats exclus** : `StatusId = 4` (résiliés)

## 3. Solution

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WORKFLOW COMPLET                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. ANALYSE (sp_AnalyzeDuplicateCharges)                   │
│     └─→ Détection sans modification                         │
│                                                              │
│  2. POPULATE (sp_PopulateDuplicateReviews)                 │
│     └─→ Remplir table temporaire                            │
│                                                              │
│  3. VALIDATION                                              │
│     ├─→ Auto-refund (cas simples)                           │
│     └─→ Manuel (sp_ApproveRefund / sp_RejectRefund)       │
│                                                              │
│  4. TRAITEMENT (sp_ProcessDuplicateRefunds)                │
│     ├─→ Extourner les doublons (StatusCode → 111)          │
│     ├─→ Créer transaction crédit                           │
│     └─→ Ajuster le balance si nécessaire                   │
│                                                              │
│  5. AUDIT (sp_GetRefundHistory)                             │
│     └─→ Historique complet                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 4. Procédure Étape par Étape

### Étape 1 : Analyse Préliminaire

```sql
-- Exécuter l'analyse (lecture seule - AUCUNE modification)
EXEC sp_AnalyzeDuplicateCharges;
```

**Résultat** : Affiche tous les doublons et cas non-tracés détectés.

---

### Étape 2 : Préparer les Cas à Traiter

```sql
-- Créer la table temporaire locale
EXEC sp_PopulateDuplicateReviews;
```

Cette étape insère les cas détectés dans une table temporaire `#DuplicateChargeReviews`.

---

### Étape 3 : Consulter les Cas en Attente

```sql
-- Voir tous les cas Pending
EXEC sp_GetPendingReviews;

-- Filtrer par contrat spécifique
EXEC sp_GetPendingReviews @ContractId = 'CONTRACT123';
```

---

### Étape 4 : Traiter les Cas

#### Option A : Traitement Automatique (Cas Simples)

```sql
-- Les cas avec exactement 2 débits peuvent être traités auto
-- Vérifier d'abord
SELECT * FROM #DuplicateChargeReviews 
WHERE RefundStatus = 'Pending' AND DuplicateCount = 2;
```

#### Option B : Validation Manuelle

```sql
-- APPROUVER un cas
EXEC sp_ApproveRefund 
    @ReviewId = 1, 
    @ApprovedBy = 'john.doe';

-- REJETER un cas
EXEC sp_RejectRefund 
    @ReviewId = 1, 
    @RejectedBy = 'john.doe', 
    @Reason = 'Transaction déjà remboursée par autre moyen';
```

---

### Étape 5 : Exécuter les Traitements

```sql
-- Traiter les refunds approuvés
EXEC sp_ProcessDuplicateRefunds;

-- Ajuster les débits non-tracés
EXEC sp_AdjustUntracedDebits;
```

---

### Étape 6 : Consulter l'Historique

```sql
-- Historique complet
EXEC sp_GetRefundHistory;

-- Filtres
EXEC sp_GetRefundHistory 
    @DateFrom = '2024-01-01',
    @DateTo = '2024-01-31';

EXEC sp_GetRefundHistory 
    @ContractId = 'CONTRACT123';

EXEC sp_GetRefundHistory 
    @RefundStatus = 'Processed';
```

---

## 5. Exemples d'Utilisation

### Exemple 1 : Doublon Simple (2 débits)

**Situation** :
- Contrat CONTRACT001
- 2 débits de 100 DH chacun
- StatusCode = 000 pour les deux

**Résultat** :
- 1 transaction extournée (StatusCode → 111)
- 1 transaction de crédit de 200 DH créée

---

### Exemple 2 : Doublon avec 1 statut non-extournable

**Situation** :
- Contrat CONTRACT002
- 3 débits de 100 DH
- 1 avec StatusCode = 111 (déjà extourné)

**Résultat** :
- Les 2 restants extournés (→ 111)
- Crédit de 200 DH créé

---

### Exemple 3 : Débits non-tracés

**Situation** :
- Contrat CONTRACT003
- 1 seul débit de 100 DH
- AvailableBalance = 1000
- Solde actuel = 800 (au lieu de 900)

**Résultat** :
- Écart de 200 DH détecté
- Balance.TransferCreditAmount += 200

---

### Exemple 4 : Avec Frais

**Situation** :
- Contrat CONTRACT004
- 1 débit de 200 DH
- 2 lignes de frais (IsFee = true) de 10 DH chacune

**Résultat** :
- Crédit total = 200 + 10 + 10 = 220 DH

---

## 6. Codes de Statut

### Statut des Reviews

| Statut | Description |
|--------|-------------|
| `Pending` | En attente de validation |
| `AutoProcessed` | Traité automatiquement (cas simples) |
| `Approved` | Approuvé manuellement |
| `Rejected` | Rejeté manuellement |
| `Processed` | Traitement terminé |

### StatusCode Transaction

| Code | Description |
|------|-------------|
| `000` | Transaction OK |
| `002` | Étape simulation |
| `111` | Transaction extournée |

### Statut Contrat

| StatusId | Description |
|----------|-------------|
| `4` | Résilié (exclu du traitement) |

---

## 7. FAQ

### Q : Pourquoi certains cas ne sont-ils pas automatiquement extournés ?

R : Si le contrat est résilié (`StatusId = 4`), le système ne propose pas de remboursement automatique. Ces cas nécessitent une validation manuelle.

### Q : Comment savoir si un cas a été traité ?

R : Consultez la table `#DuplicateChargeReviews` ou exécutez `sp_GetRefundHistory`.

### Q : Que faire si le montant du remboursement semble incorrect ?

R : Rejeter le cas (`sp_RejectRefund`) avec la raison, puis analyser manuellement via `sp_AnalyzeDuplicateCharges`.

### Q : Peut-on annuler un traitement ?

R : Les transactions extournées (StatusCode = 111) peuvent être remises à 000 si nécessaire, mais cela doit être fait manuellement en base.

### Q : Comment génère-t-on un rapport ?

R : Exécutez `sp_GetRefundHistory` avec les filtres de date appropriés.

---

## 8. Schéma des Tables

### Table Temporaire #DuplicateChargeReviews

| Colonne | Type | Description |
|---------|------|-------------|
| Id | INT | ID unique |
| ContractId | NVARCHAR(50) | ID du contrat |
| CaseType | NVARCHAR(20) | 'Duplicate' ou 'Untraced' |
| OriginalReferenceId | NVARCHAR(100) | Référence originale |
| OriginalOperationId | NVARCHAR(100) | Opération originale |
| DuplicateCount | INT | Nb de débits détectés |
| Amount | DECIMAL(18,2) | Montant unitaire |
| FeeAmount | DECIMAL(18,2) | Montant des frais |
| RefundAmount | DECIMAL(18,2) | Montant à rembourser |
| RefundStatus | NVARCHAR(20) | Statut du traitement |
| ApprovedBy | NVARCHAR(100) | Validateur |
| ApprovedAt | DATETIME | Date validation |
| ProcessedAt | DATETIME | Date traitement |
| NewReferenceId | NVARCHAR(100) | Nouvelle référence |
| BalanceAdjustment | DECIMAL(18,2) | Ajustement balance |
| ClientNote | NVARCHAR(1000) | Notes |
| CreatedAt | DATETIME | Date création |

---

## 9. Contact

Pour toute question ou problème, contacter l'équipe technique.

---

*Document généré automatiquement - Version 1.0*
