"""Simple test script for all mmm module agents."""

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
AnalystAgent = load_agent("app/mmm/agents/analyst/agent.py", "AnalystAgent")
ArchitectAgent = load_agent("app/mmm/agents/architect/agent.py", "ArchitectAgent")
DevAgent = load_agent("app/mmm/agents/dev/agent.py", "DevAgent")
PMAgent = load_agent("app/mmm/agents/pm/agent.py", "PMAgent")
QAAgent = load_agent("app/mmm/agents/qa/agent.py", "QAAgent")
QuickFlowSoloDevAgent = load_agent(
    "app/mmm/agents/quick-flow-solo-dev/agent.py", "QuickFlowSoloDevAgent"
)
SMAgent = load_agent("app/mmm/agents/sm/agent.py", "SMAgent")
TechWriterAgent = load_agent("app/mmm/agents/tech-writer/agent.py", "TechWriterAgent")


async def test_analyst():
    """Test Analyst agent."""
    print("Testing Analyst agent...")
    agent = AnalystAgent()
    result = await agent.process("Analyze requirements for a task management app")
    assert result is not None
    assert len(result) > 0
    print("✓ Analyst agent works correctly\n")


async def test_architect():
    """Test Architect agent."""
    print("Testing Architect agent...")
    agent = ArchitectAgent()
    result = await agent.process("Design architecture for a microservices app")
    assert result is not None
    assert len(result) > 0
    print("✓ Architect agent works correctly\n")


async def test_dev():
    """Test Dev agent."""
    print("Testing Dev agent...")
    agent = DevAgent()
    result = await agent.process("Implement a user authentication feature")
    assert result is not None
    assert len(result) > 0
    print("✓ Dev agent works correctly\n")


async def test_pm():
    """Test PM agent."""
    print("Testing PM agent...")
    agent = PMAgent()
    result = await agent.process("Create a project plan for a 6-month project")
    assert result is not None
    assert len(result) > 0
    print("✓ PM agent works correctly\n")


async def test_qa():
    """Test QA agent."""
    print("Testing QA agent...")
    agent = QAAgent()
    result = await agent.process("Create a test plan for an authentication system")
    assert result is not None
    assert len(result) > 0
    print("✓ QA agent works correctly\n")


async def test_quick_flow_solo_dev():
    """Test Quick Flow Solo Dev agent."""
    print("Testing Quick Flow Solo Dev agent...")
    agent = QuickFlowSoloDevAgent()
    result = await agent.process("Build a complete user authentication feature")
    assert result is not None
    assert len(result) > 0
    print("✓ Quick Flow Solo Dev agent works correctly\n")


async def test_sm():
    """Test Scrum Master agent."""
    print("Testing Scrum Master agent...")
    agent = SMAgent()
    result = await agent.process("Facilitate a sprint planning meeting")
    assert result is not None
    assert len(result) > 0
    print("✓ Scrum Master agent works correctly\n")


async def test_tech_writer():
    """Test Tech Writer agent."""
    print("Testing Tech Writer agent...")
    agent = TechWriterAgent()
    result = await agent.process("Create API documentation for a REST service")
    assert result is not None
    assert len(result) > 0
    print("✓ Tech Writer agent works correctly\n")


async def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing all mmm module agents")
    print("=" * 60)
    print()

    tests = [
        test_analyst,
        test_architect,
        test_dev,
        test_pm,
        test_qa,
        test_quick_flow_solo_dev,
        test_sm,
        test_tech_writer,
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
        print("\n🎉 All mmm module agents are working correctly!")
    else:
        print(f"\n⚠️  {failed} agent(s) failed the tests")


if __name__ == "__main__":
    asyncio.run(main())
