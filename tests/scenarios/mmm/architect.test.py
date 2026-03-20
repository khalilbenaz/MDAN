"""Scenario tests for the Architect agent."""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app"))

from mmm.agents.architect.agent import Architect


async def test_architect_system_design():
    """Test system design capability."""
    agent = Architect()

    result = await agent.process(
        "Design the system architecture for a microservices-based e-commerce platform"
    )

    assert result is not None
    assert len(result) > 0
    assert "architecture" in result.lower() or "design" in result.lower()
    print("✓ test_architect_system_design passed")


async def test_architect_component_design():
    """Test component design capability."""
    agent = Architect()

    result = await agent.process(
        "Design the components for a task management application with real-time updates"
    )

    assert result is not None
    assert len(result) > 0
    assert "component" in result.lower() or "module" in result.lower()
    print("✓ test_architect_component_design passed")


async def test_architect_technology_stack():
    """Test technology stack selection capability."""
    agent = Architect()

    result = await agent.process(
        "Recommend a technology stack for building a scalable real-time chat application"
    )

    assert result is not None
    assert len(result) > 0
    assert "technology" in result.lower() or "stack" in result.lower()
    print("✓ test_architect_technology_stack passed")


async def test_architect_api_design():
    """Test API design capability."""
    agent = Architect()

    result = await agent.process(
        "Design RESTful APIs for a user management system with authentication and authorization"
    )

    assert result is not None
    assert len(result) > 0
    assert "api" in result.lower() or "endpoint" in result.lower()
    print("✓ test_architect_api_design passed")


async def test_architect_database_design():
    """Test database design capability."""
    agent = Architect()

    result = await agent.process(
        "Design the database schema for a multi-tenant SaaS application"
    )

    assert result is not None
    assert len(result) > 0
    assert "database" in result.lower() or "schema" in result.lower()
    print("✓ test_architect_database_design passed")


async def test_architect_scalability():
    """Test scalability design capability."""
    agent = Architect()

    result = await agent.process(
        "Design a scalable architecture for a social media platform expecting millions of users"
    )

    assert result is not None
    assert len(result) > 0
    assert "scalable" in result.lower() or "scale" in result.lower()
    print("✓ test_architect_scalability passed")


async def test_architect_security():
    """Test security design capability."""
    agent = Architect()

    result = await agent.process(
        "Design security measures for a financial application handling sensitive data"
    )

    assert result is not None
    assert len(result) > 0
    assert "security" in result.lower() or "secure" in result.lower()
    print("✓ test_architect_security passed")


async def main():
    """Run all scenario tests."""
    print("Running Architect agent scenario tests...\n")

    tests = [
        test_architect_system_design,
        test_architect_component_design,
        test_architect_technology_stack,
        test_architect_api_design,
        test_architect_database_design,
        test_architect_scalability,
        test_architect_security,
    ]

    for test in tests:
        try:
            await test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            import traceback

            traceback.print_exc()

    print("\nAll Architect agent scenario tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
