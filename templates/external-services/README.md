# Templates d'Intégration de Services Externes

Ce répertoire contient des templates génériques pour intégrer des services externes dans les projets MDAN-AUTO.

## Vue d'Ensemble

Les templates fournis permettent d'intégrer n'importe quel service externe (API REST, services web, etc.) avec des patterns avancés intégrés:
- **Retry automatique** - Réessai automatique en cas d'échec
- **Circuit Breaker** - Protection contre les défaillances en cascade
- **Rate Limiting** - Limitation du taux de requêtes
- **Caching** - Mise en cache des réponses
- **Logging structuré** - Journalisation détaillée
- **Gestion des erreurs** - Gestion centralisée des exceptions

## Fichiers

- `IService.cs` - Interface générique pour tous les services externes
- `ServiceBase.cs` - Implémentation de base avec patterns avancés
- `ServiceProvider.cs` - Template pour implémenter un fournisseur spécifique
- `ExampleService.cs` - Exemple complet d'implémentation

## Installation

```bash
# Copier le template dans votre projet
cp -r templates/external-services src/Services/

# Ajouter les références nécessaires
cd src/Services/external-services
dotnet add package Microsoft.Extensions.Http
dotnet add package Microsoft.Extensions.Caching.Memory
dotnet add package Polly
```

## Configuration

### Configuration de Base (Un Service)

```json
{
  "ExternalServices": {
    "Default": {
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
  }
}
```

### Configuration Multiples Services

```json
{
  "ExternalServices": {
    "ServiceA": {
      "BaseUrl": "https://api.servicea.com/v1",
      "ApiKey": "service-a-key",
      "Timeout": 15,
      "RetryCount": 2,
      "EnableCircuitBreaker": true,
      "EnableRateLimiting": true,
      "RateLimitPerMinute": 100
    },
    "ServiceB": {
      "BaseUrl": "https://api.serviceb.com/v2",
      "ApiKey": "service-b-key",
      "Timeout": 45,
      "RetryCount": 5,
      "EnableCircuitBreaker": false,
      "EnableRateLimiting": false,
      "EnableCaching": false
    },
    "ServiceC": {
      "BaseUrl": "https://api.servicec.com/v1",
      "ApiKey": "service-c-key",
      "Timeout": 30,
      "RetryCount": 3,
      "EnableCircuitBreaker": true,
      "CircuitBreakerThreshold": 10,
      "EnableRateLimiting": true,
      "RateLimitPerMinute": 30,
      "EnableCaching": true,
      "CacheDurationMinutes": 10
    }
  }
}
```

## Utilisation

### 1. Implémenter un Service Spécifique

Créez une classe qui hérite de `ServiceBase`:

```csharp
using ExternalServices.Services;

public class MonService : ServiceBase
{
    public MonService(IConfiguration configuration, ILogger<MonService> logger)
        : base(configuration, "MonService", logger)
    {
    }

    public async Task<DonneesResponse> ObtenirDonneesAsync(int id)
    {
        return await GetDataAsync<DonneesResponse>($"donnees/{id}");
    }

    public async Task<Reponse> EnvoyerDonneesAsync(DonneesRequest request)
    {
        return await PostDataAsync<Reponse>("donnees", request);
    }
}
```

### 2. Enregistrer le Service

Dans `Program.cs` ou `Startup.cs`:

```csharp
// Enregistrer le service par défaut
builder.Services.AddScoped<IService, ExternalService>();

// Ou enregistrer un service spécifique
builder.Services.AddScoped<MonService>();
```

### 3. Utiliser le Service

```csharp
public class MonController : ControllerBase
{
    private readonly IService _service;

    public MonController(IService service)
    {
        _service = service;
    }

    [HttpGet]
    public async Task<IActionResult> Get()
    {
        await _service.AuthenticateAsync();
        var data = await _service.GetDataAsync<ResponseType>("endpoint");
        return Ok(data);
    }
}
```

## Patterns Implémentés

### Retry Automatique

Le service réessaie automatiquement les requêtes échouées:

```csharp
// Configuration
"RetryCount": 3,
"RetryDelay": 1000

// Comportement
// 1ère tentative -> Échec
// Attente 1000ms
// 2ème tentative -> Échec
// Attente 1000ms
// 3ème tentative -> Succès
```

### Circuit Breaker

Protection contre les défaillances en cascade:

```csharp
// Configuration
"EnableCircuitBreaker": true,
"CircuitBreakerThreshold": 5

// Comportement
// 5 échecs consécutifs -> Circuit ouvert
// Requêtes suivantes -> Échec immédiat (sans appel API)
// Après délai -> Tentative de rétablissement
```

### Rate Limiting

Limitation du taux de requêtes:

```csharp
// Configuration
"EnableRateLimiting": true,
"RateLimitPerMinute": 60

// Comportement
// Maximum 60 requêtes par minute
// Requêtes au-delà -> Mise en attente ou rejet
```

### Caching

Mise en cache des réponses:

```csharp
// Configuration
"EnableCaching": true,
"CacheDurationMinutes": 5

// Comportement
// 1ère requête -> Appel API + mise en cache
// Requêtes suivantes (5 min) -> Réponse depuis cache
```

## Modèles de Réponse

Tous les appels retournent un `ServiceResponse<T>`:

```csharp
public class ServiceResponse<T>
{
    public bool Success { get; set; }
    public T? Data { get; set; }
    public string? ErrorCode { get; set; }
    public string? ErrorMessage { get; set; }
    public DateTime Timestamp { get; set; }
    public int? StatusCode { get; set; }
}
```

## Gestion des Erreurs

Les erreurs sont gérées automatiquement:

- **Timeouts** - Retry automatique
- **5xx errors** - Retry automatique
- **4xx errors** - Pas de retry (erreur client)
- **Network errors** - Retry automatique
- **Circuit ouvert** - Échec immédiat

## Tests

### Tests Unitaires

```csharp
[Fact]
public async Task GetDataAsync_ShouldReturnData()
{
    // Arrange
    var service = new MonService(configuration, logger);
    
    // Act
    var result = await service.GetDataAsync<ResponseType>("endpoint");
    
    // Assert
    Assert.True(result.Success);
    Assert.NotNull(result.Data);
}
```

### Tests d'Intégration

```csharp
[Fact]
public async Task HealthCheckAsync_ShouldReturnTrue()
{
    // Arrange
    var service = new MonService(configuration, logger);
    
    // Act
    var result = await service.HealthCheckAsync();
    
    // Assert
    Assert.True(result);
}
```

## Bonnes Pratiques

1. **Toujours vérifier Success** avant d'utiliser les données
2. **Gérer les erreurs** avec try-catch pour les opérations critiques
3. **Utiliser le caching** pour les données qui changent rarement
4. **Configurer le retry** selon la criticité de l'opération
5. **Activer le circuit breaker** pour les services critiques
6. **Surveiller les logs** pour identifier les problèmes
7. **Tester en environnement sandbox** avant la production

## Sécurité

- **Jamais commiter** les clés API ou secrets
- **Toujours utiliser HTTPS** en production
- **Valider les entrées** avant envoi
- **Implémenter la rotation** des clés API
- **Utiliser des variables d'environnement** pour la configuration

## Dépannage

### Erreur: "Service non configuré"

Vérifiez que la configuration contient la section `ExternalServices` avec le nom de votre service.

### Erreur: "Circuit ouvert"

Le circuit breaker est ouvert suite à trop d'échecs. Attendez le délai de rétablissement ou vérifiez l'état du service externe.

### Erreur: "Rate limit exceeded"

Vous avez dépassé la limite de requêtes. Augmentez `RateLimitPerMinute` ou réduisez la fréquence des appels.

### Erreur: "Timeout"

Le service ne répond pas dans le délai imparti. Augmentez `Timeout` ou vérifiez la connectivité.

## Support

Pour plus d'informations ou de l'aide:
- Documentation MDAN: https://github.com/khalilbenaz/MDAN
- Issues: https://github.com/khalilbenaz/MDAN/issues