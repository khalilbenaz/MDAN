"""Scenario tests for the QA agent."""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app"))

from mmm.agents.qa.agent import QA


async def test_qa_test_plan_creation():
    """Test test plan creation capability."""
    agent = QA()

    result = await agent.process(
        "Create a comprehensive test plan for a user authentication system"
    )

    assert result is not None
    assert len(result) > 0
    assert "test plan" in result.lower() or "testing" in result.lower()
    print("✓ test_qa_test_plan_creation passed")


async def test_qa_test_case_design():
    """Test test case design capability."""
    agent = QA()

    result = await agent.process(
        "Design test cases for a shopping cart feature with various edge cases"
    )

    assert result is not None
    assert len(result) > 0
    assert "test case" in result.lower() or "scenario" in result.lower()
    print("✓ test_qa_test_case_design passed")


async def test_qa_automated_testing():
    """Test automated testing capability."""
    agent = QA()

    result = await agent.process(
        "Create automated tests for a REST API using Cypress or Playwright"
    )

    assert result is not None
    assert len(result) > 0
    assert "automated" in result.lower() or "automation" in result.lower()
    print("✓ test_qa_automated_testing passed")


async def test_qa_bug_reporting():
    """Test bug reporting capability."""
    agent = QA()

    result = await agent.process(
        "Report a bug found during testing with detailed steps to reproduce"
    )

    assert result is not None
    assert len(result) > 0
    assert "bug" in result.lower() or "issue" in result.lower()
    print("✓ test_qa_bug_reporting passed")


async def test_qa_regression_testing():
    """Test regression testing capability."""
    agent = QA()

    result = await agent.process(
        "Design a regression testing strategy for a major application update"
    )

    assert result is not None
    assert len(result) > 0
    assert "regression" in result.lower() or "regress" in result.lower()
    print("✓ test_qa_regression_testing passed")


async def test_qa_performance_testing():
    """Test performance testing capability."""
    agent = QA()

    result = await agent.process(
        "Design performance tests for a high-traffic e-commerce website"
    )

    assert result is not None
    assert len(result) > 0
    assert "performance" in result.lower() or "load" in result.lower()
    print("✓ test_qa_performance_testing passed")


async def test_qa_security_testing():
    """Test security testing capability."""
    agent = QA()

    result = await agent.process(
        "Design security tests for a financial application handling sensitive data"
    )

    assert result is not None
    assert len(result) > 0
    assert "security" in result.lower() or "vulnerability" in result.lower()
    print("✓ test_qa_security_testing passed")


async def main():
    """Run all scenario tests."""
    print("Running QA agent scenario tests...\n")

    tests = [
        test_qa_test_plan_creation,
        test_qa_test_case_design,
        test_qa_automated_testing,
        test_qa_bug_reporting,
        test_qa_regression_testing,
        test_qa_performance_testing,
        test_qa_security_testing,
    ]

    for test in tests:
        try:
            await test()
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            import traceback

            traceback.print_exc()

    print("\nAll QA agent scenario tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
