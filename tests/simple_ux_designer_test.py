"""
Simple integration test for UX Designer Agent

This test verifies that the UX Designer agent can be imported and used correctly.
"""

import sys
import os
import asyncio
import importlib.util

# Load the agent directly from file path (due to hyphen in directory name)
agent_path = os.path.join(
    os.path.dirname(__file__), "..", "app", "mmm", "agents", "ux-designer", "agent.py"
)
spec = importlib.util.spec_from_file_location("ux_designer_agent", agent_path)
ux_designer_module = importlib.util.module_from_spec(spec)
sys.modules["ux_designer_agent"] = ux_designer_module
spec.loader.exec_module(ux_designer_module)

UXDesigner = ux_designer_module.UXDesigner
UXDesignerRequest = ux_designer_module.UXDesignerRequest
UXDesignerResponse = ux_designer_module.UXDesignerResponse
UXDesignAction = ux_designer_module.UXDesignAction


def test_agent_creation():
    """Test that the agent can be created"""
    agent = UXDesigner()
    assert agent.name == "Sally"
    assert agent.title == "UX Designer"
    assert agent.icon == "🎨"
    assert len(agent.capabilities) > 0
    print("✓ Agent creation works")


def test_menu_retrieval():
    """Test that the menu can be retrieved"""
    agent = UXDesigner()
    menu = agent.get_menu()
    assert isinstance(menu, list)
    assert len(menu) > 0
    assert all("cmd" in item and "label" in item for item in menu)
    print("✓ Menu retrieval works")


async def test_redisplay_menu():
    """Test redisplay menu action"""
    agent = UXDesigner()
    request = UXDesignerRequest(action=UXDesignAction.REDISPLAY_MENU)
    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert response.action_taken == UXDesignAction.REDISPLAY_MENU
    assert "Menu" in response.content
    print("✓ Redisplay menu works")


async def test_chat():
    """Test chat action"""
    agent = UXDesigner()
    request = UXDesignerRequest(
        action=UXDesignAction.CHAT, user_input="I need help with UX design"
    )
    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert response.action_taken == UXDesignAction.CHAT
    assert len(response.content) > 0
    print("✓ Chat works")


async def test_create_ux_design():
    """Test create UX design action"""
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
    assert response.user_flows is not None
    assert len(response.user_flows) > 0
    assert response.wireframes is not None
    assert len(response.wireframes) > 0
    assert response.recommendations is not None
    assert len(response.recommendations) > 0
    assert response.next_steps is not None
    assert len(response.next_steps) > 0
    print("✓ Create UX design works")


async def test_party_mode():
    """Test party mode action"""
    agent = UXDesigner()
    request = UXDesignerRequest(action=UXDesignAction.PARTY_MODE)
    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert response.action_taken == UXDesignAction.PARTY_MODE
    assert "party" in response.content.lower() or "PARTY" in response.content
    print("✓ Party mode works")


async def test_dismiss():
    """Test dismiss action"""
    agent = UXDesigner()
    request = UXDesignerRequest(action=UXDesignAction.DISMISS)
    response = await agent.process(request)

    assert isinstance(response, UXDesignerResponse)
    assert response.action_taken == UXDesignAction.DISMISS
    assert len(response.content) > 0
    print("✓ Dismiss works")


async def run_all_tests():
    """Run all integration tests"""
    print("\\n" + "=" * 60)
    print("UX Designer Agent - Integration Tests")
    print("=" * 60 + "\\n")

    test_agent_creation()
    test_menu_retrieval()
    await test_redisplay_menu()
    await test_chat()
    await test_create_ux_design()
    await test_party_mode()
    await test_dismiss()

    print("\\n" + "=" * 60)
    print("✓ All 7 integration tests passed!")
    print("=" * 60 + "\\n")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
