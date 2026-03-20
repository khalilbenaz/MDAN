"""Scenario tests for the Tech Writer agent."""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app"))

from mmm.agents.tech_writer.agent import TechWriter


async def test_tech_writer_api_documentation():
    """Test API documentation capability."""
    agent = TechWriter()

    result = await agent.process(
        "Create comprehensive API documentation for a RESTful user management service"
    )

    assert result is not None
    assert len(result) > 0
    assert "api" in result.lower() or "documentation" in result.lower()
    print("✓ test_tech_writer_api_documentation passed")


async def test_tech_writer_user_guide():
    """Test user guide creation capability."""
    agent = TechWriter()

    result = await agent.process(
        "Create a user guide for a project management application with step-by-step instructions"
    )

    assert result is not None
    assert len(result) > 0
    assert "user guide" in result.lower() or "tutorial" in result.lower()
    print("✓ test_tech_writer_user_guide passed")


async def test_tech_writer_readme():
    """Test README creation capability."""
    agent = TechWriter()

    result = await agent.process(
        "Create a comprehensive README for an open-source project with installation and usage instructions"
    )

    assert result is not None
    assert len(result) > 0
    assert "readme" in result.lower() or "getting started" in result.lower()
    print("✓ test_tech_writer_readme passed")


async def test_tech_writer_code_documentation():
    """Test code documentation capability."""
    agent = TechWriter()

    result = await agent.process(
        "Document a complex authentication module with inline comments and docstrings"
    )

    assert result is not None
    assert len(result) > 0
    assert "document" in result.lower() or "comment" in result.lower()
    print("✓ test_tech_writer_code_documentation passed")


async def test_tech_writer_architecture_docs():
    """Test architecture documentation capability."""
    agent = TechWriter()

    result = await agent.process(
        "Create architecture documentation for a microservices-based e-commerce platform"
    )

    assert result is not None
    assert len(result) > 0
    assert "architecture" in result.lower() or "design" in result.lower()
    print("✓ test_tech_writer_architecture_docs passed")


async def test_tech_writer_troubleshooting_guide():
    """Test troubleshooting guide creation capability."""
    agent = TechWriter()

    result = await agent.process(
        "Create a troubleshooting guide for common issues in a web application"
    )

    assert result is not None
    assert len(result) > 0
    assert "troubleshoot" in result.lower() or "issue" in result.lower()
    print("✓ test_tech_writer_troubleshooting_guide passed")


async def test_tech_writer_release_notes():
    """Test release notes creation capability."""
    agent = TechWriter()

    result = await agent.process(
        "Create release notes for version 2.0 of a software product with new features and bug fixes"
    )

    assert result is not None
    assert len(result) > 0
    assert "release" in result.lower() or "changelog" in result.lower()
    print("✓ test_tech_writer_release_notes passed")


async def main():
    """Run all scenario tests."""
    print("Running Tech Writer agent scenario tests...\n")

    tests = [
        test_tech_writer_api_documentation,
        test_tech_writer_user_guide,
        test_tech_writer_readme,
        test_tech_writer_code_documentation,
        test_tech_writer_architecture_docs,
        test_tech_writer_troubleshooting_guide,
        test_tech_writer_release_notes,
    ]

    for test in tests:
        try:
            await test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            import traceback

            traceback.print_exc()

    print("\nAll Tech Writer agent scenario tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
