# Auto Phase 4: ARCHITECT

> Design system architecture

## Objective

Design the system architecture, including components, data models, security, and deployment strategy.

## Tasks

### 4.1 Design System Architecture

- Define system components
- Design component interactions
- Create architecture diagrams
- Define data flow

### 4.2 Design Data Models

- Create entity models
- Define relationships
- Design database schema
- Plan migrations

### 4.3 Design Security Architecture

- Define authentication flow
- Design authorization model
- Plan security controls
- Define encryption strategy

### 4.4 Design API Architecture

- Define API endpoints
- Design request/response models
- Plan API versioning
- Define error handling

### 4.5 Design Deployment Architecture

- Define deployment strategy
- Design infrastructure
- Plan scaling approach
- Define monitoring strategy

## Output

Generate `docs/architecture.md`:

```markdown
# System Architecture

## Overview

[High-level architecture description]

## System Components

### Frontend

**Blazor Server Application**
- User interface
- State management
- Client-side validation
- Real-time updates via SignalR

### Backend

**ASP.NET Core Web API**
- RESTful API endpoints
- Business logic
- Data access layer
- Authentication/authorization

### Database

**SQL Server 2022**
- User data
- Transaction records
- Audit logs
- Configuration data

### External Services

- Azure AD (authentication)
- Generic external services (configurable)
- Azure Key Vault (secrets)

## Architecture Diagram

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────┐
│  Azure App      │
│  Service        │
│  (Blazor Server)│
└──────┬──────────┘
       │ SignalR
       ▼
┌─────────────────┐
│  ASP.NET Core   │
│  Web API        │
└──────┬──────────┘
       │
├─────────────┬─────────────┬─────────────┐
        ▼             ▼             ▼             ▼
 ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
 │Azure AD  │  │External  │  │External  │  │Key Vault │
 │          │  │Service 1 │  │Service 2 │  │          │
 └──────────┘  └──────────┘  └──────────┘  └──────────┘
       │
       ▼
┌─────────────────┐
│  SQL Server     │
│  Database       │
└─────────────────┘
```

## Data Models

### User

```csharp
public class User
{
    public int Id { get; set; }
    public string AzureAdId { get; set; }
    public string Email { get; set; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public string Role { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? LastLoginAt { get; set; }
}
```

### ExternalService

```csharp
public class ExternalService
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string BaseUrl { get; set; }
    public string ApiKey { get; set; }
    public int Timeout { get; set; }
    public int RetryCount { get; set; }
    public int RetryDelay { get; set; }
    public bool EnableCircuitBreaker { get; set; }
    public int CircuitBreakerThreshold { get; set; }
    public bool EnableRateLimiting { get; set; }
    public int RateLimitPerMinute { get; set; }
    public bool EnableCaching { get; set; }
    public int CacheDurationMinutes { get; set; }
    public bool IsActive { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? LastSyncAt { get; set; }

    public User User { get; set; }
}
```

### ServiceActivity

```csharp
public class ServiceActivity
{
    public int Id { get; set; }
    public int ExternalServiceId { get; set; }
    public string Type { get; set; } // request, response, error
    public string Endpoint { get; set; }
    public string Method { get; set; }
    public int StatusCode { get; set; }
    public long ResponseTime { get; set; }
    public string? Description { get; set; }
    public DateTime CreatedAt { get; set; }

    public ExternalService ExternalService { get; set; }
}
```

### Notification

```csharp
public class Notification
{
    public int Id { get; set; }
    public int UserId { get; set; }
    public string Type { get; set; }
    public string Title { get; set; }
    public string Message { get; set; }
    public bool IsRead { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? ReadAt { get; set; }

    public User User { get; set; }
}
```

## Database Schema

### Tables

**Users**
- Id (PK, int, identity)
- AzureAdId (nvarchar(100), unique)
- Email (nvarchar(255), unique)
- FirstName (nvarchar(100))
- LastName (nvarchar(100))
- Role (nvarchar(50))
- CreatedAt (datetime2)
- LastLoginAt (datetime2, nullable)

**ExternalServices**
- Id (PK, int, identity)
- UserId (FK, int)
- Name (nvarchar(100))
- BaseUrl (nvarchar(500))
- ApiKey (nvarchar(500))
- Timeout (int)
- RetryCount (int)
- RetryDelay (int)
- EnableCircuitBreaker (bit)
- CircuitBreakerThreshold (int)
- EnableRateLimiting (bit)
- RateLimitPerMinute (int)
- EnableCaching (bit)
- CacheDurationMinutes (int)
- IsActive (bit)
- CreatedAt (datetime2)
- LastSyncAt (datetime2, nullable)

**ServiceActivities**
- Id (PK, int, identity)
- ExternalServiceId (FK, int)
- Type (nvarchar(20))
- Endpoint (nvarchar(500))
- Method (nvarchar(10))
- StatusCode (int)
- ResponseTime (bigint)
- Description (nvarchar(1000))
- CreatedAt (datetime2)

**Notifications**
- Id (PK, int, identity)
- UserId (FK, int)
- Type (nvarchar(50))
- Title (nvarchar(200))
- Message (nvarchar(1000))
- IsRead (bit)
- CreatedAt (datetime2)
- ReadAt (datetime2, nullable)

### Indexes

- IX_Users_AzureAdId on Users(AzureAdId)
- IX_Users_Email on Users(Email)
- IX_ExternalServices_UserId on ExternalServices(UserId)
- IX_ServiceActivities_ExternalServiceId on ServiceActivities(ExternalServiceId)
- IX_ServiceActivities_CreatedAt on ServiceActivities(CreatedAt)
- IX_Notifications_UserId on Notifications(UserId)
- IX_Notifications_IsRead on Notifications(IsRead)

## Security Architecture

### Authentication Flow

```
1. User navigates to application
2. Redirected to Azure AD login
3. User authenticates with Azure AD
4. Azure AD returns JWT token
5. Token validated by application
6. User session established
7. User can access protected resources
```

### Authorization Model

**Roles**:
- Admin: Full access
- User: Standard access
- Viewer: Read-only access

**Permissions**:
- Users: Read, Create, Update, Delete
- External Services: Read, Create, Update, Delete
- Service Activities: Read
- Notifications: Read, Update

### Security Controls

- **Authentication**: Azure AD with JWT tokens
- **Authorization**: Role-based access control (RBAC)
- **Encryption**: TLS 1.3 for data in transit, AES-256 for data at rest
- **Input Validation**: Server-side validation for all inputs
- **Output Encoding**: Encode all outputs to prevent XSS
- **SQL Injection Prevention**: Parameterized queries
- **CSRF Protection**: Anti-forgery tokens
- **Rate Limiting**: API rate limiting
- **Audit Logging**: All actions logged
- **Secrets Management**: Azure Key Vault

## API Architecture

### Endpoints

**Authentication**
- POST /api/auth/login - Login with Azure AD
- POST /api/auth/logout - Logout
- GET /api/auth/me - Get current user

**Users**
- GET /api/users - List users (Admin)
- GET /api/users/{id} - Get user details
- PUT /api/users/{id} - Update user
- DELETE /api/users/{id} - Delete user (Admin)

**External Services**
- GET /api/external-services - List external services
- GET /api/external-services/{id} - Get service details
- POST /api/external-services - Add service
- PUT /api/external-services/{id} - Update service
- DELETE /api/external-services/{id} - Delete service
- GET /api/external-services/{id}/status - Get service status

**Service Activities**
- GET /api/service-activities - List service activities
- GET /api/service-activities/{id} - Get activity details
- GET /api/external-services/{id}/activities - Get service activities

**Notifications**
- GET /api/notifications - List notifications
- GET /api/notifications/{id} - Get notification
- PUT /api/notifications/{id}/read - Mark as read
- PUT /api/notifications/read-all - Mark all as read

### Request/Response Models

**User Response**
```json
{
  "id": 1,
  "email": "user@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "role": "User",
  "createdAt": "2024-01-15T10:00:00Z"
}
```

**External Service Response**
```json
{
  "id": 1,
  "name": "ServiceName",
  "baseUrl": "https://api.example.com/v1",
  "status": "Active",
  "lastSyncAt": "2024-01-15T10:00:00Z"
}
```

**Service Activity Response**
```json
{
  "id": 1,
  "externalServiceId": 1,
  "type": "request",
  "endpoint": "/api/data",
  "method": "GET",
  "statusCode": 200,
  "responseTime": 150,
  "createdAt": "2024-01-15T10:00:00Z"
}
```

### Error Handling

**Error Response Format**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {
        "field": "email",
        "message": "Email is required"
      }
    ]
  }
}
```

**Error Codes**
- VALIDATION_ERROR (400)
- UNAUTHORIZED (401)
- FORBIDDEN (403)
- NOT_FOUND (404)
- CONFLICT (409)
- INTERNAL_ERROR (500)

## Deployment Architecture

### Azure Resources

**App Service**
- Blazor Server application
- ASP.NET Core Web API
- Scaling: Auto-scale based on CPU/memory
- Deployment slots: Production, Staging

**SQL Database**
- Azure SQL Database
- Tier: Standard S2
- Geo-replication: Enabled
- Backup: 7-day retention

**Key Vault**
- Store secrets (API keys, connection strings)
- Access policies: RBAC
- Soft delete: Enabled

**Application Insights**
- Monitoring and logging
- Performance tracking
- Error tracking
- Usage analytics

### Deployment Strategy

**CI/CD Pipeline**
1. Code pushed to GitHub
2. Azure DevOps build triggered
3. Run tests
4. Build application
5. Deploy to staging
6. Run smoke tests
7. Deploy to production

**Blue-Green Deployment**
- Zero downtime deployments
- Instant rollback capability
- Traffic routing via Azure Front Door

### Scaling Strategy

**Horizontal Scaling**
- Auto-scale based on metrics
- Scale out: Add instances
- Scale in: Remove instances

**Vertical Scaling**
- Upgrade App Service plan
- Increase database DTUs
- Monitor performance

## Monitoring Strategy

### Metrics to Monitor

- Application performance
- Response times
- Error rates
- Database performance
- API usage
- User activity

### Alerts

- High error rate (>5%)
- Slow response times (>2s)
- Database connection issues
- Authentication failures
- API rate limit breaches

### Logging

- Application logs
- Audit logs
- Security logs
- Performance logs

## Technology Stack

- **Frontend**: Blazor Server, .NET 8.0
- **Backend**: ASP.NET Core Web API, .NET 8.0
- **Database**: SQL Server 2022, Entity Framework Core
- **Authentication**: Azure AD, JWT
- **Cloud**: Azure App Service, Azure SQL Database
- **CI/CD**: Azure DevOps
- **Monitoring**: Application Insights

## Next Steps

Proceed to IMPLEMENT phase.
```

## Quality Gates

- [ ] Architecture documented
- [ ] Data models defined
- [ ] Security designed
- [ ] API designed
- [ ] Deployment planned

## Success Criteria

- Architecture is clear and complete
- Data models cover all requirements
- Security is comprehensive
- API is well-defined
- Deployment is feasible

## Error Handling

### Architecture Conflicts

- Trigger debate
- Resolve conflict
- Document decision
- Continue

### Missing Components

- Log warning
- Add placeholder
- Document gap
- Continue

## Token Management

Track token usage:
- Architecture design: ~6,000 tokens
- Data models: ~4,000 tokens
- Security design: ~4,000 tokens
- API design: ~4,000 tokens
- Deployment design: ~3,000 tokens

Total: ~21,000 tokens

## Logging

```
[timestamp] Starting ARCHITECT phase
[timestamp] Designing system architecture...
[timestamp] Designing data models...
[timestamp] Designing security architecture...
[timestamp] Designing API architecture...
[timestamp] Designing deployment architecture...
[timestamp] Token usage: X / 128,000 (X%)
[timestamp] ARCHITECT phase complete
```

## Completion Signal

```
PHASE 4 COMPLETE ✅
```

## Version

MDAN-AUTO Phase 4: ARCHITECT v1.0