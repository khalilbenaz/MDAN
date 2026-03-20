"""Scenario tests for the Module Builder agent."""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app"))

from mmb.agents.module_builder.agent import ModuleBuilderAgent


async def test_module_builder_menu_display():
    """Test menu display capability."""
    agent = ModuleBuilderAgent()

    result = await agent.process("menu")

    assert result is not None
    assert len(result) > 0
    assert "menu" in result.lower() or "module builder" in result.lower()
    print("✓ test_module_builder_menu_display passed")


async def test_module_builder_product_brief():
    """Test product brief creation capability."""
    agent = ModuleBuilderAgent()

    result = await agent.process("product-brief")

    assert result is not None
    assert len(result) > 0
    assert "product brief" in result.lower() or "module" in result.lower()
    print("✓ test_module_builder_product_brief passed")


async def test_module_builder_create_module():
    """Test create module capability."""
    agent = ModuleBuilderAgent()

    result = await agent.process("create-module")

    assert result is not None
    assert len(result) > 0
    assert "create" in result.lower() or "module" in result.lower()
    print("✓ test_module_builder_create_module passed")


async def test_module_builder_edit_module():
    """Test edit module capability."""
    agent = ModuleBuilderAgent()

    result = await agent.process("edit-module")

    assert result is not None
    assert len(result) > 0
    assert "edit" in result.lower() or "module" in result.lower()
    print("✓ test_module_builder_edit_module passed")


async def test_module_builder_validate_module():
    """Test validate module capability."""
    agent = ModuleBuilderAgent()

    result = await agent.process("validate-module")

    assert result is not None
    assert len(result) > 0
    assert "validate" in result.lower() or "compliance" in result.lower()
    print("✓ test_module_builder_validate_module passed")


async def test_module_builder_chat():
    """Test chat capability."""
    agent = ModuleBuilderAgent()

    result = await agent.process("chat")

    assert result is not None
    assert len(result) > 0
    assert "module" in result.lower() or "building" in result.lower()
    print("✓ test_module_builder_chat passed")


async def test_module_builder_fuzzy_match():
    """Test fuzzy matching capability."""
    agent = ModuleBuilderAgent()

    result = await agent.process("I want to create a new module")

    assert result is not None
    assert len(result) > 0
    assert "create" in result.lower() or "module" in result.lower()
    print("✓ test_module_builder_fuzzy_match passed")


async def main():
    """Run all scenario tests."""
    print("Running Module Builder agent scenario tests...\n")

    tests = [
        test_module_builder_menu_display,
        test_module_builder_product_brief,
        test_module_builder_create_module,
        test_module_builder_edit_module,
        test_module_builder_validate_module,
        test_module_builder_chat,
        test_module_builder_fuzzy_match,
    ]

    for test in tests:
        try:
            await test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            import traceback

            traceback.print_exc()

    print("\nAll Module Builder agent scenario tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
