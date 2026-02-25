using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Polly;
using Polly.CircuitBreaker;
using Polly.RateLimit;

namespace ExternalServices.Services
{
    /// <summary>
    /// Implémentation de base pour les services externes avec patterns avancés.
    /// </summary>
    public abstract class ServiceBase : IService
    {
        protected readonly HttpClient _httpClient;
        protected readonly IConfiguration _configuration;
        protected readonly ILogger _logger;
        protected readonly IMemoryCache _cache;
        protected readonly string _serviceName;
        protected readonly string _baseUrl;
        protected readonly string _apiKey;
        protected readonly int _timeout;
        protected readonly int _retryCount;
        protected readonly int _retryDelay;
        protected readonly bool _enableCircuitBreaker;
        protected readonly int _circuitBreakerThreshold;
        protected readonly bool _enableRateLimiting;
        protected readonly int _rateLimitPerMinute;
        protected readonly bool _enableCaching;
        protected readonly int _cacheDurationMinutes;

        protected string? _accessToken;
        protected DateTime _tokenExpiry;
        protected readonly SemaphoreSlim _rateLimitSemaphore;
        protected readonly Queue<DateTime> _requestTimestamps;
        protected AsyncCircuitBreakerPolicy? _circuitBreakerPolicy;
        protected AsyncRetryPolicy? _retryPolicy;

        protected ServiceStatus _status;

        public string ServiceName => _serviceName;
        public string BaseUrl => _baseUrl;

        protected ServiceBase(
            IConfiguration configuration,
            string serviceName,
            ILogger logger,
            IMemoryCache? cache = null)
        {
            _configuration = configuration;
            _serviceName = serviceName;
            _logger = logger;
            _cache = cache ?? new MemoryCache(new MemoryCacheOptions());
            _rateLimitSemaphore = new SemaphoreSlim(1, 1);
            _requestTimestamps = new Queue<DateTime>();
            _status = new ServiceStatus();

            var configSection = configuration.GetSection($"ExternalServices:{serviceName}");
            
            _baseUrl = configSection["BaseUrl"] ?? throw new ArgumentException($"BaseUrl not configured for service {serviceName}");
            _apiKey = configSection["ApiKey"] ?? string.Empty;
            _timeout = configSection.GetValue<int>("Timeout", 30);
            _retryCount = configSection.GetValue<int>("RetryCount", 3);
            _retryDelay = configSection.GetValue<int>("RetryDelay", 1000);
            _enableCircuitBreaker = configSection.GetValue<bool>("EnableCircuitBreaker", true);
            _circuitBreakerThreshold = configSection.GetValue<int>("CircuitBreakerThreshold", 5);
            _enableRateLimiting = configSection.GetValue<bool>("EnableRateLimiting", true);
            _rateLimitPerMinute = configSection.GetValue<int>("RateLimitPerMinute", 60);
            _enableCaching = configSection.GetValue<bool>("EnableCaching", true);
            _cacheDurationMinutes = configSection.GetValue<int>("CacheDurationMinutes", 5);

            _httpClient = new HttpClient
            {
                BaseAddress = new Uri(_baseUrl),
                Timeout = TimeSpan.FromSeconds(_timeout)
            };

            _httpClient.DefaultRequestHeaders.Accept.Add(
                new MediaTypeWithQualityHeaderValue("application/json"));

            InitializePolicies();
        }

        private void InitializePolicies()
        {
            // Retry Policy
            _retryPolicy = Policy
                .Handle<HttpRequestException>()
                .OrResult<HttpResponseMessage>(r => 
                    r.StatusCode == HttpStatusCode.ServiceUnavailable ||
                    r.StatusCode == HttpStatusCode.GatewayTimeout ||
                    r.StatusCode == HttpStatusCode.RequestTimeout)
                .WaitAndRetryAsync(
                    _retryCount,
                    retryAttempt => TimeSpan.FromMilliseconds(_retryDelay * retryAttempt),
                    onRetry: (outcome, timespan, retryCount, context) =>
                    {
                        _logger.LogWarning(
                            "Retry {RetryCount} after {Delay}ms for {ServiceName}",
                            retryCount, timespan.TotalMilliseconds, _serviceName);
                    });

            // Circuit Breaker Policy
            if (_enableCircuitBreaker)
            {
                _circuitBreakerPolicy = Policy
                    .Handle<HttpRequestException>()
                    .OrResult<HttpResponseMessage>(r => 
                        r.StatusCode == HttpStatusCode.ServiceUnavailable ||
                        r.StatusCode == HttpStatusCode.GatewayTimeout)
                    .CircuitBreakerAsync(
                        exceptionsAllowedBeforeBreaking: _circuitBreakerThreshold,
                        durationOfBreak: TimeSpan.FromMinutes(1),
                        onBreak: (exception, breakDelay) =>
                        {
                            _status.IsCircuitOpen = true;
                            _logger.LogError(
                                "Circuit broken for {ServiceName} for {BreakDelay}ms",
                                _serviceName, breakDelay.TotalMilliseconds);
                        },
                        onReset: () =>
                        {
                            _status.IsCircuitOpen = false;
                            _status.ConsecutiveFailures = 0;
                            _logger.LogInformation("Circuit reset for {ServiceName}", _serviceName);
                        });
            }
        }

        public virtual async Task AuthenticateAsync()
        {
            if (_accessToken != null && DateTime.UtcNow < _tokenExpiry)
            {
                return;
            }

            try
            {
                var authRequest = new
                {
                    ApiKey = _apiKey
                };

                var response = await ExecuteWithRetryAsync(async () =>
                {
                    var json = JsonSerializer.Serialize(authRequest);
                    var content = new StringContent(json, Encoding.UTF8, "application/json");
                    return await _httpClient.PostAsync("auth/token", content);
                });

                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    var authResponse = JsonSerializer.Deserialize<AuthResponse>(responseContent);
                    
                    if (authResponse != null)
                    {
                        _accessToken = authResponse.AccessToken;
                        _tokenExpiry = DateTime.UtcNow.AddSeconds(authResponse.ExpiresIn);
                        _status.IsAuthenticated = true;
                        _logger.LogInformation("Authenticated successfully for {ServiceName}", _serviceName);
                    }
                }
                else
                {
                    _logger.LogError("Authentication failed for {ServiceName}: {StatusCode}", 
                        _serviceName, response.StatusCode);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Authentication error for {ServiceName}", _serviceName);
                throw;
            }
        }

        public async Task<bool> IsAuthenticatedAsync()
        {
            return _accessToken != null && DateTime.UtcNow < _tokenExpiry;
        }

        public async Task<ServiceResponse<T>> GetDataAsync<T>(string endpoint, Dictionary<string, string>? parameters = null)
        {
            return await ExecuteWithCircuitBreakerAsync(async () =>
            {
                await EnsureAuthenticatedAsync();
                await ApplyRateLimitAsync();

                var cacheKey = $"GET:{endpoint}:{GetCacheKey(parameters)}";
                
                if (_enableCaching)
                {
                    var cached = await GetFromCacheAsync<T>(cacheKey);
                    if (cached != null)
                    {
                        return cached;
                    }
                }

                var url = BuildUrl(endpoint, parameters);
                var response = await ExecuteWithRetryAsync(async () =>
                {
                    _httpClient.DefaultRequestHeaders.Authorization = 
                        new AuthenticationHeaderValue("Bearer", _accessToken);
                    return await _httpClient.GetAsync(url);
                });

                var result = await ProcessResponseAsync<T>(response);
                
                if (_enableCaching && result.Success)
                {
                    await SetCacheAsync(cacheKey, result);
                }

                return result;
            });
        }

        public async Task<ServiceResponse<T>> PostDataAsync<T>(string endpoint, object data)
        {
            return await ExecuteWithCircuitBreakerAsync(async () =>
            {
                await EnsureAuthenticatedAsync();
                await ApplyRateLimitAsync();

                var json = JsonSerializer.Serialize(data);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await ExecuteWithRetryAsync(async () =>
                {
                    _httpClient.DefaultRequestHeaders.Authorization = 
                        new AuthenticationHeaderValue("Bearer", _accessToken);
                    return await _httpClient.PostAsync(endpoint, content);
                });

                return await ProcessResponseAsync<T>(response);
            });
        }

        public async Task<ServiceResponse<T>> PutDataAsync<T>(string endpoint, object data)
        {
            return await ExecuteWithCircuitBreakerAsync(async () =>
            {
                await EnsureAuthenticatedAsync();
                await ApplyRateLimitAsync();

                var json = JsonSerializer.Serialize(data);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await ExecuteWithRetryAsync(async () =>
                {
                    _httpClient.DefaultRequestHeaders.Authorization = 
                        new AuthenticationHeaderValue("Bearer", _accessToken);
                    return await _httpClient.PutAsync(endpoint, content);
                });

                return await ProcessResponseAsync<T>(response);
            });
        }

        public async Task<ServiceResponse<T>> DeleteDataAsync<T>(string endpoint)
        {
            return await ExecuteWithCircuitBreakerAsync(async () =>
            {
                await EnsureAuthenticatedAsync();
                await ApplyRateLimitAsync();

                var response = await ExecuteWithRetryAsync(async () =>
                {
                    _httpClient.DefaultRequestHeaders.Authorization = 
                        new AuthenticationHeaderValue("Bearer", _accessToken);
                    return await _httpClient.DeleteAsync(endpoint);
                });

                return await ProcessResponseAsync<T>(response);
            });
        }

        public async Task<bool> HealthCheckAsync()
        {
            try
            {
                var response = await _httpClient.GetAsync("health");
                var isHealthy = response.IsSuccessStatusCode;
                
                _status.IsHealthy = isHealthy;
                
                if (isHealthy)
                {
                    _status.LastSuccessfulCall = DateTime.UtcNow;
                    _status.ConsecutiveFailures = 0;
                }
                else
                {
                    _status.LastFailedCall = DateTime.UtcNow;
                    _status.ConsecutiveFailures++;
                }

                return isHealthy;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Health check failed for {ServiceName}", _serviceName);
                _status.IsHealthy = false;
                _status.LastFailedCall = DateTime.UtcNow;
                _status.ConsecutiveFailures++;
                return false;
            }
        }

        public async Task<ServiceStatus> GetStatusAsync()
        {
            await HealthCheckAsync();
            return _status;
        }

        protected async Task EnsureAuthenticatedAsync()
        {
            if (!await IsAuthenticatedAsync())
            {
                await AuthenticateAsync();
            }
        }

        protected async Task ApplyRateLimitAsync()
        {
            if (!_enableRateLimiting)
            {
                return;
            }

            await _rateLimitSemaphore.WaitAsync();
            try
            {
                var now = DateTime.UtcNow;
                
                // Remove timestamps older than 1 minute
                while (_requestTimestamps.Count > 0 && 
                       (now - _requestTimestamps.Peek()).TotalMinutes > 1)
                {
                    _requestTimestamps.Dequeue();
                }

                // Check if rate limit exceeded
                if (_requestTimestamps.Count >= _rateLimitPerMinute)
                {
                    var oldestRequest = _requestTimestamps.Peek();
                    var waitTime = TimeSpan.FromMinutes(1) - (now - oldestRequest);
                    
                    if (waitTime.TotalMilliseconds > 0)
                    {
                        _logger.LogWarning(
                            "Rate limit reached for {ServiceName}, waiting {WaitTime}ms",
                            _serviceName, waitTime.TotalMilliseconds);
                        await Task.Delay(waitTime);
                    }
                }

                _requestTimestamps.Enqueue(now);
            }
            finally
            {
                _rateLimitSemaphore.Release();
            }
        }

        protected async Task<T> ExecuteWithRetryAsync<T>(Func<Task<T>> action)
        {
            if (_retryPolicy != null)
            {
                return await _retryPolicy.ExecuteAsync(action);
            }
            return await action();
        }

        protected async Task<T> ExecuteWithCircuitBreakerAsync<T>(Func<Task<T>> action)
        {
            if (_circuitBreakerPolicy != null)
            {
                return await _circuitBreakerPolicy.ExecuteAsync(action);
            }
            return await action();
        }

        protected async Task<ServiceResponse<T>> ProcessResponseAsync<T>(HttpResponseMessage response)
        {
            _status.TotalCalls++;

            var result = new ServiceResponse<T>
            {
                Timestamp = DateTime.UtcNow,
                StatusCode = (int)response.StatusCode
            };

            try
            {
                var responseContent = await response.Content.ReadAsStringAsync();

                if (response.IsSuccessStatusCode)
                {
                    result.Data = JsonSerializer.Deserialize<T>(responseContent);
                    result.Success = true;
                    _status.SuccessfulCalls++;
                    _status.LastSuccessfulCall = DateTime.UtcNow;
                    _status.ConsecutiveFailures = 0;
                }
                else
                {
                    result.Success = false;
                    result.ErrorMessage = responseContent;
                    result.ErrorCode = ((int)response.StatusCode).ToString();
                    _status.FailedCalls++;
                    _status.LastFailedCall = DateTime.UtcNow;
                    _status.ConsecutiveFailures++;

                    _logger.LogWarning(
                        "Request failed for {ServiceName}: {StatusCode} - {ErrorMessage}",
                        _serviceName, response.StatusCode, responseContent);
                }
            }
            catch (Exception ex)
            {
                result.Success = false;
                result.ErrorMessage = ex.Message;
                _status.FailedCalls++;
                _status.LastFailedCall = DateTime.UtcNow;
                _status.ConsecutiveFailures++;

                _logger.LogError(ex, "Error processing response for {ServiceName}", _serviceName);
            }

            return result;
        }

        protected string BuildUrl(string endpoint, Dictionary<string, string>? parameters)
        {
            if (parameters == null || parameters.Count == 0)
            {
                return endpoint;
            }

            var queryString = string.Join("&", parameters.Select(kvp => 
                $"{WebUtility.UrlEncode(kvp.Key)}={WebUtility.UrlEncode(kvp.Value)}"));
            return $"{endpoint}?{queryString}";
        }

        protected string GetCacheKey(Dictionary<string, string>? parameters)
        {
            if (parameters == null || parameters.Count == 0)
            {
                return "default";
            }

            return string.Join("|", parameters.OrderBy(kvp => kvp.Key)
                .Select(kvp => $"{kvp.Key}={kvp.Value}"));
        }

        protected async Task<ServiceResponse<T>?> GetFromCacheAsync<T>(string cacheKey)
        {
            if (_cache.TryGetValue(cacheKey, out ServiceResponse<T>? cached))
            {
                _logger.LogDebug("Cache hit for {CacheKey}", cacheKey);
                return cached;
            }
            return null;
        }

        protected async Task SetCacheAsync<T>(string cacheKey, ServiceResponse<T> value)
        {
            var expiry = TimeSpan.FromMinutes(_cacheDurationMinutes);
            _cache.Set(cacheKey, value, expiry);
            _logger.LogDebug("Cached response for {CacheKey} for {Expiry} minutes", 
                cacheKey, _cacheDurationMinutes);
        }

        protected class AuthResponse
        {
            public string AccessToken { get; set; } = string.Empty;
            public int ExpiresIn { get; set; }
        }
    }
}