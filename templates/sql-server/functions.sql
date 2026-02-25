-- =============================================
-- SQL Server Functions Template
-- Version: 1.0.0
-- =============================================

USE YourDatabaseName;
GO

-- =============================================
-- Scalar Functions
-- =============================================

-- Get User Full Name
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[fn_GetUserFullName]') AND type in (N'FN', N'IF', N'TF', N'FS', N'FT'))
DROP FUNCTION [dbo].[fn_GetUserFullName];
GO

CREATE FUNCTION [dbo].[fn_GetUserFullName](@UserId UNIQUEIDENTIFIER)
RETURNS NVARCHAR(250)
AS
BEGIN
    DECLARE @FullName NVARCHAR(250);
    
    SELECT @FullName = ISNULL([FirstName], '') + ' ' + ISNULL([LastName], '')
    FROM [dbo].[Users]
    WHERE [Id] = @UserId;
    
    RETURN LTRIM(RTRIM(@FullName));
END
GO

-- Format Currency Amount
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[fn_FormatCurrency]') AND type in (N'FN', N'IF', N'TF', N'FS', N'FT'))
DROP FUNCTION [dbo].[fn_FormatCurrency];
GO

CREATE FUNCTION [dbo].[fn_FormatCurrency](@Amount DECIMAL(18, 2), @Currency NVARCHAR(3))
RETURNS NVARCHAR(50)
AS
BEGIN
    RETURN @Currency + ' ' + CONVERT(NVARCHAR(50), @Amount, 1);
END
GO

-- Calculate Age from Date of Birth
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[fn_CalculateAge]') AND type in (N'FN', N'IF', N'TF', N'FS', N'FT'))
DROP FUNCTION [dbo].[fn_CalculateAge];
GO

CREATE FUNCTION [dbo].[fn_CalculateAge](@DateOfBirth DATE)
RETURNS INT
AS
BEGIN
    DECLARE @Age INT;
    
    SET @Age = DATEDIFF(YEAR, @DateOfBirth, GETDATE()) -
                CASE WHEN DATEADD(YEAR, DATEDIFF(YEAR, @DateOfBirth, GETDATE()), @DateOfBirth) > GETDATE()
                     THEN 1 ELSE 0 END;
    
    RETURN @Age;
END
GO

-- =============================================
-- Table-Valued Functions
-- =============================================

-- Get User Transactions
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[fn_GetUserTransactions]') AND type in (N'FN', N'IF', N'TF', N'FS', N'FT'))
DROP FUNCTION [dbo].[fn_GetUserTransactions];
GO

CREATE FUNCTION [dbo].[fn_GetUserTransactions](@UserId UNIQUEIDENTIFIER)
RETURNS TABLE
AS
RETURN
(
    SELECT 
        [Id], [TransactionNumber], [Type], [Amount], [Currency],
        [Status], [Description], [Reference], [Provider],
        [ProcessedAt], [CreatedAt]
    FROM [dbo].[Transactions]
    WHERE [UserId] = @UserId
    ORDER BY [CreatedAt] DESC
);
GO

-- Get User Roles
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[fn_GetUserRoles]') AND type in (N'FN', N'IF', N'TF', N'FS', N'FT'))
DROP FUNCTION [dbo].[fn_GetUserRoles];
GO

CREATE FUNCTION [dbo].[fn_GetUserRoles](@UserId UNIQUEIDENTIFIER)
RETURNS TABLE
AS
RETURN
(
    SELECT 
        r.[Id], r.[Name], r.[Description], ur.[AssignedAt]
    FROM [dbo].[UserRoles] ur
    INNER JOIN [dbo].[Roles] r ON ur.[RoleId] = r.[Id]
    WHERE ur.[UserId] = @UserId
);
GO

-- =============================================
-- Inline Table-Valued Functions
-- =============================================

-- Search Users
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[fn_SearchUsers]') AND type in (N'FN', N'IF', N'TF', N'FS', N'FT'))
DROP FUNCTION [dbo].[fn_SearchUsers];
GO

CREATE FUNCTION [dbo].[fn_SearchUsers](@SearchTerm NVARCHAR(100))
RETURNS TABLE
AS
RETURN
(
    SELECT 
        [Id], [Username], [Email], [FirstName], [LastName],
        [IsActive], [EmailVerified], [CreatedAt]
    FROM [dbo].[Users]
    WHERE 
        [Username] LIKE '%' + @SearchTerm + '%' OR
        [Email] LIKE '%' + @SearchTerm + '%' OR
        [FirstName] LIKE '%' + @SearchTerm + '%' OR
        [LastName] LIKE '%' + @SearchTerm + '%'
);
GO

-- Get Transactions by Date Range
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[fn_GetTransactionsByDateRange]') AND type in (N'FN', N'IF', N'TF', N'FS', N'FT'))
DROP FUNCTION [dbo].[fn_GetTransactionsByDateRange];
GO

CREATE FUNCTION [dbo].[fn_GetTransactionsByDateRange](
    @StartDate DATETIME,
    @EndDate DATETIME,
    @UserId UNIQUEIDENTIFIER = NULL
)
RETURNS TABLE
AS
RETURN
(
    SELECT 
        [Id], [TransactionNumber], [UserId], [Type], [Amount], [Currency],
        [Status], [Description], [Provider], [ProcessedAt], [CreatedAt]
    FROM [dbo].[Transactions]
    WHERE 
        [CreatedAt] >= @StartDate AND
        [CreatedAt] <= @EndDate AND
        (@UserId IS NULL OR [UserId] = @UserId)
    ORDER BY [CreatedAt] DESC
);
GO

PRINT 'Functions created successfully.';