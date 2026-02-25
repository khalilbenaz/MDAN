"""Tests for CrewAI orchestrator."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from pathlib import Path
import tempfile
import json
import asyncio
import importlib.util

# Skip all tests if CrewAI is not installed
pytestmark = pytest.mark.skipif(
    importlib.util.find_spec("crewai") is None,
    reason="CrewAI not installed - optional integration",
)


class TestCrewAIOrchestrator:
    """Test CrewAI Orchestrator."""

    @pytest.fixture
    def orchestrator(self, temp_dir):
        """Create a CrewAI Orchestrator instance."""
        from integrations.crewai.orchestrator import CrewAIOrchestrator

        mock_llm = Mock()

        return CrewAIOrchestrator(
            project_path=str(temp_dir),
            llm=mock_llm,
            auto_mode=False,
        )

    def test_orchestrator_creation(self, orchestrator):
        """Test that Orchestrator is created successfully."""
        assert orchestrator is not None
        assert orchestrator.project_path is not None
        assert orchestrator.auto_mode is False

    def test_orchestrator_has_agents(self, orchestrator):
        """Test that Orchestrator has all required agents."""
        expected_agents = [
            "product",
            "architect",
            "ux",
            "dev",
            "test",
            "security",
            "devops",
            "doc",
        ]
        for agent_name in expected_agents:
            assert agent_name in orchestrator.agents

    def test_orchestrator_has_flows(self, orchestrator):
        """Test that Orchestrator has all required flows."""
        expected_flows = ["auto", "discovery", "build", "debate"]
        for flow_name in expected_flows:
            assert flow_name in orchestrator.flows

    def test_orchestrator_has_tools(self, orchestrator):
        """Test that Orchestrator has all required tools."""
        assert orchestrator.file_tool is not None

    def test_analyze_task_product(self, orchestrator):
        """Test task analysis for product tasks."""
        result = orchestrator.analyze_task("Create a PRD for a todo app")
        assert result["type"] == "agent"
        assert result["agent"] == "product"

    def test_analyze_task_architect(self, orchestrator):
        """Test task analysis for architect tasks."""
        result = orchestrator.analyze_task("Design the system architecture")
        assert result["type"] == "agent"
        assert result["agent"] == "architect"

    def test_analyze_task_ux(self, orchestrator):
        """Test task analysis for UX tasks."""
        result = orchestrator.analyze_task("Design the user interface")
        assert result["type"] == "agent"
        assert result["agent"] == "ux"

    def test_analyze_task_dev(self, orchestrator):
        """Test task analysis for dev tasks."""
        result = orchestrator.analyze_task("Implement the feature")
        assert result["type"] == "agent"
        assert result["agent"] == "dev"

    def test_analyze_task_test(self, orchestrator):
        """Test task analysis for test tasks."""
        result = orchestrator.analyze_task("Write unit tests")
        assert result["type"] == "agent"
        assert result["agent"] == "test"

    def test_analyze_task_security(self, orchestrator):
        """Test task analysis for security tasks."""
        result = orchestrator.analyze_task("Review security vulnerabilities")
        assert result["type"] == "agent"
        assert result["agent"] == "security"

    def test_analyze_task_devops(self, orchestrator):
        """Test task analysis for DevOps tasks."""
        result = orchestrator.analyze_task("Set up CI/CD pipeline")
        assert result["type"] == "agent"
        assert result["agent"] == "devops"

    def test_analyze_task_doc(self, orchestrator):
        """Test task analysis for documentation tasks."""
        result = orchestrator.analyze_task("Write API documentation")
        assert result["type"] == "agent"
        assert result["agent"] == "doc"

    def test_analyze_task_auto_flow(self, orchestrator):
        """Test task analysis for auto flow."""
        result = orchestrator.analyze_task("Auto build a complete application")
        assert result["type"] == "flow"
        assert result["flow"] == "auto"

    def test_analyze_task_discovery_flow(self, orchestrator):
        """Test task analysis for discovery flow."""
        result = orchestrator.analyze_task("Discover requirements for the project")
        assert result["type"] == "flow"
        assert result["flow"] == "discovery"

    def test_analyze_task_build_flow(self, orchestrator):
        """Test task analysis for build flow."""
        result = orchestrator.analyze_task("Build the application")
        assert result["type"] == "flow"
        assert result["flow"] == "build"

    def test_analyze_task_debate_flow(self, orchestrator):
        """Test task analysis for debate flow."""
        result = orchestrator.analyze_task("Debate the architecture decision")
        assert result["type"] == "flow"
        assert result["flow"] == "debate"

    def test_get_state(self, orchestrator):
        """Test getting orchestrator state."""
        state = orchestrator.get_state()
        assert "current_phase" in state
        assert "active_agents" in state
        assert "task_history" in state
        assert "auto_mode_enabled" in state

    def test_save_and_load_state(self, orchestrator, temp_dir):
        """Test saving and loading orchestrator state."""
        state_file = temp_dir / "test_state.json"

        orchestrator.state["current_phase"] = "TEST"
        orchestrator.state["task_history"].append({"test": "task"})

        orchestrator.save_state(str(state_file))
        assert state_file.exists()

        new_orchestrator = orchestrator.__class__(
            project_path=str(temp_dir),
            llm=Mock(),
        )
        new_orchestrator.load_state(str(state_file))

        assert new_orchestrator.state["current_phase"] == "TEST"
        assert len(new_orchestrator.state["task_history"]) == 1

    def test_enable_auto_mode(self, orchestrator):
        """Test enabling auto mode."""
        orchestrator.enable_auto_mode()
        assert orchestrator.is_auto_mode_enabled() is True
        assert orchestrator.state["auto_mode_enabled"] is True

    def test_disable_auto_mode(self, orchestrator):
        """Test disabling auto mode."""
        orchestrator.enable_auto_mode()
        orchestrator.disable_auto_mode()
        assert orchestrator.is_auto_mode_enabled() is False
        assert orchestrator.state["auto_mode_enabled"] is False

    def test_create_crew(self, orchestrator):
        """Test creating a crew."""
        crew = orchestrator.create_crew(["product", "architect"])
        assert crew is not None
        assert len(crew.agents) == 2

    def test_create_crew_invalid_agents(self, orchestrator):
        """Test creating a crew with invalid agents."""
        with pytest.raises(ValueError):
            orchestrator.create_crew(["invalid_agent"])

    @pytest.mark.asyncio
    async def test_execute_task_with_agent(self, orchestrator):
        """Test executing a task with an agent."""
        with patch.object(orchestrator, "_execute_agent_task") as mock_execute:
            mock_execute.return_value = {"status": "success", "result": "done"}

            result = await orchestrator.execute_task("Test task")
            assert result["status"] == "success"

    @pytest.mark.asyncio
    async def test_execute_task_with_flow(self, orchestrator):
        """Test executing a task with a flow."""
        with patch.object(orchestrator, "_execute_flow") as mock_execute:
            mock_execute.return_value = {"status": "success", "result": "done"}

            result = await orchestrator.execute_task("Auto build app")
            assert result["status"] == "success"
