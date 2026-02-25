-- =============================================
-- 02_sp_PopulateDuplicateReviews.sql
-- Remplir la table temporaire avec les cas détectés
-- =============================================

IF OBJECT_ID('dbo.sp_PopulateDuplicateReviews', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_PopulateDuplicateReviews;
GO

CREATE PROCEDURE dbo.sp_PopulateDuplicateReviews
    @DaysBack INT = 30,
    @AutoProcessSimpleCases BIT = 1,  -- 1 = auto-traiter les cas simples (2 débits)
    @CreatedBy NVARCHAR(100) = 'System'
AS
BEGIN
    SET NOCOUNT ON;

    PRINT '=============================================';
    PRINT '   POPULATE DUPLICATE REVIEWS';
    PRINT '=============================================';
    PRINT '';

    -- Vérifier que la table temporaire existe
    IF OBJECT_ID('tempdb..#DuplicateChargeReviews') IS NULL
    BEGIN
        PRINT 'ERREUR: La table temporaire #DuplicateChargeReviews n''existe pas.';
        PRINT 'Exécutez d''abord: EXEC 00_Setup_TempTable.sql';
        RETURN;
    END

    -- Vider la table temporaire
    DELETE FROM #DuplicateChargeReviews;
    PRINT 'Table temporaire vidée.';

    -- =====================================================
    -- PARTIE 1: INSÉRER LES DOUBLONS
    -- =====================================================
    PRINT '';
    PRINT 'Insertion des doublons détectés...';

    ;WITH ActiveContracts AS (
        SELECT ContractId 
        FROM Contract 
        WHERE ISNULL(StatusId, '0') <> '4'
    ),
    PotentialDuplicates AS (
        SELECT 
            t.ContractId,
            t.ReferenceId,
            t.OperationId,
            t.Amount,
            t.BusinessDate,
            COUNT(*) AS TotalDebits,
            SUM(t.Amount) AS TotalAmount,
            STRING_AGG(t.Uid, ';') WITHIN GROUP (ORDER BY t.AvailableBalance DESC) AS AllUids
        FROM [dbo].[Transaction] t
        INNER JOIN ActiveContracts ac ON t.ContractId = ac.ContractId
        WHERE t.Sign = 'D'
            AND t.StatusCode = '000'
            AND ISNULL(t.IsFee, 0) = 0
            AND t.BusinessDate >= DATEADD(DAY, -@DaysBack, CAST(GETDATE() AS DATE))
        GROUP BY t.ContractId, t.ReferenceId, t.OperationId, t.Amount, t.BusinessDate
        HAVING COUNT(*) > 1
    ),
    OrderedDebits AS (
        SELECT 
            t.Uid,
            t.ContractId,
            t.ReferenceId,
            t.OperationId,
            t.Amount,
            t.AvailableBalance,
            t.StatusCode,
            pd.TotalDebits,
            pd.AllUids,
            ROW_NUMBER() OVER (
                PARTITION BY t.ContractId, t.ReferenceId, t.OperationId, t.Amount
                ORDER BY t.AvailableBalance DESC
            ) AS DebitOrder
        FROM [dbo].[Transaction] t
        INNER JOIN PotentialDuplicates pd ON 
            t.ContractId = pd.ContractId 
            AND t.ReferenceId = pd.ReferenceId 
            AND t.OperationId = pd.OperationId
            AND t.Amount = pd.Amount
        WHERE t.Sign = 'D' AND ISNULL(t.IsFee, 0) = 0
    ),
    WithFees AS (
        SELECT 
            od.*,
            (SELECT SUM(Amount) FROM [dbo].[Transaction] tf 
             WHERE tf.ContractId = od.ContractId 
                AND tf.OperationId = od.OperationId 
                AND tf.IsFee = 1 
                AND tf.Sign = 'D'
                AND tf.StatusCode = '000') AS TotalFees
        FROM OrderedDebits od
    )
    INSERT INTO #DuplicateChargeReviews (
        ContractId,
        CaseType,
        OriginalReferenceId,
        OriginalOperationId,
        DuplicateCount,
        Amount,
        FeeAmount,
        RefundAmount,
        RefundStatus,
        CreatedAt,
        CreatedBy,
        OriginalTransactionUids,
        LastTransactionUid
    )
    SELECT 
        wh.ContractId,
        'Duplicate',
        wh.ReferenceId,
        wh.OperationId,
        wh.TotalDebits,
        wh.Amount,
        ISNULL(wh.TotalFees, 0),
        CASE 
            WHEN wh.StatusCode NOT IN ('000', '002') THEN 0  -- Pas extournable
            WHEN wh.DebitOrder = 1 THEN 0  -- Dernier = à garder
            ELSE (wh.TotalDebits - 1) * wh.Amount + ISNULL(wh.TotalFees, 0)
        END AS RefundAmount,
        CASE 
            WHEN wh.StatusCode NOT IN ('000', '002') THEN 'Pending'  -- Analyser manuellement
            WHEN @AutoProcessSimpleCases = 1 AND wh.TotalDebits = 2 THEN 'AutoProcessed'
            ELSE 'Pending'
        END AS RefundStatus,
        GETUTCDATE(),
        @CreatedBy,
        wh.AllUids,
        (SELECT TOP 1 Uid FROM OrderedDebits od2 
         WHERE od2.ContractId = wh.ContractId 
            AND od2.ReferenceId = wh.ReferenceId 
            AND od2.OperationId = wh.OperationId
         ORDER BY od2.AvailableBalance DESC) AS LastTransactionUid
    FROM WithFees wh
    WHERE wh.DebitOrder > 1 OR wh.StatusCode NOT IN ('000', '002');

    DECLARE @InsertedDoublons INT = @@ROWCOUNT;
    PRINT '  -> ' + CAST(@InsertedDoublons AS VARCHAR) + ' cas de doublons insérés.';

    -- =====================================================
    -- PARTIE 2: INSÉRER LES DÉBITS NON-TRACÉS
    -- =====================================================
    PRINT '';
    PRINT 'Insertion des débits non-tracés...';

    ;WITH ActiveContracts AS (
        SELECT ContractId, StatusId
        FROM Contract 
        WHERE ISNULL(StatusId, '0') <> '4'
    ),
    SingleDebits AS (
        SELECT 
            t.ContractId,
            t.ReferenceId,
            t.OperationId,
            t.Amount,
            t.AvailableBalance,
            t.BusinessDate,
            t.Uid,
            t.StatusCode,
            (SELECT SUM(Amount) FROM [dbo].[Transaction] tf 
             WHERE tf.ContractId = t.ContractId 
                AND tf.OperationId = t.OperationId 
                AND tf.IsFee = 1 
                AND tf.Sign = 'D'
                AND tf.StatusCode = '000') AS TotalFees
        FROM [dbo].[Transaction] t
        INNER JOIN ActiveContracts ac ON t.ContractId = ac.ContractId
        WHERE t.Sign = 'D'
            AND t.StatusCode = '000'
            AND ISNULL(t.IsFee, 0) = 0
            AND t.BusinessDate >= DATEADD(DAY, -@DaysBack, CAST(GETDATE() AS DATE))
    ),
    WithNextTransaction AS (
        SELECT 
            sd.*,
            nt.AvailableBalance AS NextAvailableBalance,
            nt.Uid AS NextUid
        FROM SingleDebits sd
        OUTER APPLY (
            SELECT TOP 1 
                t2.Uid,
                t2.AvailableBalance,
                t2.BusinessDate,
                t2.ApprovalDateTime
            FROM [dbo].[Transaction] t2
            WHERE t2.ContractId = sd.ContractId
                AND t2.BusinessDate >= sd.BusinessDate
                AND t2.Uid <> sd.Uid
            ORDER BY t2.BusinessDate ASC, ISNULL(t2.ApprovalDateTime, t2.BusinessDate) ASC
        ) nt
    ),
    WithActualBalance AS (
        SELECT 
            wnt.*,
            CASE 
                WHEN wnt.NextAvailableBalance IS NOT NULL THEN wnt.NextAvailableBalance
                ELSE dbo.fgetcontractavailablebalance(wnt.ContractId)
            END AS ActualBalanceAfter,
            CASE 
                WHEN wnt.NextAvailableBalance IS NOT NULL THEN wnt.NextAvailableBalance
                ELSE dbo.fgetcontractavailablebalance(wnt.ContractId)
            END - (wnt.AvailableBalance - wnt.Amount - ISNULL(wnt.TotalFees, 0)) AS BalanceDiff
        FROM WithNextTransaction wnt
    )
    INSERT INTO #DuplicateChargeReviews (
        ContractId,
        CaseType,
        OriginalReferenceId,
        OriginalOperationId,
        DuplicateCount,
        Amount,
        FeeAmount,
        RefundAmount,
        RefundStatus,
        BalanceAdjustment,
        ClientNote,
        CreatedAt,
        CreatedBy,
        OriginalTransactionUids
    )
    SELECT 
        wa.ContractId,
        'Untraced',
        wa.ReferenceId,
        wa.OperationId,
        1,
        wa.Amount,
        ISNULL(wa.TotalFees, 0),
        0,
        'Pending',
        ABS(wa.BalanceDiff),
        'Écart balance détecté. Solde théorique: ' + CAST((wa.AvailableBalance - wa.Amount - ISNULL(wa.TotalFees, 0)) AS VARCHAR(20)) 
            + ', Solde réel: ' + CAST(wa.ActualBalanceAfter AS VARCHAR(20)) 
            + ', Diff: ' + CAST(wa.BalanceDiff AS VARCHAR(20)),
        GETUTCDATE(),
        @CreatedBy,
        wa.Uid
    FROM WithActualBalance wa
    WHERE wa.BalanceDiff < 0  -- только отрицательные различия (недостающие средства)
        AND ABS(wa.BalanceDiff) > 0.01;  -- Seuil de 0.01 pour éviter les erreurs de précision

    DECLARE @InsertedUntraced INT = @@ROWCOUNT;
    PRINT '  -> ' + CAST(@InsertedUntraced AS VARCHAR) + ' cas de débits non-tracés insérés.';

    -- =====================================================
    -- RÉSUMÉ
    -- =====================================================
    PRINT '';
    PRINT '=============================================';
    PRINT '   RÉSUMÉ';
    PRINT '=============================================';
    
    SELECT 
        CaseType,
        RefundStatus,
        COUNT(*) AS [Nombre],
        SUM(RefundAmount) AS [Montant Total],
        SUM(BalanceAdjustment) AS [Ajustement Total]
    FROM #DuplicateChargeReviews
    GROUP BY CaseType, RefundStatus
    ORDER BY CaseType, RefundStatus;

    PRINT '';
    PRINT 'Procédure terminée. Utilisez sp_GetPendingReviews pour voir les cas.';

END;
GO

PRINT 'Procédure sp_PopulateDuplicateReviews créée avec succès.';
GO
