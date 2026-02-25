"""Pytest configuration and fixtures for MDAN tests."""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import pytest

# Add project root to path for integrations module
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Add CLI directory to path
CLI_DIR = PROJECT_ROOT / "cli"
sys.path.insert(0, str(CLI_DIR))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def mock_subprocess():
    """Mock subprocess module."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = Mock(returncode=0)
        yield mock_run


@pytest.fixture
def mock_platform():
    """Mock sys.platform."""
    with patch("sys.platform", "darwin"):
        yield


@pytest.fixture
def sample_config():
    """Sample configuration for external services."""
    return {
        "ExternalServices": {
            "ServiceA": {
                "BaseUrl": "https://api.example.com/v1",
                "ApiKey": "test-key",
                "Timeout": 30,
                "RetryCount": 3,
                "RetryDelay": 1000,
                "EnableCircuitBreaker": True,
                "CircuitBreakerThreshold": 5,
                "EnableRateLimiting": True,
                "RateLimitPerMinute": 60,
                "EnableCaching": True,
                "CacheDurationMinutes": 5,
            }
        }
    }


@pytest.fixture
def templates_dir():
    """Get templates directory path."""
    return Path(__file__).parent.parent / "templates"


@pytest.fixture
def external_services_dir(templates_dir):
    """Get external services templates directory."""
    return templates_dir / "external-services"


@pytest.fixture
def dotnet_blazor_dir(templates_dir):
    """Get .NET Blazor templates directory."""
    return templates_dir / "dotnet-blazor"


@pytest.fixture
def sql_server_dir(templates_dir):
    """Get SQL Server templates directory."""
    return templates_dir / "sql-server"
