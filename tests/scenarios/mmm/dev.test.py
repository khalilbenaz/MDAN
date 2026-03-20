"""Scenario tests for the Dev agent."""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app"))

from mmm.agents.dev.agent import Dev


async def test_dev_feature_implementation():
    """Test feature implementation capability."""
    agent = Dev()

    result = await agent.process(
        "Implement a user authentication feature with login and registration"
    )

    assert result is not None
    assert len(result) > 0
    assert "implement" in result.lower() or "code" in result.lower()
    print("✓ test_dev_feature_implementation passed")


async def test_dev_bug_fixing():
    """Test bug fixing capability."""
    agent = Dev()

    result = await agent.process(
        "Fix a bug where the application crashes when uploading large files"
    )

    assert result is not None
    assert len(result) > 0
    assert "fix" in result.lower() or "bug" in result.lower()
    print("✓ test_dev_bug_fixing passed")


async def test_dev_code_refactoring():
    """Test code refactoring capability."""
    agent = Dev()

    result = await agent.process(
        "Refactor a monolithic user service into smaller, more maintainable modules"
    )

    assert result is not None
    assert len(result) > 0
    assert "refactor" in result.lower() or "improve" in result.lower()
    print("✓ test_dev_code_refactoring passed")


async def test_dev_api_development():
    """Test API development capability."""
    agent = Dev()

    result = await agent.process(
        "Develop RESTful API endpoints for managing products in an e-commerce system"
    )

    assert result is not None
    assert len(result) > 0
    assert "api" in result.lower() or "endpoint" in result.lower()
    print("✓ test_dev_api_development passed")


async def test_dev_database_integration():
    """Test database integration capability."""
    agent = Dev()

    result = await agent.process(
        "Integrate PostgreSQL database with a Node.js application using Prisma ORM"
    )

    assert result is not None
    assert len(result) > 0
    assert "database" in result.lower() or "integration" in result.lower()
    print("✓ test_dev_database_integration passed")


async def test_dev_testing():
    """Test testing capability."""
    agent = Dev()

    result = await agent.process(
        "Write unit tests for a user service with authentication and authorization"
    )

    assert result is not None
    assert len(result) > 0
    assert "test" in result.lower() or "testing" in result.lower()
    print("✓ test_dev_testing passed")


async def test_dev_code_review():
    """Test code review capability."""
    agent = Dev()

    result = await agent.process(
        "Review a pull request for a new feature and provide feedback on code quality and best practices"
    )

    assert result is not None
    assert len(result) > 0
    assert "review" in result.lower() or "feedback" in result.lower()
    print("✓ test_dev_code_review passed")


async def main():
    """Run all scenario tests."""
    print("Running Dev agent scenario tests...\n")

    tests = [
        test_dev_feature_implementation,
        test_dev_bug_fixing,
        test_dev_code_refactoring,
        test_dev_api_development,
        test_dev_database_integration,
        test_dev_testing,
        test_dev_code_review,
    ]

    for test in tests:
        try:
            await test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            import traceback

            traceback.print_exc()

    print("\nAll Dev agent scenario tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
