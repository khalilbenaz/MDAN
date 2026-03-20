"""Scenario tests for the Workflow Builder agent."""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app"))

from mmb.agents.workflow_builder.agent import WorkflowBuilderAgent


async def test_workflow_builder_menu_display():
    """Test menu display capability."""
    agent = WorkflowBuilderAgent()

    result = await agent.process("menu")

    assert result is not None
    assert len(result) > 0
    assert "menu" in result.lower() or "workflow builder" in result.lower()
    print("✓ test_workflow_builder_menu_display passed")


async def test_workflow_builder_create_workflow():
    """Test create workflow capability."""
    agent = WorkflowBuilderAgent()

    result = await agent.process("create-workflow")

    assert result is not None
    assert len(result) > 0
    assert "create" in result.lower() or "workflow" in result.lower()
    print("✓ test_workflow_builder_create_workflow passed")


async def test_workflow_builder_edit_workflow():
    """Test edit workflow capability."""
    agent = WorkflowBuilderAgent()

    result = await agent.process("edit-workflow")

    assert result is not None
    assert len(result) > 0
    assert "edit" in result.lower() or "workflow" in result.lower()
    print("✓ test_workflow_builder_edit_workflow passed")


async def test_workflow_builder_validate_workflow():
    """Test validate workflow capability."""
    agent = WorkflowBuilderAgent()

    result = await agent.process("validate-workflow")

    assert result is not None
    assert len(result) > 0
    assert "validate" in result.lower() or "workflow" in result.lower()
    print("✓ test_workflow_builder_validate_workflow passed")


async def test_workflow_builder_max_parallel():
    """Test max-parallel validation capability."""
    agent = WorkflowBuilderAgent()

    result = await agent.process("validate-max-parallel-workflow")

    assert result is not None
    assert len(result) > 0
    assert "parallel" in result.lower() or "validation" in result.lower()
    print("✓ test_workflow_builder_max_parallel passed")


async def test_workflow_builder_rework_workflow():
    """Test rework workflow capability."""
    agent = WorkflowBuilderAgent()

    result = await agent.process("rework-workflow")

    assert result is not None
    assert len(result) > 0
    assert "rework" in result.lower() or "v6" in result.lower()
    print("✓ test_workflow_builder_rework_workflow passed")


async def test_workflow_builder_chat():
    """Test chat capability."""
    agent = WorkflowBuilderAgent()

    result = await agent.process("chat")

    assert result is not None
    assert len(result) > 0
    assert "workflow" in result.lower() or "building" in result.lower()
    print("✓ test_workflow_builder_chat passed")


async def main():
    """Run all scenario tests."""
    print("Running Workflow Builder agent scenario tests...\n")

    tests = [
        test_workflow_builder_menu_display,
        test_workflow_builder_create_workflow,
        test_workflow_builder_edit_workflow,
        test_workflow_builder_validate_workflow,
        test_workflow_builder_max_parallel,
        test_workflow_builder_rework_workflow,
        test_workflow_builder_chat,
    ]

    for test in tests:
        try:
            await test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            import traceback

            traceback.print_exc()

    print("\nAll Workflow Builder agent scenario tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
