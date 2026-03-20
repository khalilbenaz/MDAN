"""Scenario tests for the Quick Flow Solo Dev agent."""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app"))

from mmm.agents.quick_flow_solo_dev.agent import QuickFlowSoloDev


async def test_quick_flow_full_feature():
    """Test full feature development capability."""
    agent = QuickFlowSoloDev()

    result = await agent.process(
        "Build a complete user authentication feature with login, registration, and password reset"
    )

    assert result is not None
    assert len(result) > 0
    assert "feature" in result.lower() or "implement" in result.lower()
    print("✓ test_quick_flow_full_feature passed")


async def test_quick_flow_rapid_prototyping():
    """Test rapid prototyping capability."""
    agent = QuickFlowSoloDev()

    result = await agent.process(
        "Create a quick prototype for a dashboard with charts and data visualization"
    )

    assert result is not None
    assert len(result) > 0
    assert "prototype" in result.lower() or "dashboard" in result.lower()
    print("✓ test_quick_flow_rapid_prototyping passed")


async def test_quick_flow_mvp_development():
    """Test MVP development capability."""
    agent = QuickFlowSoloDev()

    result = await agent.process(
        "Build an MVP for a task management application with basic CRUD operations"
    )

    assert result is not None
    assert len(result) > 0
    assert "mvp" in result.lower() or "minimum viable" in result.lower()
    print("✓ test_quick_flow_mvp_development passed")


async def test_quick_flow_end_to_end():
    """Test end-to-end development capability."""
    agent = QuickFlowSoloDev()

    result = await agent.process(
        "Develop a complete blog application from backend to frontend with authentication"
    )

    assert result is not None
    assert len(result) > 0
    assert "end-to-end" in result.lower() or "complete" in result.lower()
    print("✓ test_quick_flow_end_to_end passed")


async def test_quick_flow_bug_fixing():
    """Test quick bug fixing capability."""
    agent = QuickFlowSoloDev()

    result = await agent.process(
        "Quickly fix a critical bug preventing users from logging in to the application"
    )

    assert result is not None
    assert len(result) > 0
    assert "fix" in result.lower() or "bug" in result.lower()
    print("✓ test_quick_flow_bug_fixing passed")


async def test_quick_flow_feature_iteration():
    """Test feature iteration capability."""
    agent = QuickFlowSoloDev()

    result = await agent.process(
        "Iterate on an existing feature to add new functionality based on user feedback"
    )

    assert result is not None
    assert len(result) > 0
    assert "iterate" in result.lower() or "improve" in result.lower()
    print("✓ test_quick_flow_feature_iteration passed")


async def test_quick_flow_deployment():
    """Test deployment capability."""
    agent = QuickFlowSoloDev()

    result = await agent.process(
        "Prepare and deploy a web application to production with proper configuration"
    )

    assert result is not None
    assert len(result) > 0
    assert "deploy" in result.lower() or "production" in result.lower()
    print("✓ test_quick_flow_deployment passed")


async def main():
    """Run all scenario tests."""
    print("Running Quick Flow Solo Dev agent scenario tests...\n")

    tests = [
        test_quick_flow_full_feature,
        test_quick_flow_rapid_prototyping,
        test_quick_flow_mvp_development,
        test_quick_flow_end_to_end,
        test_quick_flow_bug_fixing,
        test_quick_flow_feature_iteration,
        test_quick_flow_deployment,
    ]

    for test in tests:
        try:
            await test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            import traceback

            traceback.print_exc()

    print("\nAll Quick Flow Solo Dev agent scenario tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
