"""Tests for external services patterns and implementation."""

from pathlib import Path
import pytest


class TestExternalServicesPatterns:
    """Test external services advanced patterns."""

    def test_configuration_pattern_valid(self, external_services_dir):
        """Test that configuration pattern is valid."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "ExternalServices" in content
        assert "BaseUrl" in content
        assert "ApiKey" in content
        assert "Timeout" in content
        assert "RetryCount" in content
        assert "EnableCircuitBreaker" in content
        assert "EnableRateLimiting" in content
        assert "EnableCaching" in content

    def test_multiple_services_configuration(self, external_services_dir):
        """Test that multiple services configuration is documented."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "ServiceA" in content or "multiple" in content.lower()

    def test_retry_pattern_documented(self, external_services_dir):
        """Test that retry pattern is documented."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "Retry" in content or "retry" in content.lower()

    def test_circuit_breaker_pattern_documented(self, external_services_dir):
        """Test that circuit breaker pattern is documented."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "Circuit Breaker" in content or "circuit" in content.lower()

    def test_rate_limiting_pattern_documented(self, external_services_dir):
        """Test that rate limiting pattern is documented."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "Rate Limiting" in content or "rate" in content.lower()

    def test_caching_pattern_documented(self, external_services_dir):
        """Test that caching pattern is documented."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "Caching" in content or "cache" in content.lower()

    def test_service_response_model(self, external_services_dir):
        """Test that ServiceResponse model is documented."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "ServiceResponse" in content
        assert "Success" in content
        assert "Data" in content
        assert "ErrorCode" in content or "ErrorMessage" in content

    def test_error_handling_documented(self, external_services_dir):
        """Test that error handling is documented."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "Gestion des Erreurs" in content or "Error Handling" in content

    def test_security_documented(self, external_services_dir):
        """Test that security is documented."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "Sécurité" in content or "Security" in content
        assert "HTTPS" in content
        assert "API" in content

    def test_troubleshooting_documented(self, external_services_dir):
        """Test that troubleshooting is documented."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "Dépannage" in content or "Troubleshooting" in content

    def test_usage_examples(self, external_services_dir):
        """Test that usage examples are provided."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "```csharp" in content or "```json" in content

    def test_generic_service_implementation(self, external_services_dir):
        """Test that generic service implementation is shown."""
        example = external_services_dir / "ExampleService.cs"
        assert example.exists()
        content = example.read_text()
        assert "ServiceBase" in content
        assert "GetDataAsync" in content or "PostDataAsync" in content


class TestExternalServicesGeneric:
    """Test that external services are generic (not wallet-specific)."""

    def test_no_wallet_references_in_readme(self, external_services_dir):
        """Test that README has no wallet references."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "wallet" not in content.lower()
        assert "wafacash" not in content.lower()
        assert "mywafacash" not in content.lower()
        assert "fawri" not in content.lower()

    def test_no_wallet_references_in_iservice(self, external_services_dir):
        """Test that IService has no wallet references."""
        iservice = external_services_dir / "IService.cs"
        content = iservice.read_text()
        assert "wallet" not in content.lower()
        assert "wafacash" not in content.lower()
        assert "mywafacash" not in content.lower()
        assert "fawri" not in content.lower()

    def test_no_wallet_references_in_servicebase(self, external_services_dir):
        """Test that ServiceBase has no wallet references."""
        servicebase = external_services_dir / "ServiceBase.cs"
        content = servicebase.read_text()
        assert "wallet" not in content.lower()
        assert "wafacash" not in content.lower()
        assert "mywafacash" not in content.lower()
        assert "fawri" not in content.lower()

    def test_no_wallet_references_in_exampleservice(self, external_services_dir):
        """Test that ExampleService has no wallet references."""
        example = external_services_dir / "ExampleService.cs"
        content = example.read_text()
        assert "wallet" not in content.lower()
        assert "wafacash" not in content.lower()
        assert "mywafacash" not in content.lower()
        assert "fawri" not in content.lower()

    def test_generic_service_names(self, external_services_dir):
        """Test that service names are generic."""
        example = external_services_dir / "ExampleService.cs"
        content = example.read_text()
        assert "ExampleService" in content

    def test_generic_endpoint_names(self, external_services_dir):
        """Test that endpoint names are generic."""
        example = external_services_dir / "ExampleService.cs"
        content = example.read_text()
        assert "products" in content.lower() or "categories" in content.lower()

    def test_generic_configuration_names(self, external_services_dir):
        """Test that configuration names are generic."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "ServiceA" in content or "ServiceName" in content
        assert "api.example.com" in content


class TestExternalServicesIntegration:
    """Test external services integration patterns."""

    def test_http_client_usage(self, external_services_dir):
        """Test that HttpClient is used."""
        servicebase = external_services_dir / "ServiceBase.cs"
        content = servicebase.read_text()
        assert "HttpClient" in content or "IHttpClientFactory" in content

    def test_async_await_pattern(self, external_services_dir):
        """Test that async/await pattern is used."""
        iservice = external_services_dir / "IService.cs"
        content = iservice.read_text()
        assert "Task<" in content

    def test_dependency_injection_pattern(self, external_services_dir):
        """Test that dependency injection is used."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert (
            "AddScoped" in content
            or "AddTransient" in content
            or "AddSingleton" in content
        )

    def test_configuration_injection(self, external_services_dir):
        """Test that configuration is injected."""
        example = external_services_dir / "ExampleService.cs"
        content = example.read_text()
        assert "IConfiguration" in content

    def test_logger_injection(self, external_services_dir):
        """Test that logger is injected."""
        example = external_services_dir / "ExampleService.cs"
        content = example.read_text()
        assert "ILogger" in content
