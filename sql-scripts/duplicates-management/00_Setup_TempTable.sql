-- =============================================
-- 00_Setup_TempTable.sql
-- Création de la table temporaire locale pour le suivi des débits multiples
-- =============================================

IF OBJECT_ID('tempdb..#DuplicateChargeReviews') IS NOT NULL
    DROP TABLE #DuplicateChargeReviews;

CREATE TABLE #DuplicateChargeReviews (
    [Id] INT IDENTITY(1,1) PRIMARY KEY,
    [ContractId] NVARCHAR(50) NOT NULL,
    [CaseType] NVARCHAR(20) NOT NULL,  -- 'Duplicate' / 'Untraced'
    [OriginalReferenceId] NVARCHAR(100) NULL,
    [OriginalOperationId] NVARCHAR(100) NULL,
    [DuplicateCount] INT NOT NULL DEFAULT 1,
    [Amount] DECIMAL(18,2) NOT NULL,
    [FeeAmount] DECIMAL(18,2) NULL DEFAULT 0,
    [RefundAmount] DECIMAL(18,2) NOT NULL,
    [RefundStatus] NVARCHAR(20) NOT NULL DEFAULT 'Pending',
    [ApprovedBy] NVARCHAR(100) NULL,
    [ApprovedAt] DATETIME NULL,
    [RejectedBy] NVARCHAR(100) NULL,
    [RejectedAt] DATETIME NULL,
    [ProcessedAt] DATETIME NULL,
    [NewReferenceId] NVARCHAR(100) NULL,
    [NewOperationId] NVARCHAR(100) NULL,
    [BalanceAdjustment] DECIMAL(18,2) NULL,
    [ClientNote] NVARCHAR(1000) NULL,
    [CreatedAt] DATETIME NOT NULL DEFAULT GETUTCDATE(),
    [CreatedBy] NVARCHAR(100) NULL,
    [OriginalTransactionUids] NVARCHAR(MAX) NULL,  -- Liste des UIDs originaux
    [LastTransactionUid] NVARCHAR(100) NULL  -- UID de la dernière transaction (à garder)
);

-- Index pour optimiser les requêtes
CREATE INDEX IX_Temp_ContractId ON #DuplicateChargeReviews(ContractId);
CREATE INDEX IX_Temp_RefundStatus ON #DuplicateChargeReviews(RefundStatus);
CREATE INDEX IX_Temp_CreatedAt ON #DuplicateChargeReviews(CreatedAt DESC);

PRINT 'Table temporaire #DuplicateChargeReviews créée avec succès.';
