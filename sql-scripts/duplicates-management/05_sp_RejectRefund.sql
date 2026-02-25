-- =============================================
-- 05_sp_RejectRefund.sql
-- Rejeter un cas de remboursement
-- =============================================

IF OBJECT_ID('dbo.sp_RejectRefund', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_RejectRefund;
GO

CREATE PROCEDURE dbo.sp_RejectRefund
    @ReviewId INT,
    @RejectedBy NVARCHAR(100),
    @Reason NVARCHAR(1000)
AS
BEGIN
    SET NOCOUNT ON;

    -- Vérifier que la table temporaire existe
    IF OBJECT_ID('tempdb..#DuplicateChargeReviews') IS NULL
    BEGIN
        PRINT 'ERREUR: La table temporaire n''existe pas.';
        RETURN;
    END

    -- Vérifier que le cas existe et est en attente
    IF NOT EXISTS (
        SELECT 1 FROM #DuplicateChargeReviews 
        WHERE Id = @ReviewId AND RefundStatus = 'Pending'
    )
    BEGIN
        PRINT 'ERREUR: Cas non trouvé ou statut différent de Pending.';
        RETURN;
    END

    -- Mettre à jour le statut
    UPDATE #DuplicateChargeReviews
    SET RefundStatus = 'Rejected',
        RejectedBy = @RejectedBy,
        RejectedAt = GETUTCDATE(),
        ClientNote = ISNULL(ClientNote + '; ', '') + 'Rejeté par: ' + @RejectedBy + '. Raison: ' + @Reason
    WHERE Id = @ReviewId;

    PRINT 'Cas #' + CAST(@ReviewId AS VARCHAR) + ' rejeté par ' + @RejectedBy + '. Raison: ' + @Reason;

END;
GO

PRINT 'Procédure sp_RejectRefund créée avec succès.';
GO
