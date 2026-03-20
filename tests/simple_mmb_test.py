"""Simple test script for all mmb module agents."""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

# Import agents directly from their modules
import importlib.util


def load_agent(module_path, class_name):
    """Load an agent class from a file path."""
    spec = importlib.util.spec_from_file_location("agent_module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)


# Load all agents
AgentBuilderAgent = load_agent(
    "app/mmb/agents/agent-builder/agent.py", "AgentBuilderAgent"
)
ModuleBuilderAgent = load_agent(
    "app/mmb/agents/module-builder/agent.py", "ModuleBuilderAgent"
)
WorkflowBuilderAgent = load_agent(
    "app/mmb/agents/workflow-builder/agent.py", "WorkflowBuilderAgent"
)


async def test_agent_builder():
    """Test Agent Builder agent."""
    print("Testing Agent Builder agent...")
    agent = AgentBuilderAgent()
    result = await agent.process("menu")
    assert result is not None
    assert len(result) > 0
    print("✓ Agent Builder agent works correctly\n")


async def test_module_builder():
    """Test Module Builder agent."""
    print("Testing Module Builder agent...")
    agent = ModuleBuilderAgent()
    result = await agent.process("menu")
    assert result is not None
    assert len(result) > 0
    print("✓ Module Builder agent works correctly\n")


async def test_workflow_builder():
    """Test Workflow Builder agent."""
    print("Testing Workflow Builder agent...")
    agent = WorkflowBuilderAgent()
    result = await agent.process("menu")
    assert result is not None
    assert len(result) > 0
    print("✓ Workflow Builder agent works correctly\n")


async def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing all mmb module agents")
    print("=" * 60)
    print()

    tests = [
        test_agent_builder,
        test_module_builder,
        test_workflow_builder,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            await test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}\n")
            import traceback

            traceback.print_exc()
            print()
            failed += 1

    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("\n🎉 All mmb module agents are working correctly!")
    else:
        print(f"\n⚠️  {failed} agent(s) failed the tests")


if __name__ == "__main__":
    asyncio.run(main())
