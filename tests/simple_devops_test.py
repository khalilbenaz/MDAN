"""Simple test script for DevOps/Azure Pack agents."""

import sys
import os
import asyncio
import importlib.util


def load_agent(module_path, class_name):
    """Load an agent class from a file path."""
    spec = importlib.util.spec_from_file_location("agent_module", module_path)
    if spec is None:
        raise ImportError(f"Could not load spec from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)


# Load agents
DevOpsEngineerAgent = load_agent(
    os.path.join(
        os.path.dirname(__file__),
        "../app/packs/devops-azure/agents/devops-engineer/agent.py",
    ),
    "DevOpsEngineerAgent",
)
AzureSpecialistAgent = load_agent(
    os.path.join(
        os.path.dirname(__file__),
        "../app/packs/devops-azure/agents/azure-specialist/agent.py",
    ),
    "AzureSpecialistAgent",
)
CICDArchitectAgent = load_agent(
    os.path.join(
        os.path.dirname(__file__),
        "../app/packs/devops-azure/agents/cicd-architect/agent.py",
    ),
    "CICDArchitectAgent",
)


async def test_devops_engineer():
    """Test DevOps Engineer Agent."""
    print("Testing DevOps Engineer Agent...")
    agent = DevOpsEngineerAgent()

    # Test get_info method
    info = agent.get_info()
    assert info is not None
    assert "name" in info
    assert info["name"] == "DevOps Engineer"
    assert "capabilities" in info
    assert len(info["capabilities"]) > 0

    # Test process method with a simple request
    from dataclasses import dataclass

    @dataclass
    class DevOpsRequest:
        action: str
        task: str = None
        context: dict = None
        tools: list = None

    request = DevOpsRequest(action="explain", task="CI/CD pipeline")

    result = await agent.process(request)
    assert result is not None
    assert len(result) > 0
    print("✓ DevOps Engineer agent test passed")
    return True


async def test_azure_specialist():
    """Test Azure Specialist Agent."""
    print("Testing Azure Specialist Agent...")
    agent = AzureSpecialistAgent()

    # Test get_info method
    info = agent.get_info()
    assert info is not None
    assert "name" in info
    assert info["name"] == "Azure Specialist"
    assert "capabilities" in info
    assert len(info["capabilities"]) > 0

    # Test process method with a simple request
    from dataclasses import dataclass

    @dataclass
    class AzureRequest:
        action: str
        service: str = None
        task: str = None
        context: dict = None

    request = AzureRequest(action="explain", service="Virtual Machines")

    result = await agent.process(request)
    assert result is not None
    assert len(result) > 0
    print("✓ Azure Specialist agent test passed")
    return True


async def test_cicd_architect():
    """Test CI/CD Architect Agent."""
    print("Testing CI/CD Architect Agent...")
    agent = CICDArchitectAgent()

    # Test get_info method
    info = agent.get_info()
    assert info is not None
    assert "name" in info
    assert info["name"] == "CI/CD Architect"
    assert "capabilities" in info
    assert len(info["capabilities"]) > 0

    # Test process method with a simple request
    from dataclasses import dataclass

    @dataclass
    class CICDRequest:
        action: str
        pipeline_type: str = None
        deployment_strategy: str = None
        tools: list = None
        environment: str = None

    request = CICDRequest(action="design", pipeline_type="application_deployment")

    result = await agent.process(request)
    assert result is not None
    assert len(result) > 0
    print("✓ CI/CD Architect agent test passed")
    return True


async def main():
    """Run all tests."""
    print("=" * 60)
    print("DevOps/Azure Pack - Simple Agent Tests")
    print("=" * 60)
    print()

    all_passed = True

    try:
        all_passed &= await test_devops_engineer()
    except Exception as e:
        print(f"✗ DevOps Engineer agent test failed: {e}")
        import traceback

        traceback.print_exc()
        all_passed = False

    print()

    try:
        all_passed &= await test_azure_specialist()
    except Exception as e:
        print(f"✗ Azure Specialist agent test failed: {e}")
        import traceback

        traceback.print_exc()
        all_passed = False

    print()

    try:
        all_passed &= await test_cicd_architect()
    except Exception as e:
        print(f"✗ CI/CD Architect agent test failed: {e}")
        import traceback

        traceback.print_exc()
        all_passed = False

    print()
    print("=" * 60)
    if all_passed:
        print("All DevOps/Azure Pack tests passed! ✓")
    else:
        print("Some tests failed! ✗")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    all_passed = asyncio.run(main())
    sys.exit(0 if all_passed else 1)
