"""
Scenario tests for Design Thinking Coach agent
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from app.cis.agents.design_thinking_coach import (
    DesignThinkingCoach,
    DesignThinkingCoachRequest,
)


async def test_design_thinking_full_process():
    """Test full design thinking process."""
    agent = DesignThinkingCoach()
    request = DesignThinkingCoachRequest(
        challenge="Improve online shopping experience", phase="full"
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["agent"] == "Maya"
    assert result["challenge"] == "Improve online shopping experience"
    assert result["phase"] == "full"
    assert "process" in result
    assert "activities" in result
    print("✓ test_design_thinking_full_process passed")


async def test_design_thinking_empathize_phase():
    """Test design thinking with empathize phase."""
    agent = DesignThinkingCoach()
    request = DesignThinkingCoachRequest(
        challenge="Redesign mobile app navigation",
        phase="empathize",
        target_users="Millennial shoppers",
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["phase"] == "empathize"
    assert result["target_users"] == "Millennial shoppers"
    # Check that empathize activities are included
    activities = result["activities"]
    assert any(a["phase"] == "Empathize" for a in activities)
    print("✓ test_design_thinking_empathize_phase passed")


async def test_design_thinking_ideate_phase():
    """Test design thinking with ideate phase."""
    agent = DesignThinkingCoach()
    request = DesignThinkingCoachRequest(
        challenge="Create new product features", phase="ideate"
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["phase"] == "ideate"
    # Check that ideate activities are included
    activities = result["activities"]
    assert any(a["phase"] == "Ideate" for a in activities)
    print("✓ test_design_thinking_ideate_phase passed")


async def test_design_thinking_with_constraints():
    """Test design thinking with constraints."""
    agent = DesignThinkingCoach()
    request = DesignThinkingCoachRequest(
        challenge="Design sustainable packaging",
        phase="full",
        constraints="Budget limited, must use recycled materials",
        goals="Reduce environmental impact",
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["constraints"] == "Budget limited, must use recycled materials"
    assert result["goals"] == "Reduce environmental impact"
    print("✓ test_design_thinking_with_constraints passed")


async def test_design_thinking_process_structure():
    """Test that process structure is generated correctly."""
    agent = DesignThinkingCoach()
    request = DesignThinkingCoachRequest(challenge="Improve customer service")
    result = await agent.process(request)
    assert result["success"] == True
    process = result["process"]
    assert "approach" in process
    if result["phase"] == "full":
        assert "phases" in process
        phases = process["phases"]
        assert "empathize" in phases
        assert "define" in phases
        assert "ideate" in phases
        assert "prototype" in phases
        assert "test" in phases
    print("✓ test_design_thinking_process_structure passed")


async def test_design_thinking_activities():
    """Test that activities are created for each phase."""
    agent = DesignThinkingCoach()
    request = DesignThinkingCoachRequest(
        challenge="Create new user onboarding flow", phase="full"
    )
    result = await agent.process(request)
    assert result["success"] == True
    activities = result["activities"]
    assert len(activities) >= 5
    # Check activity structure
    for activity in activities:
        assert "phase" in activity
        assert "activity" in activity
        assert "description" in activity
        assert "duration" in activity
    print("✓ test_design_thinking_activities passed")


async def test_design_thinking_facilitation():
    """Test that facilitation guidance is provided."""
    agent = DesignThinkingCoach()
    request = DesignThinkingCoachRequest(challenge="Redesign website homepage")
    result = await agent.process(request)
    assert result["success"] == True
    facilitation = result["facilitation"]
    assert "mindset" in facilitation
    assert "tips" in facilitation
    assert "common_pitfalls" in facilitation
    assert "success_metrics" in facilitation
    assert len(facilitation["mindset"]) > 0
    assert len(facilitation["tips"]) > 0
    print("✓ test_design_thinking_facilitation passed")


async def test_design_thinking_principles():
    """Test that design thinking principles are included."""
    agent = DesignThinkingCoach()
    request = DesignThinkingCoachRequest(challenge="Improve product usability")
    result = await agent.process(request)
    assert result["success"] == True
    principles = result["principles"]
    assert len(principles) > 0
    assert "Design is about THEM not us" in principles
    print("✓ test_design_thinking_principles passed")


async def test_design_thinking_missing_challenge():
    """Test design thinking with missing challenge."""
    agent = DesignThinkingCoach()
    request = DesignThinkingCoachRequest(challenge="")
    result = await agent.process(request)
    assert result["success"] == False
    assert "error" in result
    print("✓ test_design_thinking_missing_challenge passed")


async def main():
    """Run all tests."""
    print("Running Design Thinking Coach agent tests...\n")

    await test_design_thinking_full_process()
    await test_design_thinking_empathize_phase()
    await test_design_thinking_ideate_phase()
    await test_design_thinking_with_constraints()
    await test_design_thinking_process_structure()
    await test_design_thinking_activities()
    await test_design_thinking_facilitation()
    await test_design_thinking_principles()
    await test_design_thinking_missing_challenge()

    print("\n✅ All Design Thinking Coach tests passed!")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
