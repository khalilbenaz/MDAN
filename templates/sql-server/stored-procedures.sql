-- =============================================
-- SQL Server Stored Procedures Template
-- Version: 1.0.0
-- =============================================

USE YourDatabaseName;
GO

-- =============================================
-- User Management Procedures
-- =============================================

-- Create User
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_CreateUser]') AND type in (N'P', N'PC'))
DROP PROCEDURE [dbo].[sp_CreateUser];
GO

CREATE PROCEDURE [dbo].[sp_CreateUser]
    @Username NVARCHAR(100),
    @Email NVARCHAR(255),
    @PasswordHash NVARCHAR(255),
    @FirstName NVARCHAR(100) = NULL,
    @LastName NVARCHAR(100) = NULL,
    @CreatedBy UNIQUEIDENTIFIER = NULL,
    @UserId UNIQUEIDENTIFIER OUTPUT,
    @ErrorMessage NVARCHAR(500) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Check if username exists
        IF EXISTS (SELECT 1 FROM [dbo].[Users] WHERE [Username] = @Username)
        BEGIN
            SET @ErrorMessage = 'Username already exists';
            ROLLBACK TRANSACTION;
            RETURN;
        END
        
        -- Check if email exists
        IF EXISTS (SELECT 1 FROM [dbo].[Users] WHERE [Email] = @Email)
        BEGIN
            SET @ErrorMessage = 'Email already exists';
            ROLLBACK TRANSACTION;
            RETURN;
        END
        
        -- Create user
        INSERT INTO [dbo].[Users] (
            [Username], [Email], [PasswordHash], [FirstName], [LastName],
            [CreatedBy], [UpdatedBy]
        )
        VALUES (
            @Username, @Email, @PasswordHash, @FirstName, @LastName,
            @CreatedBy, @CreatedBy
        );
        
        SET @UserId = SCOPE_IDENTITY();
        
        -- Log audit
        INSERT INTO [dbo].[AuditLog] (
            [TableName], [RecordId], [Action], [NewValue], [ChangedBy]
        )
        VALUES (
            'Users', CAST(@UserId AS NVARCHAR(100)), 'INSERT',
            'User created: ' + @Username, COALESCE(CAST(@CreatedBy AS NVARCHAR(100)), 'System')
        );
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        
        SET @ErrorMessage = ERROR_MESSAGE();
    END CATCH
END
GO

-- Get User by ID
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_GetUserById]') AND type in (N'P', N'PC'))
DROP PROCEDURE [dbo].[sp_GetUserById];
GO

CREATE PROCEDURE [dbo].[sp_GetUserById]
    @UserId UNIQUEIDENTIFIER
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        [Id], [Username], [Email], [FirstName], [LastName],
        [IsActive], [EmailVerified], [LastLogin], [CreatedAt], [UpdatedAt]
    FROM [dbo].[Users]
    WHERE [Id] = @UserId;
END
GO

-- Update User
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_UpdateUser]') AND type in (N'P', N'PC'))
DROP PROCEDURE [dbo].[sp_UpdateUser];
GO

CREATE PROCEDURE [dbo].[sp_UpdateUser]
    @UserId UNIQUEIDENTIFIER,
    @FirstName NVARCHAR(100) = NULL,
    @LastName NVARCHAR(100) = NULL,
    @UpdatedBy UNIQUEIDENTIFIER = NULL,
    @ErrorMessage NVARCHAR(500) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        DECLARE @OldValue NVARCHAR(MAX);
        DECLARE @NewValue NVARCHAR(MAX);
        
        -- Get old values
        SELECT @OldValue = 'FirstName:' + ISNULL([FirstName], '') + ',LastName:' + ISNULL([LastName], '')
        FROM [dbo].[Users]
        WHERE [Id] = @UserId;
        
        -- Update user
        UPDATE [dbo].[Users]
        SET 
            [FirstName] = @FirstName,
            [LastName] = @LastName,
            [UpdatedAt] = GETUTCDATE(),
            [UpdatedBy] = @UpdatedBy
        WHERE [Id] = @UserId;
        
        IF @@ROWCOUNT = 0
        BEGIN
            SET @ErrorMessage = 'User not found';
            ROLLBACK TRANSACTION;
            RETURN;
        END
        
        -- Get new values
        SELECT @NewValue = 'FirstName:' + ISNULL([FirstName], '') + ',LastName:' + ISNULL([LastName], '')
        FROM [dbo].[Users]
        WHERE [Id] = @UserId;
        
        -- Log audit
        INSERT INTO [dbo].[AuditLog] (
            [TableName], [RecordId], [Action], [OldValue], [NewValue], [ChangedBy]
        )
        VALUES (
            'Users', CAST(@UserId AS NVARCHAR(100)), 'UPDATE',
            @OldValue, @NewValue, COALESCE(CAST(@UpdatedBy AS NVARCHAR(100)), 'System')
        );
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        
        SET @ErrorMessage = ERROR_MESSAGE();
    END CATCH
END
GO

-- =============================================
-- Transaction Procedures
-- =============================================

-- Create Transaction
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_CreateTransaction]') AND type in (N'P', N'PC'))
DROP PROCEDURE [dbo].[sp_CreateTransaction];
GO

CREATE PROCEDURE [dbo].[sp_CreateTransaction]
    @UserId UNIQUEIDENTIFIER,
    @Type NVARCHAR(20),
    @Amount DECIMAL(18, 2),
    @Currency NVARCHAR(3) = 'MAD',
    @Description NVARCHAR(500) = NULL,
    @Reference NVARCHAR(100) = NULL,
    @Provider NVARCHAR(50) = NULL,
    @ProviderTransactionId NVARCHAR(100) = NULL,
    @Metadata NVARCHAR(MAX) = NULL,
    @TransactionId UNIQUEIDENTIFIER OUTPUT,
    @TransactionNumber NVARCHAR(50) OUTPUT,
    @ErrorMessage NVARCHAR(500) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Generate transaction number
        DECLARE @Prefix NVARCHAR(10) = 'TXN';
        DECLARE @DatePart NVARCHAR(8) = REPLACE(CONVERT(NVARCHAR, GETDATE(), 112), '-', '');
        DECLARE @RandomPart NVARCHAR(6) = RIGHT('000000' + CAST(CAST(CHECKSUM(NEWID()) AS INT) % 1000000 AS NVARCHAR), 6);
        SET @TransactionNumber = @Prefix + @DatePart + @RandomPart;
        
        -- Create transaction
        INSERT INTO [dbo].[Transactions] (
            [TransactionNumber], [UserId], [Type], [Amount], [Currency],
            [Description], [Reference], [Provider], [ProviderTransactionId], [Metadata]
        )
        VALUES (
            @TransactionNumber, @UserId, @Type, @Amount, @Currency,
            @Description, @Reference, @Provider, @ProviderTransactionId, @Metadata
        );
        
        SET @TransactionId = SCOPE_IDENTITY();
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        
        SET @ErrorMessage = ERROR_MESSAGE();
    END CATCH
END
GO

-- Update Transaction Status
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_UpdateTransactionStatus]') AND type in (N'P', N'PC'))
DROP PROCEDURE [dbo].[sp_UpdateTransactionStatus];
GO

CREATE PROCEDURE [dbo].[sp_UpdateTransactionStatus]
    @TransactionId UNIQUEIDENTIFIER,
    @Status NVARCHAR(20),
    @ProcessedAt DATETIME = NULL,
    @ErrorMessage NVARCHAR(500) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        DECLARE @OldStatus NVARCHAR(20);
        
        -- Get old status
        SELECT @OldStatus = [Status]
        FROM [dbo].[Transactions]
        WHERE [Id] = @TransactionId;
        
        -- Update transaction
        UPDATE [dbo].[Transactions]
        SET 
            [Status] = @Status,
            [ProcessedAt] = COALESCE(@ProcessedAt, GETUTCDATE())
        WHERE [Id] = @TransactionId;
        
        IF @@ROWCOUNT = 0
        BEGIN
            SET @ErrorMessage = 'Transaction not found';
            ROLLBACK TRANSACTION;
            RETURN;
        END
        
        -- Log audit
        INSERT INTO [dbo].[AuditLog] (
            [TableName], [RecordId], [Action], [OldValue], [NewValue], [ChangedBy]
        )
        VALUES (
            'Transactions', CAST(@TransactionId AS NVARCHAR(100)), 'UPDATE',
            'Status:' + @OldStatus, 'Status:' + @Status, 'System'
        );
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        
        SET @ErrorMessage = ERROR_MESSAGE();
    END CATCH
END
GO

PRINT 'Stored procedures created successfully.';