"""Tests for CrewAI flows."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from pathlib import Path
import tempfile
import json


class TestAutoFlow:
    """Test Auto Flow."""

    @pytest.fixture
    def auto_flow(self, temp_dir):
        """Create an Auto Flow instance."""
        from integrations.crewai.flows.auto_flow import AutoFlow

        mock_llm = Mock()

        return AutoFlow(
            project_path=str(temp_dir),
            llm=mock_llm,
            sql_config=None,
            serper_api_key=None,
        )

    def test_auto_flow_creation(self, auto_flow):
        """Test that Auto Flow is created successfully."""
        assert auto_flow is not None
        assert auto_flow.project_path is not None

    def test_auto_flow_has_phases(self, auto_flow):
        """Test that Auto Flow has all required phases."""
        phases = auto_flow.get_phases()
        expected_phases = [
            "LOAD",
            "DISCOVER",
            "PLAN",
            "ARCHITECT",
            "IMPLEMENT",
            "TEST",
            "DEPLOY",
            "DOC",
        ]
        assert len(phases) == len(expected_phases)
        for phase in expected_phases:
            assert phase in phases


class TestDiscoveryFlow:
    """Test Discovery Flow."""

    @pytest.fixture
    def discovery_flow(self, temp_dir):
        """Create a Discovery Flow instance."""
        from integrations.crewai.flows.discovery_flow import DiscoveryFlow

        mock_llm = Mock()

        return DiscoveryFlow(
            project_path=str(temp_dir),
            llm=mock_llm,
            sql_config=None,
            serper_api_key=None,
        )

    def test_discovery_flow_creation(self, discovery_flow):
        """Test that Discovery Flow is created successfully."""
        assert discovery_flow is not None
        assert discovery_flow.project_path is not None

    def test_discovery_flow_has_tasks(self, discovery_flow):
        """Test that Discovery Flow has required tasks."""
        tasks = discovery_flow.get_tasks()
        assert len(tasks) > 0
        task_names = [task.get("name", "") for task in tasks]
        assert any("PRD" in name or "prd" in name for name in task_names)


class TestBuildFlow:
    """Test Build Flow."""

    @pytest.fixture
    def build_flow(self, temp_dir):
        """Create a Build Flow instance."""
        from integrations.crewai.flows.build_flow import BuildFlow

        mock_llm = Mock()

        return BuildFlow(
            project_path=str(temp_dir),
            llm=mock_llm,
            sql_config=None,
            serper_api_key=None,
        )

    def test_build_flow_creation(self, build_flow):
        """Test that Build Flow is created successfully."""
        assert build_flow is not None
        assert build_flow.project_path is not None

    def test_build_flow_has_tasks(self, build_flow):
        """Test that Build Flow has required tasks."""
        tasks = build_flow.get_tasks()
        assert len(tasks) > 0


class TestDebateFlow:
    """Test Debate Flow."""

    @pytest.fixture
    def debate_flow(self, temp_dir):
        """Create a Debate Flow instance."""
        from integrations.crewai.flows.debate_flow import DebateFlow

        mock_llm = Mock()

        return DebateFlow(
            project_path=str(temp_dir),
            llm=mock_llm,
            sql_config=None,
            serper_api_key=None,
        )

    def test_debate_flow_creation(self, debate_flow):
        """Test that Debate Flow is created successfully."""
        assert debate_flow is not None
        assert debate_flow.project_path is not None

    def test_debate_flow_has_rounds(self, debate_flow):
        """Test that Debate Flow has required rounds."""
        rounds = debate_flow.get_rounds()
        assert len(rounds) == 3
        assert "initial" in rounds
        assert "counterarguments" in rounds
        assert "consensus" in rounds


class TestAllFlows:
    """Test all flows together."""

    def test_all_flows_have_unique_names(self):
        """Test that all flows have unique names."""
        from integrations.crewai.flows.auto_flow import AutoFlow
        from integrations.crewai.flows.discovery_flow import DiscoveryFlow
        from integrations.crewai.flows.build_flow import BuildFlow
        from integrations.crewai.flows.debate_flow import DebateFlow

        mock_llm = Mock()

        flows = [
            AutoFlow(project_path="/tmp", llm=mock_llm),
            DiscoveryFlow(project_path="/tmp", llm=mock_llm),
            BuildFlow(project_path="/tmp", llm=mock_llm),
            DebateFlow(project_path="/tmp", llm=mock_llm),
        ]

        flow_names = [flow.__class__.__name__ for flow in flows]
        assert len(flow_names) == len(set(flow_names)), "Flow names must be unique"
