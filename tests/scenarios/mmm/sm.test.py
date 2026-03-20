"""Scenario tests for the Scrum Master agent."""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app"))

from mmm.agents.sm.agent import SM


async def test_sm_sprint_facilitation():
    """Test sprint facilitation capability."""
    agent = SM()

    result = await agent.process(
        "Facilitate a sprint planning meeting for a team of 6 developers"
    )

    assert result is not None
    assert len(result) > 0
    assert "sprint" in result.lower() or "planning" in result.lower()
    print("✓ test_sm_sprint_facilitation passed")


async def test_sm_daily_standup():
    """Test daily standup facilitation capability."""
    agent = SM()

    result = await agent.process(
        "Facilitate a daily standup meeting and help the team identify blockers"
    )

    assert result is not None
    assert len(result) > 0
    assert "standup" in result.lower() or "daily" in result.lower()
    print("✓ test_sm_daily_standup passed")


async def test_sm_retrospective():
    """Test retrospective facilitation capability."""
    agent = SM()

    result = await agent.process(
        "Facilitate a sprint retrospective to help the team improve their processes"
    )

    assert result is not None
    assert len(result) > 0
    assert "retrospective" in result.lower() or "improve" in result.lower()
    print("✓ test_sm_retrospective passed")


async def test_sm_team_coaching():
    """Test team coaching capability."""
    agent = SM()

    result = await agent.process(
        "Coach a team on agile best practices and help them become more self-organizing"
    )

    assert result is not None
    assert len(result) > 0
    assert "coach" in result.lower() or "agile" in result.lower()
    print("✓ test_sm_team_coaching passed")


async def test_sm_blocker_resolution():
    """Test blocker resolution capability."""
    agent = SM()

    result = await agent.process(
        "Help the team identify and resolve blockers preventing them from completing their sprint goals"
    )

    assert result is not None
    assert len(result) > 0
    assert "blocker" in result.lower() or "impediment" in result.lower()
    print("✓ test_sm_blocker_resolution passed")


async def test_sm_velocity_tracking():
    """Test velocity tracking capability."""
    agent = SM()

    result = await agent.process(
        "Track and analyze team velocity to help with future sprint planning"
    )

    assert result is not None
    assert len(result) > 0
    assert "velocity" in result.lower() or "metric" in result.lower()
    print("✓ test_sm_velocity_tracking passed")


async def test_sm_process_improvement():
    """Test process improvement capability."""
    agent = SM()

    result = await agent.process(
        "Identify areas for process improvement and suggest changes to make the team more efficient"
    )

    assert result is not None
    assert len(result) > 0
    assert "process" in result.lower() or "improvement" in result.lower()
    print("✓ test_sm_process_improvement passed")


async def main():
    """Run all scenario tests."""
    print("Running Scrum Master agent scenario tests...\n")

    tests = [
        test_sm_sprint_facilitation,
        test_sm_daily_standup,
        test_sm_retrospective,
        test_sm_team_coaching,
        test_sm_blocker_resolution,
        test_sm_velocity_tracking,
        test_sm_process_improvement,
    ]

    for test in tests:
        try:
            await test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            import traceback

            traceback.print_exc()

    print("\nAll Scrum Master agent scenario tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
