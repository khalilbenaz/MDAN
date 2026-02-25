"""Tests for CrewAI skill router."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from pathlib import Path
import tempfile
import json


class TestSkillRouter:
    """Test Skill Router."""

    @pytest.fixture
    def skill_router(self):
        """Create a Skill Router instance."""
        from integrations.crewai.skills.skill_router import SkillRouter

        return SkillRouter()

    def test_skill_router_creation(self, skill_router):
        """Test that Skill Router is created successfully."""
        assert skill_router is not None
        assert len(skill_router.skills) > 0

    def test_get_all_skills(self, skill_router):
        """Test getting all skills."""
        all_skills = skill_router.get_all_skills()
        assert isinstance(all_skills, dict)
        assert len(all_skills) > 0

    def test_get_skills_by_category(self, skill_router):
        """Test getting skills by category."""
        product_skills = skill_router.get_skills_by_category("product")
        assert isinstance(product_skills, dict)
        assert len(product_skills) > 0

    def test_route_task_to_skill(self, skill_router):
        """Test routing a task to a skill."""
        result = skill_router.route_task("Create a PRD")
        assert result is not None
        assert "skill" in result
        assert "agent" in result

    def test_route_task_to_skill_architecture(self, skill_router):
        """Test routing an architecture task."""
        result = skill_router.route_task("Design system architecture")
        assert result is not None
        assert result["agent"] == "architect"

    def test_route_task_to_skill_ux(self, skill_router):
        """Test routing a UX task."""
        result = skill_router.route_task("Design user interface")
        assert result is not None
        assert result["agent"] == "ux"

    def test_route_task_to_skill_development(self, skill_router):
        """Test routing a development task."""
        result = skill_router.route_task("Implement feature")
        assert result is not None
        assert result["agent"] == "dev"

    def test_route_task_to_skill_testing(self, skill_router):
        """Test routing a testing task."""
        result = skill_router.route_task("Write unit tests")
        assert result is not None
        assert result["agent"] == "test"

    def test_route_task_to_skill_security(self, skill_router):
        """Test routing a security task."""
        result = skill_router.route_task("Review security")
        assert result is not None
        assert result["agent"] == "security"

    def test_route_task_to_skill_devops(self, skill_router):
        """Test routing a DevOps task."""
        result = skill_router.route_task("Set up CI/CD")
        assert result is not None
        assert result["agent"] == "devops"

    def test_route_task_to_skill_documentation(self, skill_router):
        """Test routing a documentation task."""
        result = skill_router.route_task("Write documentation")
        assert result is not None
        assert result["agent"] == "doc"

    def test_get_skill_info(self, skill_router):
        """Test getting skill information."""
        skill_info = skill_router.get_skill_info("prd_creation")
        assert skill_info is not None
        assert "name" in skill_info
        assert "description" in skill_info
        assert "category" in skill_info
        assert "agent" in skill_info

    def test_get_skill_info_invalid(self, skill_router):
        """Test getting information for invalid skill."""
        skill_info = skill_router.get_skill_info("invalid_skill")
        assert skill_info is None

    def test_has_skill(self, skill_router):
        """Test checking if skill exists."""
        assert skill_router.has_skill("prd_creation") is True
        assert skill_router.has_skill("invalid_skill") is False

    def test_get_categories(self, skill_router):
        """Test getting all categories."""
        categories = skill_router.get_categories()
        assert isinstance(categories, list)
        assert len(categories) > 0
        assert "product" in categories
        assert "architecture" in categories
        assert "development" in categories

    def test_search_skills(self, skill_router):
        """Test searching skills by keyword."""
        results = skill_router.search_skills("PRD")
        assert isinstance(results, dict)
        assert len(results) > 0

    def test_search_skills_no_results(self, skill_router):
        """Test searching skills with no results."""
        results = skill_router.search_skills("xyz_invalid_keyword_xyz")
        assert isinstance(results, dict)
        assert len(results) == 0

    def test_get_agent_skills(self, skill_router):
        """Test getting skills for a specific agent."""
        dev_skills = skill_router.get_agent_skills("dev")
        assert isinstance(dev_skills, dict)
        assert len(dev_skills) > 0

    def test_get_agent_skills_invalid(self, skill_router):
        """Test getting skills for invalid agent."""
        dev_skills = skill_router.get_agent_skills("invalid_agent")
        assert isinstance(dev_skills, dict)
        assert len(dev_skills) == 0

    def test_skill_count(self, skill_router):
        """Test total skill count."""
        all_skills = skill_router.get_all_skills()
        assert len(all_skills) >= 50  # Should have at least 50 skills

    def test_all_skills_have_required_fields(self, skill_router):
        """Test that all skills have required fields."""
        all_skills = skill_router.get_all_skills()

        for skill_name, skill_info in all_skills.items():
            assert "name" in skill_info
            assert "description" in skill_info
            assert "category" in skill_info
            assert "agent" in skill_info

    def test_all_skills_have_valid_agents(self, skill_router):
        """Test that all skills have valid agent assignments."""
        valid_agents = [
            "product",
            "architect",
            "ux",
            "dev",
            "test",
            "security",
            "devops",
            "doc",
        ]
        all_skills = skill_router.get_all_skills()

        for skill_name, skill_info in all_skills.items():
            assert skill_info["agent"] in valid_agents
