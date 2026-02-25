-- =============================================
-- 03_sp_GetPendingReviews.sql
-- Liste des cas en attente de validation
-- =============================================

IF OBJECT_ID('dbo.sp_GetPendingReviews', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_GetPendingReviews;
GO

CREATE PROCEDURE dbo.sp_GetPendingReviews
    @ContractId NVARCHAR(50) = NULL,
    @CaseType NVARCHAR(20) = NULL,
    @RefundStatus NVARCHAR(20) = NULL,
    @DateFrom DATETIME = NULL,
    @DateTo DATETIME = NULL
AS
BEGIN
    SET NOCOUNT ON;

    -- Vérifier que la table temporaire existe
    IF OBJECT_ID('tempdb..#DuplicateChargeReviews') IS NULL
    BEGIN
        PRINT 'ERREUR: La table temporaire #DuplicateChargeReviews n''existe pas.';
        PRINT 'Exécutez d''abord: EXEC 00_Setup_TempTable.sql';
        RETURN;
    END

    -- Liste principale
    SELECT 
        Id,
        ContractId,
        CaseType,
        OriginalReferenceId,
        OriginalOperationId,
        DuplicateCount,
        Amount,
        FeeAmount,
        RefundAmount,
        RefundStatus,
        ApprovedBy,
        ApprovedAt,
        RejectedBy,
        RejectedAt,
        ProcessedAt,
        NewReferenceId,
        BalanceAdjustment,
        ClientNote,
        CreatedAt,
        CreatedBy
    FROM #DuplicateChargeReviews
    WHERE 1=1
        AND (@ContractId IS NULL OR ContractId = @ContractId)
        AND (@CaseType IS NULL OR CaseType = @CaseType)
        AND (@RefundStatus IS NULL OR RefundStatus = @RefundStatus)
        AND (@DateFrom IS NULL OR CreatedAt >= @DateFrom)
        AND (@DateTo IS NULL OR CreatedAt <= @DateTo)
    ORDER BY CreatedAt DESC;

    -- Statistiques
    PRINT '';
    PRINT '--- STATISTIQUES ---';
    
    SELECT 
        CaseType,
        RefundStatus,
        COUNT(*) AS [Nombre],
        SUM(RefundAmount) AS [Montant]
    FROM #DuplicateChargeReviews
    WHERE 1=1
        AND (@ContractId IS NULL OR ContractId = @ContractId)
        AND (@DateFrom IS NULL OR CreatedAt >= @DateFrom)
        AND (@DateTo IS NULL OR CreatedAt <= @DateTo)
    GROUP BY CaseType, RefundStatus
    ORDER BY CaseType, RefundStatus;

END;
GO

PRINT 'Procédure sp_GetPendingReviews créée avec succès.';
GO
