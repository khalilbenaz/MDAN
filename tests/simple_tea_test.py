"""
Simple integration test for tea module agent
Tests that the TEA agent can be imported and instantiated correctly
"""

import asyncio
import sys
import os
import importlib.util

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


async def test_tea_agent():
    """Test TEA Agent"""
    print("Testing TEA Agent (Murat)...")

    try:
        agent_path = os.path.join(
            os.path.dirname(__file__), "../app/tea/agents/tea/agent.py"
        )
        module = importlib.util.spec_from_file_location("agent_module", agent_path)
        if module is None or module.loader is None:
            raise ImportError(f"Could not load spec from {agent_path}")
        agent_module = importlib.util.module_from_spec(module)
        module.loader.exec_module(agent_module)

        TEA = agent_module.TEA
        TEARequest = agent_module.TEARequest

        agent = TEA()

        # Test basic processing
        request = TEARequest(task="teach-me-testing", context="I want to learn testing")
        result = await agent.process(request)

        assert result is not None
        assert isinstance(result, dict)
        assert result["success"] == True
        print("✓ TEA Agent works correctly")
        return True
    except Exception as e:
        print(f"✗ TEA Agent failed: {e}")
        import traceback

        traceback.print_exc()
        return False


async def run_all_tests():
    """Run all tea module agent tests"""
    print("=" * 60)
    print("TEA Module - Integration Tests")
    print("=" * 60)

    tests = [
        test_tea_agent(),
    ]

    results = await asyncio.gather(*tests)

    passed = sum(results)
    total = len(results)

    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} agents passed")
    print("=" * 60)

    if passed == total:
        print("✓ All TEA agents work correctly!")
        return 0
    else:
        print(f"✗ {total - passed} agent(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
