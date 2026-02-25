"""Tests for MDAN templates."""

from pathlib import Path
import pytest


class TestExternalServicesTemplate:
    """Test external services template."""

    def test_external_services_template_exists(self, external_services_dir):
        """Test that external services template directory exists."""
        assert external_services_dir.exists()
        assert external_services_dir.is_dir()

    def test_external_services_files_complete(self, external_services_dir):
        """Test that all required files exist."""
        required_files = [
            "README.md",
            "IService.cs",
            "ServiceBase.cs",
            "ServiceProvider.cs",
            "ExampleService.cs",
        ]

        for file_name in required_files:
            file_path = external_services_dir / file_name
            assert file_path.exists(), f"Missing file: {file_name}"

    def test_iservice_interface_exists(self, external_services_dir):
        """Test that IService.cs interface exists."""
        iservice = external_services_dir / "IService.cs"
        assert iservice.exists()
        content = iservice.read_text()
        assert "interface IService" in content
        assert "Task<ServiceResponse<T>>" in content

    def test_servicebase_has_retry_logic(self, external_services_dir):
        """Test that ServiceBase.cs has retry logic."""
        servicebase = external_services_dir / "ServiceBase.cs"
        assert servicebase.exists()
        content = servicebase.read_text()
        assert "RetryCount" in content or "retry" in content.lower()

    def test_servicebase_has_circuit_breaker(self, external_services_dir):
        """Test that ServiceBase.cs has circuit breaker."""
        servicebase = external_services_dir / "ServiceBase.cs"
        assert servicebase.exists()
        content = servicebase.read_text()
        assert "CircuitBreaker" in content or "circuit" in content.lower()

    def test_servicebase_has_rate_limiting(self, external_services_dir):
        """Test that ServiceBase.cs has rate limiting."""
        servicebase = external_services_dir / "ServiceBase.cs"
        assert servicebase.exists()
        content = servicebase.read_text()
        assert "RateLimit" in content or "rate" in content.lower()

    def test_servicebase_has_caching(self, external_services_dir):
        """Test that ServiceBase.cs has caching."""
        servicebase = external_services_dir / "ServiceBase.cs"
        assert servicebase.exists()
        content = servicebase.read_text()
        assert "Cache" in content or "cache" in content.lower()

    def test_exampleservice_complete(self, external_services_dir):
        """Test that ExampleService.cs is complete."""
        example = external_services_dir / "ExampleService.cs"
        assert example.exists()
        content = example.read_text()
        assert "class ExampleService" in content
        assert "ServiceBase" in content

    def test_external_services_documentation_french(self, external_services_dir):
        """Test that external services documentation is in French."""
        readme = external_services_dir / "README.md"
        assert readme.exists()
        content = readme.read_text()
        assert "Templates d'Intégration" in content or "Intégration" in content


class TestDotNetBlazorTemplate:
    """Test .NET Blazor template."""

    def test_dotnet_blazor_template_exists(self, dotnet_blazor_dir):
        """Test that .NET Blazor template directory exists."""
        assert dotnet_blazor_dir.exists()
        assert dotnet_blazor_dir.is_dir()

    def test_dotnet_blazor_readme_exists(self, dotnet_blazor_dir):
        """Test that Blazor README exists."""
        readme = dotnet_blazor_dir / "README.md"
        assert readme.exists()

    def test_dotnet_blazor_has_program_cs(self, dotnet_blazor_dir):
        """Test that Blazor template has Program.cs example."""
        readme = dotnet_blazor_dir / "README.md"
        content = readme.read_text()
        assert "Program.cs" in content
        assert "WebApplication.CreateBuilder" in content

    def test_dotnet_blazor_has_azure_ad(self, dotnet_blazor_dir):
        """Test that Blazor template has Azure AD integration."""
        readme = dotnet_blazor_dir / "README.md"
        content = readme.read_text()
        assert "AzureAd" in content or "Azure AD" in content

    def test_dotnet_blazor_has_external_services(self, dotnet_blazor_dir):
        """Test that Blazor template has external services configuration."""
        readme = dotnet_blazor_dir / "README.md"
        content = readme.read_text()
        assert "ExternalServices" in content

    def test_dotnet_blazor_has_entity_framework(self, dotnet_blazor_dir):
        """Test that Blazor template has Entity Framework."""
        readme = dotnet_blazor_dir / "README.md"
        content = readme.read_text()
        assert "EntityFrameworkCore" in content or "DbContext" in content


class TestSQLServerTemplate:
    """Test SQL Server template."""

    def test_sql_server_template_exists(self, sql_server_dir):
        """Test that SQL Server template directory exists."""
        assert sql_server_dir.exists()
        assert sql_server_dir.is_dir()

    def test_sql_server_files_complete(self, sql_server_dir):
        """Test that all SQL Server files exist."""
        required_files = [
            "README.md",
            "schema.sql",
            "stored-procedures.sql",
            "functions.sql",
        ]

        for file_name in required_files:
            file_path = sql_server_dir / file_name
            assert file_path.exists(), f"Missing file: {file_name}"

    def test_sql_server_schema_exists(self, sql_server_dir):
        """Test that schema.sql exists."""
        schema = sql_server_dir / "schema.sql"
        assert schema.exists()
        content = schema.read_text()
        assert "CREATE TABLE" in content.upper()

    def test_sql_server_stored_procedures_exist(self, sql_server_dir):
        """Test that stored-procedures.sql exists."""
        procedures = sql_server_dir / "stored-procedures.sql"
        assert procedures.exists()
        content = procedures.read_text()
        assert "CREATE PROCEDURE" in content.upper()

    def test_sql_server_functions_exist(self, sql_server_dir):
        """Test that functions.sql exists."""
        functions = sql_server_dir / "functions.sql"
        assert functions.exists()
        content = functions.read_text()
        assert "CREATE FUNCTION" in content.upper()


class TestTemplatesDocumentation:
    """Test templates documentation."""

    def test_external_services_readme_complete(self, external_services_dir):
        """Test that external services README is complete."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "Installation" in content
        assert "Configuration" in content
        assert "Utilisation" in content
        assert "Patterns" in content or "Patterns Implémentés" in content

    def test_dotnet_blazor_readme_complete(self, dotnet_blazor_dir):
        """Test that Blazor README is complete."""
        readme = dotnet_blazor_dir / "README.md"
        content = readme.read_text()
        assert "Program.cs" in content
        assert "appsettings.json" in content
        assert "ApplicationDbContext" in content

    def test_sql_server_readme_complete(self, sql_server_dir):
        """Test that SQL Server README is complete."""
        readme = sql_server_dir / "README.md"
        content = readme.read_text()
        assert "Usage" in content
        assert "Best Practices" in content
