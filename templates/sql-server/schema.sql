-- =============================================
-- SQL Server Database Schema Template
-- Version: 1.0.0
-- =============================================

-- Enable required features
SET ANSI_NULLS ON;
GO
SET QUOTED_IDENTIFIER ON;
GO

-- =============================================
-- Create Database (if not exists)
-- =============================================
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'YourDatabaseName')
BEGIN
    CREATE DATABASE YourDatabaseName;
END
GO

USE YourDatabaseName;
GO

-- =============================================
-- Schema Versioning Table
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[SchemaVersion]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[SchemaVersion](
        [Id] [int] IDENTITY(1,1) NOT NULL,
        [Version] [nvarchar](50) NOT NULL,
        [Description] [nvarchar](500) NULL,
        [AppliedOn] [datetime] NOT NULL CONSTRAINT [DF_SchemaVersion_AppliedOn] DEFAULT (GETUTCDATE()),
        [AppliedBy] [nvarchar](100) NULL,
        CONSTRAINT [PK_SchemaVersion] PRIMARY KEY CLUSTERED ([Id] ASC)
    );
END
GO

-- =============================================
-- Audit Log Table
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[AuditLog]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[AuditLog](
        [Id] [bigint] IDENTITY(1,1) NOT NULL,
        [TableName] [nvarchar](100) NOT NULL,
        [RecordId] [nvarchar](100) NOT NULL,
        [Action] [nvarchar](20) NOT NULL,
        [OldValue] [nvarchar](max) NULL,
        [NewValue] [nvarchar](max) NULL,
        [ChangedBy] [nvarchar](100) NOT NULL,
        [ChangedOn] [datetime] NOT NULL CONSTRAINT [DF_AuditLog_ChangedOn] DEFAULT (GETUTCDATE()),
        [IpAddress] [nvarchar](50) NULL,
        CONSTRAINT [PK_AuditLog] PRIMARY KEY CLUSTERED ([Id] ASC)
    );
    
    CREATE INDEX [IX_AuditLog_TableName] ON [dbo].[AuditLog]([TableName]);
    CREATE INDEX [IX_AuditLog_ChangedOn] ON [dbo].[AuditLog]([ChangedOn]);
END
GO

-- =============================================
-- Example: Users Table
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Users]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[Users](
        [Id] [uniqueidentifier] NOT NULL CONSTRAINT [DF_Users_Id] DEFAULT (NEWID()),
        [Username] [nvarchar](100) NOT NULL,
        [Email] [nvarchar](255) NOT NULL,
        [PasswordHash] [nvarchar](255) NOT NULL,
        [FirstName] [nvarchar](100) NULL,
        [LastName] [nvarchar](100) NULL,
        [IsActive] [bit] NOT NULL CONSTRAINT [DF_Users_IsActive] DEFAULT (1),
        [EmailVerified] [bit] NOT NULL CONSTRAINT [DF_Users_EmailVerified] DEFAULT (0),
        [LastLogin] [datetime] NULL,
        [FailedLoginAttempts] [int] NOT NULL CONSTRAINT [DF_Users_FailedLoginAttempts] DEFAULT (0),
        [LockedUntil] [datetime] NULL,
        [CreatedAt] [datetime] NOT NULL CONSTRAINT [DF_Users_CreatedAt] DEFAULT (GETUTCDATE()),
        [UpdatedAt] [datetime] NOT NULL CONSTRAINT [DF_Users_UpdatedAt] DEFAULT (GETUTCDATE()),
        [CreatedBy] [uniqueidentifier] NULL,
        [UpdatedBy] [uniqueidentifier] NULL,
        CONSTRAINT [PK_Users] PRIMARY KEY CLUSTERED ([Id] ASC),
        CONSTRAINT [UQ_Users_Username] UNIQUE NONCLUSTERED ([Username] ASC),
        CONSTRAINT [UQ_Users_Email] UNIQUE NONCLUSTERED ([Email] ASC)
    );
    
    CREATE INDEX [IX_Users_Email] ON [dbo].[Users]([Email]);
    CREATE INDEX [IX_Users_IsActive] ON [dbo].[Users]([IsActive]);
END
GO

-- =============================================
-- Example: Roles Table
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Roles]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[Roles](
        [Id] [uniqueidentifier] NOT NULL CONSTRAINT [DF_Roles_Id] DEFAULT (NEWID()),
        [Name] [nvarchar](50) NOT NULL,
        [Description] [nvarchar](255) NULL,
        [IsSystem] [bit] NOT NULL CONSTRAINT [DF_Roles_IsSystem] DEFAULT (0),
        [CreatedAt] [datetime] NOT NULL CONSTRAINT [DF_Roles_CreatedAt] DEFAULT (GETUTCDATE()),
        CONSTRAINT [PK_Roles] PRIMARY KEY CLUSTERED ([Id] ASC),
        CONSTRAINT [UQ_Roles_Name] UNIQUE NONCLUSTERED ([Name] ASC)
    );
END
GO

-- =============================================
-- Example: UserRoles Junction Table
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[UserRoles]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[UserRoles](
        [UserId] [uniqueidentifier] NOT NULL,
        [RoleId] [uniqueidentifier] NOT NULL,
        [AssignedAt] [datetime] NOT NULL CONSTRAINT [DF_UserRoles_AssignedAt] DEFAULT (GETUTCDATE()),
        [AssignedBy] [uniqueidentifier] NULL,
        CONSTRAINT [PK_UserRoles] PRIMARY KEY CLUSTERED ([UserId] ASC, [RoleId] ASC),
        CONSTRAINT [FK_UserRoles_Users] FOREIGN KEY([UserId]) REFERENCES [dbo].[Users]([Id]) ON DELETE CASCADE,
        CONSTRAINT [FK_UserRoles_Roles] FOREIGN KEY([RoleId]) REFERENCES [dbo].[Roles]([Id]) ON DELETE CASCADE
    );
END
GO

-- =============================================
-- Example: Transactions Table (Financial)
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Transactions]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[Transactions](
        [Id] [uniqueidentifier] NOT NULL CONSTRAINT [DF_Transactions_Id] DEFAULT (NEWID()),
        [TransactionNumber] [nvarchar](50) NOT NULL,
        [UserId] [uniqueidentifier] NOT NULL,
        [Type] [nvarchar](20) NOT NULL,
        [Amount] [decimal](18, 2) NOT NULL,
        [Currency] [nvarchar](3) NOT NULL CONSTRAINT [DF_Transactions_Currency] DEFAULT ('MAD'),
        [Status] [nvarchar](20) NOT NULL CONSTRAINT [DF_Transactions_Status] DEFAULT ('Pending'),
        [Description] [nvarchar](500) NULL,
        [Reference] [nvarchar](100) NULL,
        [Provider] [nvarchar](50) NULL,
        [ProviderTransactionId] [nvarchar](100) NULL,
        [Metadata] [nvarchar](max) NULL,
        [ProcessedAt] [datetime] NULL,
        [CreatedAt] [datetime] NOT NULL CONSTRAINT [DF_Transactions_CreatedAt] DEFAULT (GETUTCDATE()),
        CONSTRAINT [PK_Transactions] PRIMARY KEY CLUSTERED ([Id] ASC),
        CONSTRAINT [UQ_Transactions_TransactionNumber] UNIQUE NONCLUSTERED ([TransactionNumber] ASC),
        CONSTRAINT [FK_Transactions_Users] FOREIGN KEY([UserId]) REFERENCES [dbo].[Users]([Id]),
        CONSTRAINT [CK_Transactions_Amount] CHECK ([Amount] > 0)
    );
    
    CREATE INDEX [IX_Transactions_UserId] ON [dbo].[Transactions]([UserId]);
    CREATE INDEX [IX_Transactions_Status] ON [dbo].[Transactions]([Status]);
    CREATE INDEX [IX_Transactions_CreatedAt] ON [dbo].[Transactions]([CreatedAt] DESC);
    CREATE INDEX [IX_Transactions_TransactionNumber] ON [dbo].[Transactions]([TransactionNumber]);
END
GO

-- =============================================
-- Insert Initial Data
-- =============================================

-- Insert default roles
IF NOT EXISTS (SELECT * FROM [dbo].[Roles] WHERE [Name] = 'Admin')
BEGIN
    INSERT INTO [dbo].[Roles] ([Name], [Description], [IsSystem])
    VALUES ('Admin', 'System administrator with full access', 1);
END
GO

IF NOT EXISTS (SELECT * FROM [dbo].[Roles] WHERE [Name] = 'User')
BEGIN
    INSERT INTO [dbo].[Roles] ([Name], [Description], [IsSystem])
    VALUES ('User', 'Standard user with limited access', 1);
END
GO

-- Record schema version
IF NOT EXISTS (SELECT * FROM [dbo].[SchemaVersion] WHERE [Version] = '1.0.0')
BEGIN
    INSERT INTO [dbo].[SchemaVersion] ([Version], [Description], [AppliedBy])
    VALUES ('1.0.0', 'Initial database schema', 'MDAN-AUTO');
END
GO

PRINT 'Database schema created successfully.';