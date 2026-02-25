-- =============================================
-- 01_sp_AnalyzeDuplicateCharges.sql
-- Analyse des débits multiples - LECTURE SEULE (sans modification)
-- =============================================

IF OBJECT_ID('dbo.sp_AnalyzeDuplicateCharges', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_AnalyzeDuplicateCharges;
GO

CREATE PROCEDURE dbo.sp_AnalyzeDuplicateCharges
    @DaysBack INT = 30  -- Nombre de jours à analyser (par défaut 30)
AS
BEGIN
    SET NOCOUNT ON;

    PRINT '=============================================';
    PRINT '   ANALYSE DES DÉBITS MULTIPLES';
    PRINT '   Période: derniers ' + CAST(@DaysBack AS VARCHAR) + ' jours';
    PRINT '=============================================';
    PRINT '';

    -- =====================================================
    -- PARTIE 1: DÉTECTION DES DOUBLONS
    -- =====================================================
    PRINT '--- PARTIE 1: DOUBLONS DÉTECTÉS ---';
    PRINT '';

    ;WITH ActiveContracts AS (
        -- Exclure les contrats résiliés (StatusId = 4)
        SELECT ContractId 
        FROM Contract 
        WHERE ISNULL(StatusId, '0') <> '4'
    ),
    PotentialDuplicates AS (
        -- Grouper les débits par contrat + référence + opération + montant
        SELECT 
            t.ContractId,
            t.ReferenceId,
            t.OperationId,
            t.Amount,
            t.BusinessDate,
            COUNT(*) AS TotalDebits,
            SUM(t.Amount) AS TotalAmount
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
        -- Ordonner par AvailableBalance (plus grand = plus récent)
        SELECT 
            t.Uid,
            t.ContractId,
            t.ReferenceId,
            t.OperationId,
            t.Amount,
            t.AvailableBalance,
            t.StatusCode,
            t.BusinessDate,
            t.ApprovalDateTime,
            pd.TotalDebits,
            pd.TotalAmount,
            ROW_NUMBER() OVER (
                PARTITION BY t.ContractId, t.ReferenceId, t.OperationId, t.Amount
                ORDER BY t.AvailableBalance DESC
            ) AS DebitOrder,
            CASE 
                WHEN t.StatusCode NOT IN ('000', '002') 
                THEN 1 ELSE 0 
            END AS CannotRefund
        FROM [dbo].[Transaction] t
        INNER JOIN PotentialDuplicates pd ON 
            t.ContractId = pd.ContractId 
            AND t.ReferenceId = pd.ReferenceId 
            AND t.OperationId = pd.OperationId
            AND t.Amount = pd.Amount
        WHERE t.Sign = 'D' AND ISNULL(t.IsFee, 0) = 0
    )
    SELECT 
        od.ContractId,
        od.ReferenceId,
        od.OperationId,
        od.Amount,
        od.TotalDebits AS [Nb Débits],
        od.TotalAmount AS [Montant Total],
        od.TotalDebits - 1 AS [Nb À Rembourser],
        (od.TotalDebits - 1) * od.Amount AS [Montant Remboursement],
        od.DebitOrder AS [Ordre],
        od.AvailableBalance AS [Solde Avant],
        od.StatusCode AS [Statut],
        CASE 
            WHEN od.CannotRefund = 1 THEN 'NON-EXTOURNABLE'
            WHEN od.DebitOrder = 1 THEN 'À GARDER'
            ELSE 'À EXTOURNER'
        END AS [Action],
        CASE 
            WHEN od.StatusCode NOT IN ('000', '002', '111') 
            THEN 'Statut non-standard - analyser manuellement'
            ELSE ''
        END AS [Avertissement]
    FROM OrderedDebits od
    ORDER BY od.ContractId, od.BusinessDate, od.AvailableBalance DESC;

    -- =====================================================
    -- PARTIE 2: RÉSUMÉ DES DOUBLONS PAR CONTRAT
    -- =====================================================
    PRINT '';
    PRINT '--- RÉSUMÉ PAR CONTRAT ---';
    PRINT '';

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
            COUNT(*) AS TotalDebits,
            SUM(t.Amount) AS TotalAmount
        FROM [dbo].[Transaction] t
        INNER JOIN ActiveContracts ac ON t.ContractId = ac.ContractId
        WHERE t.Sign = 'D'
            AND t.StatusCode = '000'
            AND ISNULL(t.IsFee, 0) = 0
            AND t.BusinessDate >= DATEADD(DAY, -@DaysBack, CAST(GETDATE() AS DATE))
        GROUP BY t.ContractId, t.ReferenceId, t.OperationId, t.Amount
        HAVING COUNT(*) > 1
    )
    SELECT 
        pd.ContractId,
        COUNT(*) AS [Nb Groupes Doublons],
        SUM(pd.TotalDebits) AS [Nb Total Débits],
        SUM(pd.TotalAmount) AS [Montant Total],
        SUM(pd.TotalDebits - 1) * MAX(pd.Amount) AS [Est. Montant À Rembourser]
    FROM PotentialDuplicates pd
    GROUP BY pd.ContractId
    ORDER BY [Nb Groupes Doublons] DESC;

    -- =====================================================
    -- PARTIE 3: FRAIS ASSOCIÉS AUX DOUBLONS
    -- =====================================================
    PRINT '';
    PRINT '--- FRAIS ASSOCIÉS (IsFee = true) ---';
    PRINT '';

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
            t.Amount
        FROM [dbo].[Transaction] t
        INNER JOIN ActiveContracts ac ON t.ContractId = ac.ContractId
        WHERE t.Sign = 'D'
            AND t.StatusCode = '000'
            AND ISNULL(t.IsFee, 0) = 0
            AND t.BusinessDate >= DATEADD(DAY, -@DaysBack, CAST(GETDATE() AS DATE))
        GROUP BY t.ContractId, t.ReferenceId, t.OperationId, t.Amount
        HAVING COUNT(*) > 1
    )
    SELECT 
        t.ContractId,
        t.ReferenceId,
        t.OperationId,
        t.Amount AS [Montant Débit],
        t_fees.Amount AS [Montant Frais],
        t_fees.Uid AS [Uid Frais],
        CASE WHEN t_fees.StatusCode = '000' THEN 'OK' ELSE t_fees.StatusCode END AS [Statut Frais]
    FROM [dbo].[Transaction] t
    INNER JOIN PotentialDuplicates pd ON 
        t.ContractId = pd.ContractId 
        AND t.ReferenceId = pd.ReferenceId 
        AND t.OperationId = pd.OperationId
        AND t.Amount = pd.Amount
    INNER JOIN [dbo].[Transaction] t_fees ON 
        t.ContractId = t_fees.ContractId 
        AND t.OperationId = t_fees.OperationId
        AND t_fees.IsFee = 1
    WHERE t.Sign = 'D' AND ISNULL(t.IsFee, 0) = 0
    ORDER BY t.ContractId, t.BusinessDate;

    -- =====================================================
    -- PARTIE 4: DÉBITS NON-TRACÉS (1 seule trans, écart balance)
    -- =====================================================
    PRINT '';
    PRINT '--- DÉBITS NON-TRACÉS ---';
    PRINT '';

    ;WITH ActiveContracts AS (
        SELECT ContractId, StatusId
        FROM Contract 
        WHERE ISNULL(StatusId, '0') <> '4'
    ),
    SingleDebits AS (
        -- Transactions uniques par contrat + ref + op + montant
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
        -- Chercher la transaction suivante
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
            END AS ActualBalanceAfter
        FROM WithNextTransaction wnt
    )
    SELECT 
        wa.ContractId,
        wa.ReferenceId,
        wa.OperationId,
        wa.Amount AS [Montant],
        ISNULL(wa.TotalFees, 0) AS [Frais],
        wa.Amount + ISNULL(wa.TotalFees, 0) AS [Total Débit],
        wa.AvailableBalance AS [Solde Avant],
        (wa.AvailableBalance - wa.Amount - ISNULL(wa.TotalFees, 0)) AS [Solde Théorique Après],
        wa.ActualBalanceAfter AS [Solde Réel Après],
        CASE 
            WHEN wa.NextAvailableBalance IS NOT NULL THEN 'Transaction suivante'
            ELSE 'Fonction fgetcontractavailablebalance'
        END AS [Source Solde Réel],
        (wa.AvailableBalance - wa.Amount - ISNULL(wa.TotalFees, 0)) - wa.ActualBalanceAfter AS [Écart]
    FROM WithActualBalance wa
    WHERE (wa.AvailableBalance - wa.Amount - ISNULL(wa.TotalFees, 0)) - wa.ActualBalanceAfter > 0
    ORDER BY wa.ContractId, wa.BusinessDate;

    -- =====================================================
    -- PARTIE 5: STATISTIQUES GLOBALES
    -- =====================================================
    PRINT '';
    PRINT '--- STATISTIQUES GLOBALES ---';
    PRINT '';

    ;WITH ActiveContracts AS (
        SELECT ContractId 
        FROM Contract 
        WHERE ISNULL(StatusId, '0') <> '4'
    ),
    DuplicatesStats AS (
        SELECT 
            t.ContractId,
            t.ReferenceId,
            t.OperationId,
            t.Amount,
            COUNT(*) AS TotalDebits
        FROM [dbo].[Transaction] t
        INNER JOIN ActiveContracts ac ON t.ContractId = ac.ContractId
        WHERE t.Sign = 'D'
            AND t.StatusCode = '000'
            AND ISNULL(t.IsFee, 0) = 0
            AND t.BusinessDate >= DATEADD(DAY, -@DaysBack, CAST(GETDATE() AS DATE))
        GROUP BY t.ContractId, t.ReferenceId, t.OperationId, t.Amount
        HAVING COUNT(*) > 1
    )
    SELECT 
        'Doublons' AS [Type],
        COUNT(DISTINCT ContractId) AS [Nb Contrats Touchés],
        COUNT(*) AS [Nb Groupes Doublons],
        SUM(TotalDebits) AS [Nb Total Débits],
        SUM((TotalDebits - 1) * Amount) AS [Est. Montant À Rembourser]
    FROM DuplicatesStats;

    PRINT '';
    PRINT '=============================================';
    PRINT '   FIN DE L''ANALYSE';
    PRINT '=============================================';

END;
GO

PRINT 'Procédure sp_AnalyzeDuplicateCharges créée avec succès.';
GO
