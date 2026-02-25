# .NET 8.0 Blazor Server Project Template

## Project Structure

```
MyProject/
├── MyProject.sln
├── src/
│   ├── MyProject.Server/
│   │   ├── Program.cs
│   │   ├── Startup.cs
│   │   ├── appsettings.json
│   │   ├── appsettings.Development.json
│   │   ├── appsettings.Production.json
│   │   ├── Data/
│   │   │   └── ApplicationDbContext.cs
│   │   ├── Models/
│   │   ├── Controllers/
│   │   ├── Pages/
│   │   ├── Services/
│   │   └── wwwroot/
│   │       ├── css/
│   │       ├── js/
│   │       └── lib/
│   ├── MyProject.Shared/
│   │   └── Models/
│   └── MyProject.Client/
│       └── Components/
└── tests/
    ├── MyProject.Tests/
    └── MyProject.IntegrationTests/
```

## Program.cs

```csharp
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.Identity.Web;
using Microsoft.EntityFrameworkCore;
using MyProject.Server.Data;
using MyProject.Server.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddAuthentication(OpenIdConnectDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApp(builder.Configuration.GetSection("AzureAd"));

builder.Services.AddAuthorization();

builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor()
    .AddMicrosoftIdentityConsentHandler();

builder.Services.AddControllersWithViews();

// Database
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Services
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddScoped<INotificationService, NotificationService>();

// External Services (Generic)
builder.Services.AddHttpClient<IExternalService, ExternalService>();

// SignalR
builder.Services.AddSignalR();

var app = builder.Build();

// Configure pipeline
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();
app.MapBlazorHub();
app.MapFallbackToPage("/_Host");

app.Run();
```

## appsettings.json

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=MyProjectDb;Trusted_Connection=True;MultipleActiveResultSets=true"
  },
  "AzureAd": {
    "Instance": "https://login.microsoftonline.com/",
    "Domain": "yourdomain.onmicrosoft.com",
    "TenantId": "your-tenant-id",
    "ClientId": "your-client-id",
    "CallbackPath": "/signin-oidc",
    "SignedOutCallbackPath": "/signout-callback-oidc"
  },
  "ExternalServices": {
    "ServiceName": {
      "BaseUrl": "https://api.example.com/v1",
      "ApiKey": "your-api-key",
      "Timeout": 30,
      "RetryCount": 3,
      "RetryDelay": 1000,
      "EnableCircuitBreaker": true,
      "CircuitBreakerThreshold": 5,
      "EnableRateLimiting": true,
      "RateLimitPerMinute": 60,
      "EnableCaching": true,
      "CacheDurationMinutes": 5
    }
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```

## ApplicationDbContext.cs

```csharp
using Microsoft.EntityFrameworkCore;
using MyProject.Server.Models;

namespace MyProject.Server.Data;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<User> Users { get; set; }
    public DbSet<Notification> Notifications { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // User configuration
        modelBuilder.Entity<User>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.AzureAdId).IsUnique();
            entity.HasIndex(e => e.Email).IsUnique();
        });

        // Notification configuration
        modelBuilder.Entity<Notification>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasOne(e => e.User)
                  .WithMany(u => u.Notifications)
                  .HasForeignKey(e => e.UserId)
                  .OnDelete(DeleteBehavior.Cascade);
            entity.HasIndex(e => e.UserId);
            entity.HasIndex(e => e.IsRead);
        });
    }
}
```

## User Model

```csharp
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MyProject.Server.Models;

public class User
{
    [Key]
    public int Id { get; set; }

    [Required]
    [MaxLength(100)]
    public string AzureAdId { get; set; } = string.Empty;

    [Required]
    [MaxLength(255)]
    public string Email { get; set; } = string.Empty;

    [MaxLength(100)]
    public string? FirstName { get; set; }

    [MaxLength(100)]
    public string? LastName { get; set; }

    [MaxLength(50)]
    public string Role { get; set; } = "User";

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public DateTime? LastLoginAt { get; set; }

    // Navigation properties
    public ICollection<Notification> Notifications { get; set; } = new List<Notification>();
}
```

## Notification Model

```csharp
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MyProject.Server.Models;

public class Notification
{
    [Key]
    public int Id { get; set; }

    [Required]
    public int UserId { get; set; }

    [MaxLength(50)]
    public string Type { get; set; } = string.Empty;

    [MaxLength(200)]
    public string Title { get; set; } = string.Empty;

    [MaxLength(1000)]
    public string Message { get; set; } = string.Empty;

    public bool IsRead { get; set; } = false;

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public DateTime? ReadAt { get; set; }

    // Navigation properties
    [ForeignKey(nameof(UserId))]
    public User? User { get; set; }
}
```

## UserService.cs

```csharp
using Microsoft.EntityFrameworkCore;
using MyProject.Server.Data;
using MyProject.Server.Models;

namespace MyProject.Server.Services;

public interface IUserService
{
    Task<User?> GetUserByAzureAdIdAsync(string azureAdId);
    Task<User?> GetUserByIdAsync(int id);
    Task<IEnumerable<User>> GetAllUsersAsync();
    Task<User> CreateUserAsync(User user);
    Task<User?> UpdateUserAsync(int id, User user);
    Task<bool> DeleteUserAsync(int id);
    Task UpdateLastLoginAsync(int id);
}

public class UserService : IUserService
{
    private readonly ApplicationDbContext _context;

    public UserService(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<User?> GetUserByAzureAdIdAsync(string azureAdId)
    {
        return await _context.Users
            .FirstOrDefaultAsync(u => u.AzureAdId == azureAdId);
    }

    public async Task<User?> GetUserByIdAsync(int id)
    {
        return await _context.Users
            .FirstOrDefaultAsync(u => u.Id == id);
    }

    public async Task<IEnumerable<User>> GetAllUsersAsync()
    {
        return await _context.Users
            .OrderBy(u => u.CreatedAt)
            .ToListAsync();
    }

    public async Task<User> CreateUserAsync(User user)
    {
        user.CreatedAt = DateTime.UtcNow;
        _context.Users.Add(user);
        await _context.SaveChangesAsync();
        return user;
    }

    public async Task<User?> UpdateUserAsync(int id, User user)
    {
        var existing = await _context.Users.FindAsync(id);
        if (existing == null) return null;

        existing.Email = user.Email;
        existing.FirstName = user.FirstName;
        existing.LastName = user.LastName;
        existing.Role = user.Role;

        await _context.SaveChangesAsync();
        return existing;
    }

    public async Task<bool> DeleteUserAsync(int id)
    {
        var user = await _context.Users.FindAsync(id);
        if (user == null) return false;

        _context.Users.Remove(user);
        await _context.SaveChangesAsync();
        return true;
    }

    public async Task UpdateLastLoginAsync(int id)
    {
        var user = await _context.Users.FindAsync(id);
        if (user != null)
        {
            user.LastLoginAt = DateTime.UtcNow;
            await _context.SaveChangesAsync();
        }
    }
}
```

## Migration Commands

```bash
# Add migration
dotnet ef migrations add InitialCreate --project src/MyProject.Server

# Update database
dotnet ef database update --project src/MyProject.Server

# Create SQL script
dotnet ef migrations script --project src/MyProject.Server --output migration.sql
```

## Build Commands

```bash
# Build solution
dotnet build

# Run application
dotnet run --project src/MyProject.Server

# Publish for production
dotnet publish src/MyProject.Server -c Release -o ./publish
```

## Testing Commands

```bash
# Run all tests
dotnet test

# Run with coverage
dotnet test --collect:"XPlat Code Coverage"
```

## Docker Support

```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["src/MyProject.Server/MyProject.Server.csproj", "src/MyProject.Server/"]
RUN dotnet restore "src/MyProject.Server/MyProject.Server.csproj"
COPY . .
WORKDIR "/src/src/MyProject.Server"
RUN dotnet build "MyProject.Server.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "MyProject.Server.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "MyProject.Server.dll"]
```

## Version

.NET 8.0 Blazor Server Template v1.0