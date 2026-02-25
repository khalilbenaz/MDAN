using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace ExternalServices.Services
{
    /// <summary>
    /// Template pour implémenter un fournisseur de service spécifique.
    /// 
    /// Instructions:
    /// 1. Copiez ce fichier et renommez-le selon votre service (ex: MonService.cs)
    /// 2. Remplacez 'ServiceProvider' par le nom de votre service
    /// 3. Implémentez les méthodes spécifiques à votre service
    /// 4. Définissez les modèles de requête/réponse spécifiques
    /// </summary>
    public class ServiceProvider : ServiceBase
    {
        public ServiceProvider(
            IConfiguration configuration,
            ILogger<ServiceProvider> logger,
            IMemoryCache? cache = null)
            : base(configuration, "ServiceProvider", logger, cache)
        {
        }

        #region Méthodes Spécifiques au Service

        /// <summary>
        /// Exemple de méthode pour récupérer des données spécifiques.
        /// Remplacez cette méthode par vos propres méthodes métier.
        /// </summary>
        /// <param name="id">Identifiant de la ressource.</param>
        /// <returns>Données de la ressource.</returns>
        public async Task<ServiceResponse<RessponseData>> GetRessourceAsync(int id)
        {
            return await GetDataAsync<RessponseData>($"ressources/{id}");
        }

        /// <summary>
        /// Exemple de méthode pour créer une nouvelle ressource.
        /// Remplacez cette méthode par vos propres méthodes métier.
        /// </summary>
        /// <param name="request">Données de la ressource à créer.</param>
        /// <returns>Réponse du service.</returns>
        public async Task<ServiceResponse<CreateResponse>> CreateRessourceAsync(CreateRequest request)
        {
            return await PostDataAsync<CreateResponse>("ressources", request);
        }

        /// <summary>
        /// Exemple de méthode pour mettre à jour une ressource.
        /// Remplacez cette méthode par vos propres méthodes métier.
        /// </summary>
        /// <param name="id">Identifiant de la ressource.</param>
        /// <param name="request">Données de mise à jour.</param>
        /// <returns>Réponse du service.</returns>
        public async Task<ServiceResponse<UpdateResponse>> UpdateRessourceAsync(int id, UpdateRequest request)
        {
            return await PutDataAsync<UpdateResponse>($"ressources/{id}", request);
        }

        /// <summary>
        /// Exemple de méthode pour supprimer une ressource.
        /// Remplacez cette méthode par vos propres méthodes métier.
        /// </summary>
        /// <param name="id">Identifiant de la ressource.</param>
        /// <returns>Réponse du service.</returns>
        public async Task<ServiceResponse<DeleteResponse>> DeleteRessourceAsync(int id)
        {
            return await DeleteDataAsync<DeleteResponse>($"ressources/{id}");
        }

        /// <summary>
        /// Exemple de méthode pour rechercher des ressources.
        /// Remplacez cette méthode par vos propres méthodes métier.
        /// </summary>
        /// <param name="query">Terme de recherche.</param>
        /// <param name="page">Numéro de page.</param>
        /// <param name="pageSize">Taille de la page.</param>
        /// <returns>Liste des ressources.</returns>
        public async Task<ServiceResponse<SearchResponse>> SearchRessourcesAsync(
            string query, 
            int page = 1, 
            int pageSize = 20)
        {
            var parameters = new Dictionary<string, string>
            {
                { "q", query },
                { "page", page.ToString() },
                { "pageSize", pageSize.ToString() }
            };

            return await GetDataAsync<SearchResponse>("ressources/search", parameters);
        }

        #endregion

        #region Méthodes d'Authentification Spécifiques (Optionnel)

        /// <summary>
        /// Surchargez cette méthode si votre service utilise une authentification personnalisée.
        /// </summary>
        public override async Task AuthenticateAsync()
        {
            // Exemple d'authentification personnalisée
            // Supprimez cette méthode si vous utilisez l'authentification par défaut

            if (_accessToken != null && DateTime.UtcNow < _tokenExpiry)
            {
                return;
            }

            try
            {
                var authRequest = new
                {
                    ClientId = _configuration[$"ExternalServices:{_serviceName}:ClientId"],
                    ClientSecret = _configuration[$"ExternalServices:{_serviceName}:ClientSecret"],
                    GrantType = "client_credentials"
                };

                var response = await ExecuteWithRetryAsync(async () =>
                {
                    var json = System.Text.Json.JsonSerializer.Serialize(authRequest);
                    var content = new System.Net.Http.StringContent(
                        json, 
                        System.Text.Encoding.UTF8, 
                        "application/json");
                    return await _httpClient.PostAsync("oauth/token", content);
                });

                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    var authResponse = System.Text.Json.JsonSerializer.Deserialize<CustomAuthResponse>(responseContent);
                    
                    if (authResponse != null)
                    {
                        _accessToken = authResponse.AccessToken;
                        _tokenExpiry = DateTime.UtcNow.AddSeconds(authResponse.ExpiresIn);
                        _status.IsAuthenticated = true;
                        _logger.LogInformation("Authenticated successfully for {ServiceName}", _serviceName);
                    }
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Authentication error for {ServiceName}", _serviceName);
                throw;
            }
        }

        #endregion

        #region Modèles de Requête/Réponse Spécifiques

        /// <summary>
        /// Modèle de réponse pour une ressource.
        /// Définissez vos propres modèles selon votre service.
        /// </summary>
        public class RessponseData
        {
            public int Id { get; set; }
            public string Name { get; set; } = string.Empty;
            public string Description { get; set; } = string.Empty;
            public DateTime CreatedAt { get; set; }
            public DateTime? UpdatedAt { get; set; }
        }

        /// <summary>
        /// Modèle de requête pour créer une ressource.
        /// </summary>
        public class CreateRequest
        {
            public string Name { get; set; } = string.Empty;
            public string Description { get; set; } = string.Empty;
        }

        /// <summary>
        /// Modèle de réponse de création.
        /// </summary>
        public class CreateResponse
        {
            public int Id { get; set; }
            public bool Success { get; set; }
            public string Message { get; set; } = string.Empty;
        }

        /// <summary>
        /// Modèle de requête pour mettre à jour une ressource.
        /// </summary>
        public class UpdateRequest
        {
            public string Name { get; set; } = string.Empty;
            public string Description { get; set; } = string.Empty;
        }

        /// <summary>
        /// Modèle de réponse de mise à jour.
        /// </summary>
        public class UpdateResponse
        {
            public bool Success { get; set; }
            public string Message { get; set; } = string.Empty;
        }

        /// <summary>
        /// Modèle de réponse de suppression.
        /// </summary>
        public class DeleteResponse
        {
            public bool Success { get; set; }
            public string Message { get; set; } = string.Empty;
        }

        /// <summary>
        /// Modèle de réponse de recherche.
        /// </summary>
        public class SearchResponse
        {
            public List<RessponseData> Items { get; set; } = new();
            public int TotalCount { get; set; }
            public int Page { get; set; }
            public int PageSize { get; set; }
            public int TotalPages { get; set; }
        }

        /// <summary>
        /// Modèle de réponse d'authentification personnalisée.
        /// </summary>
        public class CustomAuthResponse
        {
            public string AccessToken { get; set; } = string.Empty;
            public string TokenType { get; set; } = string.Empty;
            public int ExpiresIn { get; set; }
            public string RefreshToken { get; set; } = string.Empty;
        }

        #endregion
    }
}