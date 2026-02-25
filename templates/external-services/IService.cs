using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace ExternalServices.Services
{
    /// <summary>
    /// Interface générique pour les services externes.
    /// Fournit les opérations de base pour interagir avec n'importe quel service externe.
    /// </summary>
    public interface IService
    {
        /// <summary>
        /// Nom du service.
        /// </summary>
        string ServiceName { get; }

        /// <summary>
        /// URL de base du service.
        /// </summary>
        string BaseUrl { get; }

        /// <summary>
        /// Authentifie le service auprès du fournisseur.
        /// </summary>
        /// <returns>Tâche asynchrone.</returns>
        Task AuthenticateAsync();

        /// <summary>
        /// Vérifie si le service est authentifié.
        /// </summary>
        /// <returns>True si authentifié, false sinon.</returns>
        Task<bool> IsAuthenticatedAsync();

        /// <summary>
        /// Récupère des données depuis un endpoint.
        /// </summary>
        /// <typeparam name="T">Type de données attendu.</typeparam>
        /// <param name="endpoint">Endpoint à appeler.</param>
        /// <param name="parameters">Paramètres de requête optionnels.</param>
        /// <returns>Réponse du service.</returns>
        Task<ServiceResponse<T>> GetDataAsync<T>(string endpoint, Dictionary<string, string>? parameters = null);

        /// <summary>
        /// Envoie des données à un endpoint via POST.
        /// </summary>
        /// <typeparam name="T">Type de réponse attendu.</typeparam>
        /// <param name="endpoint">Endpoint à appeler.</param>
        /// <param name="data">Données à envoyer.</param>
        /// <returns>Réponse du service.</returns>
        Task<ServiceResponse<T>> PostDataAsync<T>(string endpoint, object data);

        /// <summary>
        /// Met à jour des données via PUT.
        /// </summary>
        /// <typeparam name="T">Type de réponse attendu.</typeparam>
        /// <param name="endpoint">Endpoint à appeler.</param>
        /// <param name="data">Données à envoyer.</param>
        /// <returns>Réponse du service.</returns>
        Task<ServiceResponse<T>> PutDataAsync<T>(string endpoint, object data);

        /// <summary>
        /// Supprime des données via DELETE.
        /// </summary>
        /// <typeparam name="T">Type de réponse attendu.</typeparam>
        /// <param name="endpoint">Endpoint à appeler.</param>
        /// <returns>Réponse du service.</returns>
        Task<ServiceResponse<T>> DeleteDataAsync<T>(string endpoint);

        /// <summary>
        /// Vérifie la santé du service.
        /// </summary>
        /// <returns>True si le service est sain, false sinon.</returns>
        Task<bool> HealthCheckAsync();

        /// <summary>
        /// Récupère le statut détaillé du service.
        /// </summary>
        /// <returns>Statut du service.</returns>
        Task<ServiceStatus> GetStatusAsync();
    }

    /// <summary>
    /// Réponse générique d'un service externe.
    /// </summary>
    /// <typeparam name="T">Type des données.</typeparam>
    public class ServiceResponse<T>
    {
        public bool Success { get; set; }
        public T? Data { get; set; }
        public string? ErrorCode { get; set; }
        public string? ErrorMessage { get; set; }
        public DateTime Timestamp { get; set; }
        public int? StatusCode { get; set; }
        public Dictionary<string, string>? Headers { get; set; }
    }

    /// <summary>
    /// Statut d'un service externe.
    /// </summary>
    public class ServiceStatus
    {
        public bool IsHealthy { get; set; }
        public bool IsAuthenticated { get; set; }
        public bool IsCircuitOpen { get; set; }
        public DateTime? LastSuccessfulCall { get; set; }
        public DateTime? LastFailedCall { get; set; }
        public int ConsecutiveFailures { get; set; }
        public int TotalCalls { get; set; }
        public int SuccessfulCalls { get; set; }
        public int FailedCalls { get; set; }
    }
}