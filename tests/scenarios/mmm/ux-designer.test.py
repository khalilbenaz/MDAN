"""
Scenario tests for UX Designer Agent

Tests the UX Designer agent's ability to handle various UX design tasks
including user research, interaction design, and experience strategy.
"""

import sys
import os
import asyncio
import importlib.util

# Load the agent directly from file path (due to hyphen in directory name)
agent_path = os.path.join(
    os.path.dirname(__file__),
    "../../..",
    "app",
    "mmm",
    "agents",
    "ux-designer",
    "agent.py",
)
spec = importlib.util.spec_from_file_location("ux_designer_agent", agent_path)
ux_designer_module = importlib.util.module_from_spec(spec)
sys.modules["ux_designer_agent"] = ux_designer_module
spec.loader.exec_module(ux_designer_module)

UXDesigner = ux_designer_module.UXDesigner
UXDesignerRequest = ux_designer_module.UXDesignerRequest
UXDesignerResponse = ux_designer_module.UXDesignerResponse
UXDesignAction = ux_designer_module.UXDesignAction


async def test_scenario_1_redisplay_menu():
    """Test: User requests to see the menu"""
    agent = UXDesigner()
    request = UXDesignerRequest(action=UXDesignAction.REDISPLAY_MENU)

    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert response.action_taken == UXDesignAction.REDISPLAY_MENU
    assert "Menu" in response.content
    assert "MH" in response.content or "menu" in response.content.lower()
    print("✓ Scenario 1: Menu redisplay works correctly")


async def test_scenario_2_chat_basic():
    """Test: User wants to chat about UX design"""
    agent = UXDesigner()
    request = UXDesignerRequest(
        action=UXDesignAction.CHAT, user_input="I need help with a mobile app design"
    )

    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert response.action_taken == UXDesignAction.CHAT
    assert "Sally" in response.content or "empathetic" in response.content.lower()
    print("✓ Scenario 2: Basic chat works correctly")


async def test_scenario_3_create_ux_design_basic():
    """Test: User wants to create a UX design with basic context"""
    agent = UXDesigner()
    request = UXDesignerRequest(
        action=UXDesignAction.CREATE_UX_DESIGN,
        target_audience="young professionals",
        platform="mobile",
        user_stories=[
            "As a user, I want to quickly find nearby restaurants",
            "As a user, I want to see ratings and reviews",
        ],
    )

    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert response.action_taken == UXDesignAction.CREATE_UX_DESIGN
    assert "young professionals" in response.content
    assert "user flows" in response.content.lower()
    assert response.user_flows is not None
    assert len(response.user_flows) > 0
    assert response.recommendations is not None
    assert len(response.recommendations) > 0
    print("✓ Scenario 3: Basic UX design creation works correctly")


async def test_scenario_4_create_ux_design_with_project_context():
    """Test: User wants to create a UX design with detailed project context"""
    agent = UXDesigner()
    request = UXDesignerRequest(
        action=UXDesignAction.CREATE_UX_DESIGN,
        target_audience="enterprise developers",
        platform="web",
        project_context={
            "feature_name": "Code Review Dashboard",
            "goals": ["Improve review speed", "Increase code quality"],
            "constraints": ["Must support dark mode", "Accessible"],
        },
        user_stories=[
            "As a developer, I want to see pending reviews",
            "As a developer, I want to filter by repository",
        ],
    )

    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert response.action_taken == UXDesignAction.CREATE_UX_DESIGN
    assert "enterprise developers" in response.content
    assert "Code Review Dashboard" in response.content
    assert response.wireframes is not None
    assert len(response.wireframes) > 0
    assert response.next_steps is not None
    assert len(response.next_steps) > 0
    print("✓ Scenario 4: UX design with project context works correctly")


async def test_scenario_5_create_ux_design_web_platform():
    """Test: UX design creation for web platform"""
    agent = UXDesigner()
    request = UXDesignerRequest(
        action=UXDesignAction.CREATE_UX_DESIGN,
        platform="web",
        target_audience="online shoppers",
    )

    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert response.action_taken == UXDesignAction.CREATE_UX_DESIGN
    assert "online shoppers" in response.content
    assert response.wireframes is not None
    # Web platform should have standard wireframes
    assert any(wf["screen"] == "Landing/Home" for wf in response.wireframes)
    print("✓ Scenario 5: Web platform UX design works correctly")


async def test_scenario_6_create_ux_design_mobile_platform():
    """Test: UX design creation for mobile platform"""
    agent = UXDesigner()
    request = UXDesignerRequest(
        action=UXDesignAction.CREATE_UX_DESIGN,
        platform="mobile",
        target_audience="fitness enthusiasts",
    )

    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert response.action_taken == UXDesignAction.CREATE_UX_DESIGN
    assert "fitness enthusiasts" in response.content
    assert response.wireframes is not None
    # Mobile platform should have navigation wireframe
    assert any(wf["screen"] == "Navigation" for wf in response.wireframes)
    print("✓ Scenario 6: Mobile platform UX design works correctly")


async def test_scenario_7_party_mode():
    """Test: User activates party mode"""
    agent = UXDesigner()
    request = UXDesignerRequest(action=UXDesignAction.PARTY_MODE)

    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert response.action_taken == UXDesignAction.PARTY_MODE
    assert "PARTY MODE" in response.content or "party" in response.content.lower()
    assert "🎉" in response.content or "🎨" in response.content
    print("✓ Scenario 7: Party mode works correctly")


async def test_scenario_8_dismiss_agent():
    """Test: User dismisses the agent"""
    agent = UXDesigner()
    request = UXDesignerRequest(action=UXDesignAction.DISMISS)

    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert response.action_taken == UXDesignAction.DISMISS
    assert (
        "goodbye" in response.content.lower()
        or "dismiss" in response.content.lower()
        or "pleasure" in response.content.lower()
    )
    print("✓ Scenario 8: Agent dismissal works correctly")


async def test_scenario_9_user_flows_generation():
    """Test: User flows are generated correctly"""
    agent = UXDesigner()
    request = UXDesignerRequest(
        action=UXDesignAction.CREATE_UX_DESIGN,
        project_context={"feature_name": "User Profile Management"},
    )

    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert response.user_flows is not None
    assert len(response.user_flows) > 0

    # Check that flows have required structure
    for flow in response.user_flows:
        assert "name" in flow
        assert "steps" in flow
        assert "emotional_journey" in flow
        assert len(flow["steps"]) > 0

    print("✓ Scenario 9: User flows generation works correctly")


async def test_scenario_10_wireframe_recommendations():
    """Test: Wireframe recommendations are generated correctly"""
    agent = UXDesigner()
    request = UXDesignerRequest(action=UXDesignAction.CREATE_UX_DESIGN, platform="web")

    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert response.wireframes is not None
    assert len(response.wireframes) > 0

    # Check that wireframes have required structure
    for wf in response.wireframes:
        assert "screen" in wf
        assert "elements" in wf
        assert "priority" in wf
        assert len(wf["elements"]) > 0
        assert wf["priority"] in ["High", "Medium", "Low"]

    print("✓ Scenario 10: Wireframe recommendations work correctly")


async def test_scenario_11_design_principles_included():
    """Test: Design principles are included in response"""
    agent = UXDesigner()
    request = UXDesignerRequest(action=UXDesignAction.CREATE_UX_DESIGN)

    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert "user needs" in response.content.lower()
    assert "feedback" in response.content.lower()
    assert "empathy" in response.content.lower()
    print("✓ Scenario 11: Design principles are included correctly")


async def test_scenario_12_next_steps_provided():
    """Test: Next steps are provided in response"""
    agent = UXDesigner()
    request = UXDesignerRequest(action=UXDesignAction.CREATE_UX_DESIGN)

    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert response.next_steps is not None
    assert len(response.next_steps) > 0

    # Check that next steps are numbered
    for step in response.next_steps:
        assert step.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8."))

    print("✓ Scenario 12: Next steps are provided correctly")


async def run_all_scenarios():
    """Run all scenario tests"""
    print("\n" + "=" * 60)
    print("Running UX Designer Agent Scenario Tests")
    print("=" * 60 + "\n")

    await test_scenario_1_redisplay_menu()
    await test_scenario_2_chat_basic()
    await test_scenario_3_create_ux_design_basic()
    await test_scenario_4_create_ux_design_with_project_context()
    await test_scenario_5_create_ux_design_web_platform()
    await test_scenario_6_create_ux_design_mobile_platform()
    await test_scenario_7_party_mode()
    await test_scenario_8_dismiss_agent()
    await test_scenario_9_user_flows_generation()
    await test_scenario_10_wireframe_recommendations()
    await test_scenario_11_design_principles_included()
    await test_scenario_12_next_steps_provided()

    print("\n" + "=" * 60)
    print("✓ All 12 scenario tests passed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(run_all_scenarios())
