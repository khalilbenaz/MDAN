"""Tests for MDAN installation."""

import json
import subprocess
from pathlib import Path
import pytest


class TestInstallationFiles:
    """Test installation files exist."""

    def test_postinstall_script_exists(self):
        """Test that postinstall script exists."""
        postinstall = Path(__file__).parent.parent / "cli" / "postinstall.js"
        assert postinstall.exists()

    def test_install_script_exists(self):
        """Test that install.sh script exists."""
        install = Path(__file__).parent.parent / "install.sh"
        assert install.exists()

    def test_package_json_exists(self):
        """Test that package.json exists."""
        package_json = Path(__file__).parent.parent / "package.json"
        assert package_json.exists()

    def test_cli_executable_exists(self):
        """Test that CLI executable exists."""
        cli_js = Path(__file__).parent.parent / "cli" / "mdan.js"
        cli_py = Path(__file__).parent.parent / "cli" / "mdan.py"
        assert cli_js.exists() or cli_py.exists()


class TestPackageJson:
    """Test package.json configuration."""

    def test_package_json_valid(self):
        """Test that package.json is valid JSON."""
        package_json = Path(__file__).parent.parent / "package.json"
        content = package_json.read_text()
        data = json.loads(content)
        assert data is not None

    def test_package_json_has_name(self):
        """Test that package.json has name."""
        package_json = Path(__file__).parent.parent / "package.json"
        content = package_json.read_text()
        data = json.loads(content)
        assert "name" in data
        assert data["name"] == "mdan-cli"

    def test_package_json_has_version(self):
        """Test that package.json has version."""
        package_json = Path(__file__).parent.parent / "package.json"
        content = package_json.read_text()
        data = json.loads(content)
        assert "version" in data
        assert data["version"] == "2.6.0"

    def test_package_json_has_bin(self):
        """Test that package.json has bin configuration."""
        package_json = Path(__file__).parent.parent / "package.json"
        content = package_json.read_text()
        data = json.loads(content)
        assert "bin" in data
        assert "mdan" in data["bin"]

    def test_package_json_has_postinstall_script(self):
        """Test that package.json has postinstall script."""
        package_json = Path(__file__).parent.parent / "package.json"
        content = package_json.read_text()
        data = json.loads(content)
        assert "scripts" in data
        assert "postinstall" in data["scripts"]

    def test_package_json_has_files(self):
        """Test that package.json has files configuration."""
        package_json = Path(__file__).parent.parent / "package.json"
        content = package_json.read_text()
        data = json.loads(content)
        assert "files" in data
        assert "cli/" in data["files"]
        assert "core/" in data["files"]
        assert "agents/" in data["files"]
        assert "templates/" in data["files"]

    def test_package_json_includes_auto_files(self):
        """Test that package.json includes MDAN-AUTO files."""
        package_json = Path(__file__).parent.parent / "package.json"
        content = package_json.read_text()
        data = json.loads(content)
        assert "files" in data
        assert "phases/" in data["files"]
        assert "memory/" in data["files"]


class TestCLIExecutable:
    """Test CLI executable."""

    def test_cli_python_executable_exists(self):
        """Test that Python CLI exists."""
        cli_py = Path(__file__).parent.parent / "cli" / "mdan.py"
        assert cli_py.exists()

    def test_cli_python_has_version(self):
        """Test that Python CLI has version constant."""
        cli_py = Path(__file__).parent.parent / "cli" / "mdan.py"
        content = cli_py.read_text()
        assert 'VERSION = "2.5.1"' in content

    def test_cli_python_has_main_function(self):
        """Test that Python CLI has main function."""
        cli_py = Path(__file__).parent.parent / "cli" / "mdan.py"
        content = cli_py.read_text()
        assert "def main():" in content

    def test_cli_python_has_auto_command(self):
        """Test that Python CLI has auto command."""
        cli_py = Path(__file__).parent.parent / "cli" / "mdan.py"
        content = cli_py.read_text()
        assert "cmd_auto" in content

    def test_cli_python_has_resume_command(self):
        """Test that Python CLI has resume command."""
        cli_py = Path(__file__).parent.parent / "cli" / "mdan.py"
        content = cli_py.read_text()
        assert "cmd_resume" in content


class TestCoreFiles:
    """Test core files exist."""

    def test_orchestrator_exists(self):
        """Test that orchestrator.md exists."""
        orchestrator = Path(__file__).parent.parent / "core" / "orchestrator.md"
        assert orchestrator.exists()

    def test_universal_envelope_exists(self):
        """Test that universal-envelope.md exists."""
        envelope = Path(__file__).parent.parent / "core" / "universal-envelope.md"
        assert envelope.exists()

    def test_debate_protocol_exists(self):
        """Test that debate-protocol.md exists."""
        debate = Path(__file__).parent.parent / "core" / "debate-protocol.md"
        assert debate.exists()


class TestAgentFiles:
    """Test agent files exist."""

    def test_auto_orchestrator_exists(self):
        """Test that auto-orchestrator.md exists."""
        auto_orch = Path(__file__).parent.parent / "agents" / "auto-orchestrator.md"
        assert auto_orch.exists()

    def test_core_agents_exist(self):
        """Test that core agents exist."""
        agents_dir = Path(__file__).parent.parent / "agents"
        required_agents = [
            "product.md",
            "architect.md",
            "ux.md",
            "dev.md",
            "test.md",
            "security.md",
            "devops.md",
            "doc.md",
        ]
        for agent in required_agents:
            assert (agents_dir / agent).exists(), f"Missing agent: {agent}"


class TestPhaseFiles:
    """Test phase files exist."""

    def test_auto_phases_exist(self):
        """Test that auto phases exist."""
        phases_dir = Path(__file__).parent.parent / "phases"
        required_phases = [
            "auto-01-load.md",
            "auto-02-discover.md",
            "auto-03-plan.md",
            "auto-04-architect.md",
            "auto-05-implement.md",
            "auto-06-test.md",
            "auto-07-deploy.md",
            "auto-08-doc.md",
        ]
        for phase in required_phases:
            assert (phases_dir / phase).exists(), f"Missing phase: {phase}"


class TestMemoryFiles:
    """Test memory files exist."""

    def test_memory_auto_exists(self):
        """Test that MEMORY-AUTO.json exists."""
        memory_auto = Path(__file__).parent.parent / "memory" / "MEMORY-AUTO.json"
        assert memory_auto.exists()

    def test_context_save_format_exists(self):
        """Test that CONTEXT-SAVE-FORMAT.md exists."""
        context_format = (
            Path(__file__).parent.parent / "memory" / "CONTEXT-SAVE-FORMAT.md"
        )
        assert context_format.exists()

    def test_resume_protocol_exists(self):
        """Test that RESUME-PROTOCOL.md exists."""
        resume_protocol = Path(__file__).parent.parent / "memory" / "RESUME-PROTOCOL.md"
        assert resume_protocol.exists()


class TestWorkflowFiles:
    """Test workflow files exist."""

    def test_auto_workflow_exists(self):
        """Test that auto.md workflow exists."""
        auto_workflow = Path(__file__).parent.parent / "workflows" / "auto.md"
        assert auto_workflow.exists()
