-- =============================================
-- 04_sp_ApproveRefund.sql
-- Approuver un cas de remboursement
-- =============================================

IF OBJECT_ID('dbo.sp_ApproveRefund', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_ApproveRefund;
GO

CREATE PROCEDURE dbo.sp_ApproveRefund
    @ReviewId INT,
    @ApprovedBy NVARCHAR(100),
    @Note NVARCHAR(500) = NULL
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
    SET RefundStatus = 'Approved',
        ApprovedBy = @ApprovedBy,
        ApprovedAt = GETUTCDATE(),
        ClientNote = ISNULL(ClientNote + '; ', '') + 'Approuvé par: ' + @ApprovedBy + ISNULL('. Note: ' + @Note, '')
    WHERE Id = @ReviewId;

    PRINT 'Cas #' + CAST(@ReviewId AS VARCHAR) + ' approuvé par ' + @ApprovedBy;

END;
GO

PRINT 'Procédure sp_ApproveRefund créée avec succès.';
GO
