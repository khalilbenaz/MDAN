using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace ExternalServices.Services
{
    /// <summary>
    /// Exemple complet d'implémentation d'un service externe.
    /// 
    /// Ce service exemple montre comment intégrer une API hypothétique "ApiExemple"
    /// en utilisant le template ServiceProvider.
    /// 
    /// Fonctionnalités démontrées:
    /// - Authentification avec token
    /// - CRUD complet (Create, Read, Update, Delete)
    /// - Recherche avec pagination
    /// - Gestion des erreurs
    /// - Utilisation des patterns (retry, circuit breaker, rate limiting, caching)
    /// </summary>
    public class ExampleService : ServiceBase
    {
        public ExampleService(
            IConfiguration configuration,
            ILogger<ExampleService> logger,
            IMemoryCache? cache = null)
            : base(configuration, "ExampleService", logger, cache)
        {
        }

        #region Opérations CRUD

        /// <summary>
        /// Récupère un produit par son ID.
        /// </summary>
        /// <param name="productId">ID du produit.</param>
        /// <returns>Informations du produit.</returns>
        public async Task<ServiceResponse<Product>> GetProductAsync(int productId)
        {
            _logger.LogInformation("Fetching product {ProductId}", productId);
            
            var response = await GetDataAsync<Product>($"products/{productId}");
            
            if (response.Success)
            {
                _logger.LogInformation("Product {ProductId} fetched successfully", productId);
            }
            else
            {
                _logger.LogWarning("Failed to fetch product {ProductId}: {Error}", 
                    productId, response.ErrorMessage);
            }
            
            return response;
        }

        /// <summary>
        /// Récupère la liste des produits avec pagination.
        /// </summary>
        /// <param name="page">Numéro de page (défaut: 1).</param>
        /// <param name="pageSize">Taille de la page (défaut: 20).</param>
        /// <param name="category">Filtre par catégorie (optionnel).</param>
        /// <returns>Liste des produits.</returns>
        public async Task<ServiceResponse<ProductListResponse>> GetProductsAsync(
            int page = 1, 
            int pageSize = 20,
            string? category = null)
        {
            _logger.LogInformation("Fetching products - Page: {Page}, Size: {PageSize}, Category: {Category}",
                page, pageSize, category ?? "All");

            var parameters = new Dictionary<string, string>
            {
                { "page", page.ToString() },
                { "pageSize", pageSize.ToString() }
            };

            if (!string.IsNullOrEmpty(category))
            {
                parameters.Add("category", category);
            }

            var response = await GetDataAsync<ProductListResponse>("products", parameters);
            
            if (response.Success)
            {
                _logger.LogInformation("Fetched {Count} products", response.Data?.Items?.Count ?? 0);
            }
            
            return response;
        }

        /// <summary>
        /// Crée un nouveau produit.
        /// </summary>
        /// <param name="request">Données du produit à créer.</param>
        /// <returns>Produit créé avec son ID.</returns>
        public async Task<ServiceResponse<ProductCreateResponse>> CreateProductAsync(CreateProductRequest request)
        {
            _logger.LogInformation("Creating product: {ProductName}", request.Name);

            var response = await PostDataAsync<ProductCreateResponse>("products", request);
            
            if (response.Success)
            {
                _logger.LogInformation("Product created successfully with ID: {ProductId}", 
                    response.Data?.ProductId);
            }
            else
            {
                _logger.LogError("Failed to create product: {Error}", response.ErrorMessage);
            }
            
            return response;
        }

        /// <summary>
        /// Met à jour un produit existant.
        /// </summary>
        /// <param name="productId">ID du produit à mettre à jour.</param>
        /// <param name="request">Données de mise à jour.</param>
        /// <returns>Résultat de la mise à jour.</returns>
        public async Task<ServiceResponse<ProductUpdateResponse>> UpdateProductAsync(
            int productId, 
            UpdateProductRequest request)
        {
            _logger.LogInformation("Updating product {ProductId}", productId);

            var response = await PutDataAsync<ProductUpdateResponse>($"products/{productId}", request);
            
            if (response.Success)
            {
                _logger.LogInformation("Product {ProductId} updated successfully", productId);
            }
            else
            {
                _logger.LogError("Failed to update product {ProductId}: {Error}", 
                    productId, response.ErrorMessage);
            }
            
            return response;
        }

        /// <summary>
        /// Supprime un produit.
        /// </summary>
        /// <param name="productId">ID du produit à supprimer.</param>
        /// <returns>Résultat de la suppression.</returns>
        public async Task<ServiceResponse<ProductDeleteResponse>> DeleteProductAsync(int productId)
        {
            _logger.LogInformation("Deleting product {ProductId}", productId);

            var response = await DeleteDataAsync<ProductDeleteResponse>($"products/{productId}");
            
            if (response.Success)
            {
                _logger.LogInformation("Product {ProductId} deleted successfully", productId);
            }
            else
            {
                _logger.LogError("Failed to delete product {ProductId}: {Error}", 
                    productId, response.ErrorMessage);
            }
            
            return response;
        }

        #endregion

        #region Recherche

        /// <summary>
        /// Recherche des produits par terme de recherche.
        /// </summary>
        /// <param name="query">Terme de recherche.</param>
        /// <param name="page">Numéro de page (défaut: 1).</param>
        /// <param name="pageSize">Taille de la page (défaut: 20).</param>
        /// <returns>Résultats de recherche.</returns>
        public async Task<ServiceResponse<ProductListResponse>> SearchProductsAsync(
            string query,
            int page = 1,
            int pageSize = 20)
        {
            _logger.LogInformation("Searching products with query: {Query}", query);

            var parameters = new Dictionary<string, string>
            {
                { "q", query },
                { "page", page.ToString() },
                { "pageSize", pageSize.ToString() }
            };

            var response = await GetDataAsync<ProductListResponse>("products/search", parameters);
            
            if (response.Success)
            {
                _logger.LogInformation("Search returned {Count} results", 
                    response.Data?.Items?.Count ?? 0);
            }
            
            return response;
        }

        #endregion

        #region Opérations Spécifiques

        /// <summary>
        /// Récupère les catégories de produits.
        /// </summary>
        /// <returns>Liste des catégories.</returns>
        public async Task<ServiceResponse<List<Category>>> GetCategoriesAsync()
        {
            _logger.LogInformation("Fetching categories");

            var response = await GetDataAsync<List<Category>>("categories");
            
            if (response.Success)
            {
                _logger.LogInformation("Fetched {Count} categories", response.Data?.Count ?? 0);
            }
            
            return response;
        }

        /// <summary>
        /// Récupère les statistiques des produits.
        /// </summary>
        /// <returns>Statistiques.</returns>
        public async Task<ServiceResponse<ProductStatistics>> GetStatisticsAsync()
        {
            _logger.LogInformation("Fetching product statistics");

            var response = await GetDataAsync<ProductStatistics>("products/statistics");
            
            if (response.Success)
            {
                _logger.LogInformation("Statistics fetched: Total={Total}, Active={Active}",
                    response.Data?.TotalProducts, response.Data?.ActiveProducts);
            }
            
            return response;
        }

        #endregion

        #region Modèles de Données

        /// <summary>
        /// Modèle de produit.
        /// </summary>
        public class Product
        {
            public int Id { get; set; }
            public string Name { get; set; } = string.Empty;
            public string Description { get; set; } = string.Empty;
            public decimal Price { get; set; }
            public string Currency { get; set; } = "EUR";
            public string Category { get; set; } = string.Empty;
            public bool IsActive { get; set; }
            public int Stock { get; set; }
            public DateTime CreatedAt { get; set; }
            public DateTime? UpdatedAt { get; set; }
        }

        /// <summary>
        /// Modèle de réponse de liste de produits.
        /// </summary>
        public class ProductListResponse
        {
            public List<Product> Items { get; set; } = new();
            public int TotalCount { get; set; }
            public int Page { get; set; }
            public int PageSize { get; set; }
            public int TotalPages { get; set; }
        }

        /// <summary>
        /// Modèle de requête pour créer un produit.
        /// </summary>
        public class CreateProductRequest
        {
            public string Name { get; set; } = string.Empty;
            public string Description { get; set; } = string.Empty;
            public decimal Price { get; set; }
            public string Currency { get; set; } = "EUR";
            public string Category { get; set; } = string.Empty;
            public int Stock { get; set; }
        }

        /// <summary>
        /// Modèle de réponse de création de produit.
        /// </summary>
        public class ProductCreateResponse
        {
            public int ProductId { get; set; }
            public bool Success { get; set; }
            public string Message { get; set; } = string.Empty;
        }

        /// <summary>
        /// Modèle de requête pour mettre à jour un produit.
        /// </summary>
        public class UpdateProductRequest
        {
            public string Name { get; set; } = string.Empty;
            public string Description { get; set; } = string.Empty;
            public decimal Price { get; set; }
            public string Currency { get; set; } = "EUR";
            public string Category { get; set; } = string.Empty;
            public int Stock { get; set; }
            public bool IsActive { get; set; }
        }

        /// <summary>
        /// Modèle de réponse de mise à jour de produit.
        /// </summary>
        public class ProductUpdateResponse
        {
            public bool Success { get; set; }
            public string Message { get; set; } = string.Empty;
        }

        /// <summary>
        /// Modèle de réponse de suppression de produit.
        /// </summary>
        public class ProductDeleteResponse
        {
            public bool Success { get; set; }
            public string Message { get; set; } = string.Empty;
        }

        /// <summary>
        /// Modèle de catégorie.
        /// </summary>
        public class Category
        {
            public string Id { get; set; } = string.Empty;
            public string Name { get; set; } = string.Empty;
            public string Description { get; set; } = string.Empty;
            public int ProductCount { get; set; }
        }

        /// <summary>
        /// Modèle de statistiques de produits.
        /// </summary>
        public class ProductStatistics
        {
            public int TotalProducts { get; set; }
            public int ActiveProducts { get; set; }
            public int InactiveProducts { get; set; }
            public decimal AveragePrice { get; set; }
            public int TotalStock { get; set; }
            public int LowStockProducts { get; set; }
            public DateTime LastUpdated { get; set; }
        }

        #endregion
    }
}