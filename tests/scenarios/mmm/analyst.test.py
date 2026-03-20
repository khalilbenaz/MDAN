"""Scenario tests for the Analyst agent."""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app"))

from mmm.agents.analyst.agent import Analyst


async def test_analyst_basic_analysis():
    """Test basic business analysis capability."""
    agent = Analyst()

    result = await agent.process(
        "Analyze the requirements for building a simple task management application"
    )

    assert result is not None
    assert len(result) > 0
    assert "analysis" in result.lower() or "requirement" in result.lower()
    print("✓ test_analyst_basic_analysis passed")


async def test_analyst_user_stories():
    """Test user story creation capability."""
    agent = Analyst()

    result = await agent.process(
        "Create user stories for a task management application with features like creating tasks, assigning them, and tracking progress"
    )

    assert result is not None
    assert len(result) > 0
    assert "user story" in result.lower() or "story" in result.lower()
    print("✓ test_analyst_user_stories passed")


async def test_analyst_requirements_gathering():
    """Test requirements gathering capability."""
    agent = Analyst()

    result = await agent.process(
        "Gather requirements for an e-commerce platform with product catalog, shopping cart, and payment processing"
    )

    assert result is not None
    assert len(result) > 0
    assert "requirement" in result.lower() or "functional" in result.lower()
    print("✓ test_analyst_requirements_gathering passed")


async def test_analyst_stakeholder_analysis():
    """Test stakeholder analysis capability."""
    agent = Analyst()

    result = await agent.process(
        "Identify and analyze stakeholders for a healthcare management system"
    )

    assert result is not None
    assert len(result) > 0
    assert "stakeholder" in result.lower() or "user" in result.lower()
    print("✓ test_analyst_stakeholder_analysis passed")


async def test_analyst_use_cases():
    """Test use case creation capability."""
    agent = Analyst()

    result = await agent.process(
        "Create use cases for a social media application with features like posting, commenting, and liking"
    )

    assert result is not None
    assert len(result) > 0
    assert "use case" in result.lower() or "scenario" in result.lower()
    print("✓ test_analyst_use_cases passed")


async def test_analyst_business_rules():
    """Test business rules definition capability."""
    agent = Analyst()

    result = await agent.process(
        "Define business rules for a banking application including transaction limits and approval workflows"
    )

    assert result is not None
    assert len(result) > 0
    assert "business rule" in result.lower() or "validation" in result.lower()
    print("✓ test_analyst_business_rules passed")


async def test_analyst_acceptance_criteria():
    """Test acceptance criteria definition capability."""
    agent = Analyst()

    result = await agent.process(
        "Define acceptance criteria for a user registration feature with email verification"
    )

    assert result is not None
    assert len(result) > 0
    assert "acceptance criteria" in result.lower() or "criteria" in result.lower()
    print("✓ test_analyst_acceptance_criteria passed")


async def main():
    """Run all scenario tests."""
    print("Running Analyst agent scenario tests...\n")

    tests = [
        test_analyst_basic_analysis,
        test_analyst_user_stories,
        test_analyst_requirements_gathering,
        test_analyst_stakeholder_analysis,
        test_analyst_use_cases,
        test_analyst_business_rules,
        test_analyst_acceptance_criteria,
    ]

    for test in tests:
        try:
            await test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            import traceback

            traceback.print_exc()

    print("\nAll Analyst agent scenario tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
