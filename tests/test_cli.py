"""Tests for MDAN CLI commands."""

import sys
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest

# Add CLI directory to path
CLI_DIR = Path(__file__).parent.parent / "cli"
sys.path.insert(0, str(CLI_DIR))

import mdan


class TestVersion:
    """Test version command."""

    def test_version_constant(self):
        """Test that version constant is set."""
        assert mdan.VERSION == "2.5.1"

    def test_version_output(self, capsys):
        """Test version command output."""
        with patch("sys.argv", ["mdan", "version"]):
            mdan.main()
            captured = capsys.readouterr()
            assert "2.5.1" in captured.out


class TestHelp:
    """Test help command."""

    def test_help_displays_banner(self, capsys):
        """Test that help displays banner."""
        with patch("sys.argv", ["mdan", "help"]):
            mdan.main()
            captured = capsys.readouterr()
            assert "Multi-Agent Development Agentic Network" in captured.out

    def test_help_displays_commands(self, capsys):
        """Test that help displays available commands."""
        with patch("sys.argv", ["mdan", "help"]):
            mdan.main()
            captured = capsys.readouterr()
            assert "init" in captured.out
            assert "attach" in captured.out
            assert "auto" in captured.out
            assert "resume" in captured.out


class TestInit:
    """Test init command."""

    def test_init_creates_project(self, temp_dir):
        """Test that init creates project directory."""
        project_name = "test-project"
        project_path = temp_dir / project_name

        with patch("sys.argv", ["mdan", "init", str(project_path)]):
            mdan.main()

        assert project_path.exists()
        assert (project_path / "mdan").exists()
        assert (project_path / "mdan_output").exists()

    def test_init_creates_directories(self, temp_dir):
        """Test that init creates required directories."""
        project_name = "test-dirs"
        project_path = temp_dir / project_name

        with patch("sys.argv", ["mdan", "init", str(project_path)]):
            mdan.main()

        assert (project_path / "mdan" / "agents").exists()
        assert (project_path / "mdan" / "skills").exists()
        assert (project_path / "mdan_output").exists()
        assert (project_path / ".claude" / "skills").exists()
        assert (project_path / ".github").exists()

    def test_init_copies_orchestrator(self, temp_dir):
        """Test that init copies orchestrator file."""
        project_name = "test-orchestrator"
        project_path = temp_dir / project_name

        with patch("sys.argv", ["mdan", "init", str(project_path)]):
            mdan.main()

        assert (project_path / "mdan" / "orchestrator.md").exists()
        assert (project_path / "mdan" / "universal-envelope.md").exists()

    def test_init_copies_agents(self, temp_dir):
        """Test that init copies agent files."""
        project_name = "test-agents"
        project_path = temp_dir / project_name

        with patch("sys.argv", ["mdan", "init", str(project_path)]):
            mdan.main()

        agents_dir = project_path / "mdan" / "agents"
        assert agents_dir.exists()
        assert (agents_dir / "product.md").exists()
        assert (agents_dir / "architect.md").exists()
        assert (agents_dir / "dev.md").exists()

    def test_init_creates_cursorrules(self, temp_dir):
        """Test that init creates .cursorrules file."""
        project_name = "test-cursorrules"
        project_path = temp_dir / project_name

        with patch("sys.argv", ["mdan", "init", str(project_path)]):
            mdan.main()

        assert (project_path / ".cursorrules").exists()
        assert (project_path / ".windsurfrules").exists()

    def test_init_creates_readme(self, temp_dir):
        """Test that init creates README.md."""
        project_name = "test-readme"
        project_path = temp_dir / project_name

        with patch("sys.argv", ["mdan", "init", str(project_path)]):
            mdan.main()

        readme = project_path / "README.md"
        assert readme.exists()
        content = readme.read_text()
        assert "Built with MDAN" in content


class TestAttach:
    """Test attach command."""

    def test_attach_creates_structure(self, temp_dir):
        """Test that attach creates MDAN structure."""
        import os

        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            mdan.cmd_attach()
        finally:
            os.chdir(original_cwd)

        assert (temp_dir / "mdan" / "agents").exists()
        assert (temp_dir / "mdan" / "skills").exists()
        assert (temp_dir / ".claude" / "skills").exists()
        assert (temp_dir / ".github").exists()

    def test_attach_rebuild_mode(self, temp_dir):
        """Test attach with --rebuild flag."""
        import os

        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            mdan.cmd_attach("--rebuild")
        finally:
            os.chdir(original_cwd)

        cursorrules = temp_dir / ".cursorrules"
        assert cursorrules.exists()
        content = cursorrules.read_text()
        assert "REBUILD MODE" in content


class TestAuto:
    """Test auto command."""

    def test_auto_displays_info(self, capsys):
        """Test that auto displays autonomous mode info."""
        with patch("sys.argv", ["mdan", "auto"]):
            mdan.main()
            captured = capsys.readouterr()
            assert "MDAN-AUTO v1.0" in captured.out
            assert "Autonomous Development Mode" in captured.out
            assert "LOAD" in captured.out
            assert "DISCOVER" in captured.out
            assert "PLAN" in captured.out
            assert "ARCHITECT" in captured.out
            assert "IMPLEMENT" in captured.out
            assert "TEST" in captured.out
            assert "DEPLOY" in captured.out
            assert "DOC" in captured.out


class TestResume:
    """Test resume command."""

    def test_resume_with_valid_file(self, temp_dir, capsys):
        """Test resume with valid save file."""
        import json

        save_data = {
            "project": {"name": "test-project"},
            "phases": {
                "current": "IMPLEMENT",
                "completed": ["LOAD", "DISCOVER", "PLAN", "ARCHITECT"],
            },
            "context": {
                "token_usage": {"total": 50000, "limit": 128000, "percentage": 0.39}
            },
        }

        save_file = temp_dir / "mdan-save-test.json"
        save_file.write_text(json.dumps(save_data))

        with patch("sys.argv", ["mdan", "resume", str(save_file)]):
            mdan.main()
            captured = capsys.readouterr()
            assert "test-project" in captured.out
            assert "IMPLEMENT" in captured.out
            assert "LOAD" in captured.out
            assert "39.0%" in captured.out

    def test_resume_with_invalid_file(self, temp_dir, capsys):
        """Test resume with invalid save file."""
        save_file = temp_dir / "invalid.json"
        save_file.write_text("invalid json")

        with patch("sys.argv", ["mdan", "resume", str(save_file)]):
            mdan.main()
            captured = capsys.readouterr()
            assert "Error" in captured.out

    def test_resume_with_missing_file(self, capsys):
        """Test resume with missing save file."""
        with patch("sys.argv", ["mdan", "resume", "/tmp/nonexistent.json"]):
            mdan.main()
            captured = capsys.readouterr()
            assert "Error" in captured.out


class TestPhase:
    """Test phase command."""

    def test_phase_displays_content(self, capsys):
        """Test that phase displays phase content."""
        with patch("sys.argv", ["mdan", "phase", "1"]):
            mdan.main()
            captured = capsys.readouterr()
            assert "DISCOVER" in captured.out

    def test_phase_with_name(self, capsys):
        """Test phase with phase name."""
        with patch("sys.argv", ["mdan", "phase", "discover"]):
            mdan.main()
            captured = capsys.readouterr()
            assert "DISCOVER" in captured.out

    def test_phase_invalid(self, capsys):
        """Test phase with invalid phase."""
        with patch("sys.argv", ["mdan", "phase", "invalid"]):
            mdan.main()
            captured = capsys.readouterr()
            assert "Usage" in captured.out


class TestAgent:
    """Test agent command."""

    def test_agent_displays_content(self, capsys):
        """Test that agent displays agent content."""
        with patch("sys.argv", ["mdan", "agent", "product"]):
            mdan.main()
            captured = capsys.readouterr()
            assert "Product" in captured.out

    def test_agent_lists_agents(self, capsys):
        """Test that agent lists available agents."""
        with patch("sys.argv", ["mdan", "agent"]):
            mdan.main()
            captured = capsys.readouterr()
            assert "product" in captured.out
            assert "architect" in captured.out
            assert "dev" in captured.out


class TestSkills:
    """Test skills command."""

    def test_skills_lists_skills(self, capsys):
        """Test that skills lists available skills."""
        with patch("sys.argv", ["mdan", "skills"]):
            mdan.main()
            captured = capsys.readouterr()
            assert "Skills:" in captured.out


class TestStatus:
    """Test status command."""

    def test_status_no_project(self, temp_dir, capsys):
        """Test status when no MDAN project."""
        import os

        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            mdan.cmd_status()
        finally:
            os.chdir(original_cwd)

        captured = capsys.readouterr()
        assert (
            "No MDAN project" in captured.out or "No MDAN project here" in captured.out
        )
