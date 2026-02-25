"""Regression tests to ensure no wallet references remain."""

import subprocess
from pathlib import Path
import pytest


class TestNoWalletReferences:
    """Test that no wallet references exist in the codebase."""

    def test_no_wafacash_references(self):
        """Test that no 'wafacash' references exist."""
        result = subprocess.run(
            [
                "grep",
                "-r",
                "wafacash",
                "--exclude-dir=node_modules",
                "--exclude-dir=.git",
                "--exclude-dir=docs-site",
                "--exclude-dir=tests",
                "--exclude-dir=__pycache__",
                "--exclude-dir=.pytest_cache",
                "--exclude-dir=venv",
                "--exclude-dir=.github",
                ".",
            ],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, f"Found 'wafacash' references:\n{result.stdout}"

    def test_no_mywafacash_references(self):
        """Test that no 'mywafacash' references exist."""
        result = subprocess.run(
            [
                "grep",
                "-r",
                "mywafacash",
                "--exclude-dir=node_modules",
                "--exclude-dir=.git",
                "--exclude-dir=docs-site",
                "--exclude-dir=tests",
                "--exclude-dir=__pycache__",
                "--exclude-dir=.pytest_cache",
                "--exclude-dir=venv",
                "--exclude-dir=.github",
                ".",
            ],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, (
            f"Found 'mywafacash' references:\n{result.stdout}"
        )

    def test_no_fawri_references(self):
        """Test that no 'Fawri' references exist."""
        result = subprocess.run(
            [
                "grep",
                "-r",
                "Fawri",
                "--exclude-dir=node_modules",
                "--exclude-dir=.git",
                "--exclude-dir=docs-site",
                "--exclude-dir=tests",
                "--exclude-dir=__pycache__",
                "--exclude-dir=.pytest_cache",
                "--exclude-dir=venv",
                "--exclude-dir=.github",
                ".",
            ],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, f"Found 'Fawri' references:\n{result.stdout}"

    def test_no_wallet_references_in_templates(self, templates_dir):
        """Test that no wallet references exist in templates."""
        result = subprocess.run(
            ["grep", "-r", "-i", "wallet", str(templates_dir)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, (
            f"Found wallet references in templates:\n{result.stdout}"
        )

    def test_no_wallet_references_in_agents(self):
        """Test that no wallet references exist in agents."""
        agents_dir = Path(__file__).parent.parent / "agents"
        result = subprocess.run(
            ["grep", "-r", "-i", "wallet", str(agents_dir)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, (
            f"Found wallet references in agents:\n{result.stdout}"
        )

    def test_no_wallet_references_in_phases(self):
        """Test that no wallet references exist in phases."""
        phases_dir = Path(__file__).parent.parent / "phases"
        result = subprocess.run(
            ["grep", "-r", "-i", "wallet", str(phases_dir)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, (
            f"Found wallet references in phases:\n{result.stdout}"
        )

    def test_no_wallet_references_in_workflows(self):
        """Test that no wallet references exist in workflows."""
        workflows_dir = Path(__file__).parent.parent / "workflows"
        result = subprocess.run(
            ["grep", "-r", "-i", "wallet", str(workflows_dir)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, (
            f"Found wallet references in workflows:\n{result.stdout}"
        )

    def test_no_wallet_references_in_core(self):
        """Test that no wallet references exist in core."""
        core_dir = Path(__file__).parent.parent / "core"
        result = subprocess.run(
            ["grep", "-r", "-i", "wallet", str(core_dir)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, (
            f"Found wallet references in core:\n{result.stdout}"
        )

    def test_no_wallet_references_in_cli(self):
        """Test that no wallet references exist in CLI."""
        cli_dir = Path(__file__).parent.parent / "cli"
        result = subprocess.run(
            ["grep", "-r", "-i", "wallet", str(cli_dir)], capture_output=True, text=True
        )
        assert result.returncode != 0, (
            f"Found wallet references in CLI:\n{result.stdout}"
        )


class TestExternalServicesGeneric:
    """Test that external services are generic."""

    def test_external_services_directory_exists(self, templates_dir):
        """Test that external-services directory exists."""
        external_services = templates_dir / "external-services"
        assert external_services.exists()

    def test_wallets_directory_does_not_exist(self, templates_dir):
        """Test that wallets directory does not exist."""
        wallets = templates_dir / "wallets"
        assert not wallets.exists()

    def test_external_services_has_generic_names(self, external_services_dir):
        """Test that external services use generic names."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "ServiceA" in content or "ServiceName" in content
        assert "api.example.com" in content

    def test_external_services_no_specific_providers(self, external_services_dir):
        """Test that no specific payment providers are mentioned."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "payment" not in content.lower()
        assert "bank" not in content.lower()
        assert "transfer" not in content.lower()


class TestGenericConfiguration:
    """Test that configuration is generic."""

    def test_generic_service_configuration(self, external_services_dir):
        """Test that service configuration is generic."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "BaseUrl" in content
        assert "ApiKey" in content
        assert "Timeout" in content

    def test_multiple_services_supported(self, external_services_dir):
        """Test that multiple services are supported."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "ServiceA" in content or "multiple" in content.lower()

    def test_no_payment_specific_fields(self, external_services_dir):
        """Test that no payment-specific fields exist."""
        readme = external_services_dir / "README.md"
        content = readme.read_text()
        assert "amount" not in content.lower()
        assert "currency" not in content.lower()
        assert "transaction" not in content.lower()


class TestBlazorTemplateGeneric:
    """Test that Blazor template is generic."""

    def test_blazor_no_wallet_models(self, dotnet_blazor_dir):
        """Test that Blazor template has no wallet models."""
        readme = dotnet_blazor_dir / "README.md"
        content = readme.read_text()
        assert "Wallet" not in content
        assert "Transaction" not in content

    def test_blazor_has_external_services(self, dotnet_blazor_dir):
        """Test that Blazor template has external services."""
        readme = dotnet_blazor_dir / "README.md"
        content = readme.read_text()
        assert "ExternalServices" in content

    def test_blazor_generic_models(self, dotnet_blazor_dir):
        """Test that Blazor template has generic models."""
        readme = dotnet_blazor_dir / "README.md"
        content = readme.read_text()
        assert "User" in content
        assert "Notification" in content


class TestSQLServerTemplateGeneric:
    """Test that SQL Server template is generic."""

    def test_sql_no_wallet_tables(self, sql_server_dir):
        """Test that SQL template has no wallet tables."""
        schema = sql_server_dir / "schema.sql"
        if schema.exists():
            content = schema.read_text()
            assert "Wallet" not in content

    def test_sql_generic_tables(self, sql_server_dir):
        """Test that SQL template has generic tables."""
        schema = sql_server_dir / "schema.sql"
        if schema.exists():
            content = schema.read_text()
            assert "Users" in content or "User" in content


class TestDocumentationGeneric:
    """Test that documentation is generic."""

    def test_readme_no_wallet_references(self):
        """Test that README has no wallet references."""
        readme = Path(__file__).parent.parent / "README.md"
        content = readme.read_text()
        # Allow "wallet" in test documentation context, but not as features
        assert "wafacash" not in content.lower()
        assert "mywafacash" not in content.lower()
        assert "fawri" not in content.lower()
        assert "wafacash" not in content.lower()
        assert "mywafacash" not in content.lower()
        assert "fawri" not in content.lower()

    def test_agents_md_no_wallet_references(self):
        """Test that AGENTS.md has no wallet references."""
        agents_md = Path(__file__).parent.parent / "AGENTS.md"
        if agents_md.exists():
            content = agents_md.read_text()
            assert "wallet" not in content.lower()
            assert "wafacash" not in content.lower()
            assert "mywafacash" not in content.lower()
            assert "fawri" not in content.lower()

    def test_auto_orchestrator_no_wallet_references(self):
        """Test that auto-orchestrator has no wallet references."""
        auto_orch = Path(__file__).parent.parent / "agents" / "auto-orchestrator.md"
        if auto_orch.exists():
            content = auto_orch.read_text()
            assert "wallet" not in content.lower()
            assert "wafacash" not in content.lower()
            assert "mywafacash" not in content.lower()
            assert "fawri" not in content.lower()

    def test_debate_protocol_no_wallet_references(self):
        """Test that debate protocol has no wallet references."""
        debate = Path(__file__).parent.parent / "core" / "debate-protocol.md"
        if debate.exists():
            content = debate.read_text()
            assert "wallet" not in content.lower()
            assert "wafacash" not in content.lower()
            assert "mywafacash" not in content.lower()
            assert "fawri" not in content.lower()


class TestAutoPhasesGeneric:
    """Test that auto phases are generic."""

    def test_auto_load_no_wallet_references(self):
        """Test that auto-01-load has no wallet references."""
        phase = Path(__file__).parent.parent / "phases" / "auto-01-load.md"
        if phase.exists():
            content = phase.read_text()
            assert "wallet" not in content.lower()
            assert "wafacash" not in content.lower()
            assert "mywafacash" not in content.lower()
            assert "fawri" not in content.lower()

    def test_auto_discover_no_wallet_references(self):
        """Test that auto-02-discover has no wallet references."""
        phase = Path(__file__).parent.parent / "phases" / "auto-02-discover.md"
        if phase.exists():
            content = phase.read_text()
            assert "wallet" not in content.lower()
            assert "wafacash" not in content.lower()
            assert "mywafacash" not in content.lower()
            assert "fawri" not in content.lower()

    def test_auto_plan_no_wallet_references(self):
        """Test that auto-03-plan has no wallet references."""
        phase = Path(__file__).parent.parent / "phases" / "auto-03-plan.md"
        if phase.exists():
            content = phase.read_text()
            assert "wallet" not in content.lower()
            assert "wafacash" not in content.lower()
            assert "mywafacash" not in content.lower()
            assert "fawri" not in content.lower()

    def test_auto_architect_no_wallet_references(self):
        """Test that auto-04-architect has no wallet references."""
        phase = Path(__file__).parent.parent / "phases" / "auto-04-architect.md"
        if phase.exists():
            content = phase.read_text()
            assert "wallet" not in content.lower()
            assert "wafacash" not in content.lower()
            assert "mywafacash" not in content.lower()
            assert "fawri" not in content.lower()

    def test_auto_implement_no_wallet_references(self):
        """Test that auto-05-implement has no wallet references."""
        phase = Path(__file__).parent.parent / "phases" / "auto-05-implement.md"
        if phase.exists():
            content = phase.read_text()
            assert "wallet" not in content.lower()
            assert "wafacash" not in content.lower()
            assert "mywafacash" not in content.lower()
            assert "fawri" not in content.lower()

    def test_auto_test_no_wallet_references(self):
        """Test that auto-06-test has no wallet references."""
        phase = Path(__file__).parent.parent / "phases" / "auto-06-test.md"
        if phase.exists():
            content = phase.read_text()
            assert "wallet" not in content.lower()
            assert "wafacash" not in content.lower()
            assert "mywafacash" not in content.lower()
            assert "fawri" not in content.lower()

    def test_auto_deploy_no_wallet_references(self):
        """Test that auto-07-deploy has no wallet references."""
        phase = Path(__file__).parent.parent / "phases" / "auto-07-deploy.md"
        if phase.exists():
            content = phase.read_text()
            assert "wallet" not in content.lower()
            assert "wafacash" not in content.lower()
            assert "mywafacash" not in content.lower()
            assert "fawri" not in content.lower()

    def test_auto_doc_no_wallet_references(self):
        """Test that auto-08-doc has no wallet references."""
        phase = Path(__file__).parent.parent / "phases" / "auto-08-doc.md"
        if phase.exists():
            content = phase.read_text()
            assert "wallet" not in content.lower()
            assert "wafacash" not in content.lower()
            assert "mywafacash" not in content.lower()
            assert "fawri" not in content.lower()
