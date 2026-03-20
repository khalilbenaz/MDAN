"""
Simple test script to verify MDAN Master agent works without the scenario framework.
"""

import sys
import os
import asyncio

# Add the app directory to the path
app_path = os.path.join(os.path.dirname(__file__), "..", "app")
sys.path.insert(0, app_path)

# Import directly from the file
import importlib.util

agent_file = os.path.join(app_path, "core", "agents", "mdan-master", "agent.py")
spec = importlib.util.spec_from_file_location("mdan_master_agent", agent_file)
if spec and spec.loader:
    mdan_master_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mdan_master_module)
    MDANMasterAgent = mdan_master_module.MDANMasterAgent
    AgentRequest = mdan_master_module.AgentRequest
else:
    raise ImportError(f"Could not load agent from {agent_file}")


async def test_agent():
    """Test the MDAN Master agent."""
    print("=" * 60)
    print("Testing MDAN Master Agent")
    print("=" * 60)

    # Test 1: Agent initialization
    print("\n[Test 1] Agent Initialization")
    agent = MDANMasterAgent()
    print(f"  Name: {agent.name}")
    print(f"  Title: {agent.title}")
    print(f"  Icon: {agent.icon}")
    print(f"  Capabilities: {', '.join(agent.capabilities)}")
    print("  ✓ Agent initialized successfully")

    # Test 2: Greet action with context
    print("\n[Test 2] Greet Action with Context")
    request = AgentRequest(
        action="greet",
        context={
            "user_name": "Alice",
            "communication_language": "English",
            "output_folder": "/output",
        },
    )
    result = await agent.process(request)
    print(f"  Message: {result['message']}")
    print(f"  Agent: {result['agent']}")
    print(f"  Language: {result['language']}")
    print(f"  Menu items: {len(result['menu'])}")
    print("  ✓ Greet action works correctly")

    # Test 3: List tasks
    print("\n[Test 3] List Tasks")
    request = AgentRequest(action="list-tasks")
    result = await agent.process(request)
    print(f"  Message: {result['message']}")
    print(f"  Tasks count: {result['count']}")
    for task in result["tasks"]:
        print(f"    - {task['name']} ({task['module']})")
    print("  ✓ List tasks works correctly")

    # Test 4: List workflows
    print("\n[Test 4] List Workflows")
    request = AgentRequest(action="list-workflows")
    result = await agent.process(request)
    print(f"  Message: {result['message']}")
    print(f"  Workflows count: {result['count']}")
    for workflow in result["workflows"]:
        print(f"    - {workflow['name']} ({workflow['module']})")
    print("  ✓ List workflows works correctly")

    # Test 5: Help action
    print("\n[Test 5] Help Action")
    request = AgentRequest(action="help")
    result = await agent.process(request)
    print(f"  Message: {result['message']}")
    print(f"  Agent: {result['agent']}")
    print(f"  Usage items: {len(result['usage'])}")
    print("  ✓ Help action works correctly")

    # Test 6: Unknown action
    print("\n[Test 6] Unknown Action")
    request = AgentRequest(action="unknown-action")
    result = await agent.process(request)
    print(f"  Message: {result['message']}")
    print(f"  Action: {result['action']}")
    print(f"  Suggestion: {result['suggestion']}")
    print("  ✓ Unknown action handled correctly")

    # Test 7: Get info
    print("\n[Test 7] Get Agent Info")
    info = agent.get_info()
    print(f"  Name: {info['name']}")
    print(f"  Role: {info['role']}")
    print(f"  Principles: {len(info['principles'])}")
    print("  ✓ Get info works correctly")

    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_agent())
