"""
Scenario tests for Brainstorming Coach agent
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from app.cis.agents.brainstorming_coach import (
    BrainstormingCoach,
    BrainstormingCoachRequest,
)


async def test_brainstorming_basic():
    """Test basic brainstorming session."""
    agent = BrainstormingCoach()
    request = BrainstormingCoachRequest(
        topic="New product ideas for a coffee shop", session_type="standard"
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["agent"] == "Carson"
    assert result["topic"] == "New product ideas for a coffee shop"
    assert "session_plan" in result
    assert "techniques" in result
    assert len(result["techniques"]) > 0
    print("✓ test_brainstorming_basic passed")


async def test_brainstorming_party_mode():
    """Test brainstorming with party mode."""
    agent = BrainstormingCoach()
    request = BrainstormingCoachRequest(
        topic="Team building activities", session_type="party-mode", participants=10
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["session_type"] == "party-mode"
    assert result["participants"] == 10
    # Check that party mode warm-up is included
    assert any("Party Mode" in t["name"] for t in result["techniques"])
    print("✓ test_brainstorming_party_mode passed")


async def test_brainstorming_with_constraints():
    """Test brainstorming with constraints."""
    agent = BrainstormingCoach()
    request = BrainstormingCoachRequest(
        topic="Marketing campaign ideas",
        session_type="standard",
        constraints="Budget under $5000, 2-week timeline",
        goals="Increase brand awareness",
    )
    result = await agent.process(request)
    assert result["success"] == True
    assert result["constraints"] == "Budget under $5000, 2-week timeline"
    assert result["goals"] == "Increase brand awareness"
    print("✓ test_brainstorming_with_constraints passed")


async def test_brainstorming_session_plan():
    """Test that session plan is generated correctly."""
    agent = BrainstormingCoach()
    request = BrainstormingCoachRequest(topic="App feature ideas")
    result = await agent.process(request)
    assert result["success"] == True
    session_plan = result["session_plan"]
    assert "warm_up" in session_plan
    assert "ideation_phase" in session_plan
    assert "expansion_phase" in session_plan
    assert "convergence_phase" in session_plan
    assert "action_planning" in session_plan
    print("✓ test_brainstorming_session_plan passed")


async def test_brainstorming_techniques():
    """Test that brainstorming techniques are provided."""
    agent = BrainstormingCoach()
    request = BrainstormingCoachRequest(topic="Innovation ideas")
    result = await agent.process(request)
    assert result["success"] == True
    techniques = result["techniques"]
    assert len(techniques) >= 5
    # Check for known techniques
    technique_names = [t["name"] for t in techniques]
    assert "Classic Brainstorming" in technique_names
    assert "Mind Mapping" in technique_names
    print("✓ test_brainstorming_techniques passed")


async def test_brainstorming_facilitation_guide():
    """Test that facilitation guide is provided."""
    agent = BrainstormingCoach()
    request = BrainstormingCoachRequest(topic="Team improvement ideas")
    result = await agent.process(request)
    assert result["success"] == True
    guide = result["facilitation_guide"]
    assert "opening" in guide
    assert "ground_rules" in guide
    assert "prompts" in guide
    assert "closing" in guide
    assert len(guide["ground_rules"]) > 0
    assert len(guide["prompts"]) > 0
    print("✓ test_brainstorming_facilitation_guide passed")


async def test_brainstorming_principles():
    """Test that brainstorming principles are included."""
    agent = BrainstormingCoach()
    request = BrainstormingCoachRequest(topic="Creative ideas")
    result = await agent.process(request)
    assert result["success"] == True
    principles = result["principles"]
    assert len(principles) > 0
    assert "Psychological safety unlocks breakthroughs" in principles
    print("✓ test_brainstorming_principles passed")


async def test_brainstorming_missing_topic():
    """Test brainstorming with missing topic."""
    agent = BrainstormingCoach()
    request = BrainstormingCoachRequest(topic="")
    result = await agent.process(request)
    assert result["success"] == False
    assert "error" in result
    print("✓ test_brainstorming_missing_topic passed")


async def main():
    """Run all tests."""
    print("Running Brainstorming Coach agent tests...\n")

    await test_brainstorming_basic()
    await test_brainstorming_party_mode()
    await test_brainstorming_with_constraints()
    await test_brainstorming_session_plan()
    await test_brainstorming_techniques()
    await test_brainstorming_facilitation_guide()
    await test_brainstorming_principles()
    await test_brainstorming_missing_topic()

    print("\n✅ All Brainstorming Coach tests passed!")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
