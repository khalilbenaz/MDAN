"""Scenario tests for the Agent Builder agent."""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app"))

from mmb.agents.agent_builder.agent import AgentBuilderAgent


async def test_agent_builder_menu_display():
    """Test menu display capability."""
    agent = AgentBuilderAgent()

    result = await agent.process("menu")

    assert result is not None
    assert len(result) > 0
    assert "menu" in result.lower() or "agent builder" in result.lower()
    print("✓ test_agent_builder_menu_display passed")


async def test_agent_builder_create_agent():
    """Test create agent capability."""
    agent = AgentBuilderAgent()

    result = await agent.process("create-agent")

    assert result is not None
    assert len(result) > 0
    assert "create" in result.lower() or "agent" in result.lower()
    print("✓ test_agent_builder_create_agent passed")


async def test_agent_builder_edit_agent():
    """Test edit agent capability."""
    agent = AgentBuilderAgent()

    result = await agent.process("edit-agent")

    assert result is not None
    assert len(result) > 0
    assert "edit" in result.lower() or "agent" in result.lower()
    print("✓ test_agent_builder_edit_agent passed")


async def test_agent_builder_validate_agent():
    """Test validate agent capability."""
    agent = AgentBuilderAgent()

    result = await agent.process("validate-agent")

    assert result is not None
    assert len(result) > 0
    assert "validate" in result.lower() or "compliance" in result.lower()
    print("✓ test_agent_builder_validate_agent passed")


async def test_agent_builder_chat():
    """Test chat capability."""
    agent = AgentBuilderAgent()

    result = await agent.process("chat")

    assert result is not None
    assert len(result) > 0
    assert "agent" in result.lower() or "building" in result.lower()
    print("✓ test_agent_builder_chat passed")


async def test_agent_builder_fuzzy_match():
    """Test fuzzy matching capability."""
    agent = AgentBuilderAgent()

    result = await agent.process("I want to create a new agent")

    assert result is not None
    assert len(result) > 0
    assert "create" in result.lower() or "agent" in result.lower()
    print("✓ test_agent_builder_fuzzy_match passed")


async def test_agent_builder_dismiss():
    """Test dismiss capability."""
    agent = AgentBuilderAgent()

    result = await agent.process("dismiss")

    assert result is not None
    assert len(result) > 0
    assert "goodbye" in result.lower() or "dismiss" in result.lower()
    print("✓ test_agent_builder_dismiss passed")


async def main():
    """Run all scenario tests."""
    print("Running Agent Builder agent scenario tests...\n")

    tests = [
        test_agent_builder_menu_display,
        test_agent_builder_create_agent,
        test_agent_builder_edit_agent,
        test_agent_builder_validate_agent,
        test_agent_builder_chat,
        test_agent_builder_fuzzy_match,
        test_agent_builder_dismiss,
    ]

    for test in tests:
        try:
            await test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            import traceback

            traceback.print_exc()

    print("\nAll Agent Builder agent scenario tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
