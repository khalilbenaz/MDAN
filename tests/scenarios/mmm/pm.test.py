"""Scenario tests for the PM agent."""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app"))

from mmm.agents.pm.agent import PM


async def test_pm_project_planning():
    """Test project planning capability."""
    agent = PM()

    result = await agent.process(
        "Create a project plan for building a mobile banking application with a 6-month timeline"
    )

    assert result is not None
    assert len(result) > 0
    assert "project" in result.lower() or "plan" in result.lower()
    print("✓ test_pm_project_planning passed")


async def test_pm_backlog_management():
    """Test backlog management capability."""
    agent = PM()

    result = await agent.process(
        "Organize and prioritize the product backlog for an e-commerce platform"
    )

    assert result is not None
    assert len(result) > 0
    assert "backlog" in result.lower() or "priorit" in result.lower()
    print("✓ test_pm_backlog_management passed")


async def test_pm_sprint_planning():
    """Test sprint planning capability."""
    agent = PM()

    result = await agent.process(
        "Plan a 2-week sprint for a development team working on a task management application"
    )

    assert result is not None
    assert len(result) > 0
    assert "sprint" in result.lower() or "iteration" in result.lower()
    print("✓ test_pm_sprint_planning passed")


async def test_pm_stakeholder_communication():
    """Test stakeholder communication capability."""
    agent = PM()

    result = await agent.process(
        "Prepare a status report for stakeholders on the progress of a healthcare system project"
    )

    assert result is not None
    assert len(result) > 0
    assert "stakeholder" in result.lower() or "report" in result.lower()
    print("✓ test_pm_stakeholder_communication passed")


async def test_pm_risk_management():
    """Test risk management capability."""
    agent = PM()

    result = await agent.process(
        "Identify and mitigate risks for a critical financial system migration project"
    )

    assert result is not None
    assert len(result) > 0
    assert "risk" in result.lower() or "mitigat" in result.lower()
    print("✓ test_pm_risk_management passed")


async def test_pm_resource_allocation():
    """Test resource allocation capability."""
    agent = PM()

    result = await agent.process(
        "Allocate resources for a team of 8 developers working on multiple concurrent projects"
    )

    assert result is not None
    assert len(result) > 0
    assert "resource" in result.lower() or "team" in result.lower()
    print("✓ test_pm_resource_allocation passed")


async def test_pm_roadmap_creation():
    """Test roadmap creation capability."""
    agent = PM()

    result = await agent.process(
        "Create a product roadmap for a SaaS platform for the next 12 months"
    )

    assert result is not None
    assert len(result) > 0
    assert "roadmap" in result.lower() or "timeline" in result.lower()
    print("✓ test_pm_roadmap_creation passed")


async def main():
    """Run all scenario tests."""
    print("Running PM agent scenario tests...\n")

    tests = [
        test_pm_project_planning,
        test_pm_backlog_management,
        test_pm_sprint_planning,
        test_pm_stakeholder_communication,
        test_pm_risk_management,
        test_pm_resource_allocation,
        test_pm_roadmap_creation,
    ]

    for test in tests:
        try:
            await test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            import traceback

            traceback.print_exc()

    print("\nAll PM agent scenario tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
