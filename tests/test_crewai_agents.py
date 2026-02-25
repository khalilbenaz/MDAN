"""Tests for CrewAI agents."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from pathlib import Path
import tempfile
import json


class TestProductAgent:
    """Test Product Agent."""

    @pytest.fixture
    def product_agent(self):
        """Create a Product Agent instance."""
        from integrations.crewai.agents.product_agent import ProductAgent

        mock_llm = Mock()
        mock_llm.temperature = 0.7

        return ProductAgent(
            llm=mock_llm,
            sql_tool=None,
            serper_tool=None,
            file_tool=None,
        )

    def test_product_agent_creation(self, product_agent):
        """Test that Product Agent is created successfully."""
        assert product_agent is not None
        assert product_agent.name == "Khalil"
        assert product_agent.role == "Product Manager"

    def test_product_agent_get_agent(self, product_agent):
        """Test getting the CrewAI agent."""
        agent = product_agent.get_agent()
        assert agent is not None
        assert agent.role == "Product Manager"

    def test_product_agent_tasks(self, product_agent):
        """Test Product Agent task creation."""
        task = product_agent.create_prd_task("Build a todo app")
        assert task is not None
        assert (
            "PRD" in task.description
            or "Product Requirements Document" in task.description
        )


class TestArchitectAgent:
    """Test Architect Agent."""

    @pytest.fixture
    def architect_agent(self):
        """Create an Architect Agent instance."""
        from integrations.crewai.agents.architect_agent import ArchitectAgent

        mock_llm = Mock()
        mock_llm.temperature = 0.5

        return ArchitectAgent(
            llm=mock_llm,
            sql_tool=None,
            serper_tool=None,
            file_tool=None,
        )

    def test_architect_agent_creation(self, architect_agent):
        """Test that Architect Agent is created successfully."""
        assert architect_agent is not None
        assert architect_agent.name == "Reda"
        assert architect_agent.role == "Software Architect"

    def test_architect_agent_get_agent(self, architect_agent):
        """Test getting the CrewAI agent."""
        agent = architect_agent.get_agent()
        assert agent is not None
        assert agent.role == "Software Architect"


class TestUXAgent:
    """Test UX Agent."""

    @pytest.fixture
    def ux_agent(self):
        """Create a UX Agent instance."""
        from integrations.crewai.agents.ux_agent import UXAgent

        mock_llm = Mock()
        mock_llm.temperature = 0.6

        return UXAgent(
            llm=mock_llm,
            sql_tool=None,
            serper_tool=None,
            file_tool=None,
        )

    def test_ux_agent_creation(self, ux_agent):
        """Test that UX Agent is created successfully."""
        assert ux_agent is not None
        assert ux_agent.name == "Jihane"
        assert ux_agent.role == "UX Designer"

    def test_ux_agent_get_agent(self, ux_agent):
        """Test getting the CrewAI agent."""
        agent = ux_agent.get_agent()
        assert agent is not None
        assert agent.role == "UX Designer"


class TestDevAgent:
    """Test Dev Agent."""

    @pytest.fixture
    def dev_agent(self):
        """Create a Dev Agent instance."""
        from integrations.crewai.agents.dev_agent import DevAgent

        mock_llm = Mock()
        mock_llm.temperature = 0.3

        return DevAgent(
            llm=mock_llm,
            sql_tool=None,
            serper_tool=None,
            file_tool=None,
        )

    def test_dev_agent_creation(self, dev_agent):
        """Test that Dev Agent is created successfully."""
        assert dev_agent is not None
        assert dev_agent.name == "Haytame"
        assert dev_agent.role == "Software Developer"

    def test_dev_agent_get_agent(self, dev_agent):
        """Test getting the CrewAI agent."""
        agent = dev_agent.get_agent()
        assert agent is not None
        assert agent.role == "Software Developer"


class TestTestAgent:
    """Test Test Agent."""

    @pytest.fixture
    def test_agent(self):
        """Create a Test Agent instance."""
        from integrations.crewai.agents.test_agent import TestAgent

        mock_llm = Mock()
        mock_llm.temperature = 0.4

        return TestAgent(
            llm=mock_llm,
            sql_tool=None,
            serper_tool=None,
            file_tool=None,
        )

    def test_test_agent_creation(self, test_agent):
        """Test that Test Agent is created successfully."""
        assert test_agent is not None
        assert test_agent.name == "Youssef"
        assert test_agent.role == "QA Engineer"

    def test_test_agent_get_agent(self, test_agent):
        """Test getting the CrewAI agent."""
        agent = test_agent.get_agent()
        assert agent is not None
        assert agent.role == "QA Engineer"


class TestSecurityAgent:
    """Test Security Agent."""

    @pytest.fixture
    def security_agent(self):
        """Create a Security Agent instance."""
        from integrations.crewai.agents.security_agent import SecurityAgent

        mock_llm = Mock()
        mock_llm.temperature = 0.2

        return SecurityAgent(
            llm=mock_llm,
            sql_tool=None,
            serper_tool=None,
            file_tool=None,
        )

    def test_security_agent_creation(self, security_agent):
        """Test that Security Agent is created successfully."""
        assert security_agent is not None
        assert security_agent.name == "Said"
        assert security_agent.role == "Security Engineer"

    def test_security_agent_get_agent(self, security_agent):
        """Test getting the CrewAI agent."""
        agent = security_agent.get_agent()
        assert agent is not None
        assert agent.role == "Security Engineer"


class TestDevOpsAgent:
    """Test DevOps Agent."""

    @pytest.fixture
    def devops_agent(self):
        """Create a DevOps Agent instance."""
        from integrations.crewai.agents.devops_agent import DevOpsAgent

        mock_llm = Mock()
        mock_llm.temperature = 0.4

        return DevOpsAgent(
            llm=mock_llm,
            sql_tool=None,
            serper_tool=None,
            file_tool=None,
        )

    def test_devops_agent_creation(self, devops_agent):
        """Test that DevOps Agent is created successfully."""
        assert devops_agent is not None
        assert devops_agent.name == "Anas"
        assert devops_agent.role == "DevOps Engineer"

    def test_devops_agent_get_agent(self, devops_agent):
        """Test getting the CrewAI agent."""
        agent = devops_agent.get_agent()
        assert agent is not None
        assert agent.role == "DevOps Engineer"


class TestDocAgent:
    """Test Doc Agent."""

    @pytest.fixture
    def doc_agent(self):
        """Create a Doc Agent instance."""
        from integrations.crewai.agents.doc_agent import DocAgent

        mock_llm = Mock()
        mock_llm.temperature = 0.5

        return DocAgent(
            llm=mock_llm,
            sql_tool=None,
            serper_tool=None,
            file_tool=None,
        )

    def test_doc_agent_creation(self, doc_agent):
        """Test that Doc Agent is created successfully."""
        assert doc_agent is not None
        assert doc_agent.name == "Amina"
        assert doc_agent.role == "Technical Writer"

    def test_doc_agent_get_agent(self, doc_agent):
        """Test getting the CrewAI agent."""
        agent = doc_agent.get_agent()
        assert agent is not None
        assert agent.role == "Technical Writer"


class TestAllAgents:
    """Test all agents together."""

    def test_all_agents_have_unique_names(self):
        """Test that all agents have unique names."""
        from integrations.crewai.agents.product_agent import ProductAgent
        from integrations.crewai.agents.architect_agent import ArchitectAgent
        from integrations.crewai.agents.ux_agent import UXAgent
        from integrations.crewai.agents.dev_agent import DevAgent
        from integrations.crewai.agents.test_agent import TestAgent
        from integrations.crewai.agents.security_agent import SecurityAgent
        from integrations.crewai.agents.devops_agent import DevOpsAgent
        from integrations.crewai.agents.doc_agent import DocAgent

        mock_llm = Mock()

        agents = [
            ProductAgent(llm=mock_llm),
            ArchitectAgent(llm=mock_llm),
            UXAgent(llm=mock_llm),
            DevAgent(llm=mock_llm),
            TestAgent(llm=mock_llm),
            SecurityAgent(llm=mock_llm),
            DevOpsAgent(llm=mock_llm),
            DocAgent(llm=mock_llm),
        ]

        names = [agent.name for agent in agents]
        assert len(names) == len(set(names)), "Agent names must be unique"

    def test_all_agents_have_unique_roles(self):
        """Test that all agents have unique roles."""
        from integrations.crewai.agents.product_agent import ProductAgent
        from integrations.crewai.agents.architect_agent import ArchitectAgent
        from integrations.crewai.agents.ux_agent import UXAgent
        from integrations.crewai.agents.dev_agent import DevAgent
        from integrations.crewai.agents.test_agent import TestAgent
        from integrations.crewai.agents.security_agent import SecurityAgent
        from integrations.crewai.agents.devops_agent import DevOpsAgent
        from integrations.crewai.agents.doc_agent import DocAgent

        mock_llm = Mock()

        agents = [
            ProductAgent(llm=mock_llm),
            ArchitectAgent(llm=mock_llm),
            UXAgent(llm=mock_llm),
            DevAgent(llm=mock_llm),
            TestAgent(llm=mock_llm),
            SecurityAgent(llm=mock_llm),
            DevOpsAgent(llm=mock_llm),
            DocAgent(llm=mock_llm),
        ]

        roles = [agent.role for agent in agents]
        assert len(roles) == len(set(roles)), "Agent roles must be unique"
