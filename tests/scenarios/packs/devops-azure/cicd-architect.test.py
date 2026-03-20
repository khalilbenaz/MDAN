"""Scenario tests for CI/CD Architect Agent."""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))

from app.packs.devops_azure.agents.cicd_architect.agent import CICDArchitectAgent


def test_cicd_architect_basic_info():
    """Test that CI/CD Architect provides basic information."""
    agent = CICDArchitectAgent()
    result = agent.process("What is CI/CD architecture?")
    assert result is not None
    assert len(result) > 0
    assert "CI" in result or "CD" in result or "architecture" in result.lower()


def test_cicd_architect_github_actions():
    """Test that CI/CD Architect can discuss GitHub Actions."""
    agent = CICDArchitectAgent()
    result = agent.process("How do I set up GitHub Actions?")
    assert result is not None
    assert len(result) > 0
    assert "GitHub" in result or "Actions" in result or "workflow" in result.lower()


def test_cicd_architect_azure_devops():
    """Test that CI/CD Architect can discuss Azure DevOps."""
    agent = CICDArchitectAgent()
    result = agent.process("Explain Azure DevOps pipelines")
    assert result is not None
    assert len(result) > 0
    assert (
        "Azure DevOps" in result
        or "pipeline" in result.lower()
        or "build" in result.lower()
    )


def test_cicd_architect_jenkins():
    """Test that CI/CD Architect can discuss Jenkins."""
    agent = CICDArchitectAgent()
    result = agent.process("How do I configure Jenkins?")
    assert result is not None
    assert len(result) > 0
    assert (
        "Jenkins" in result or "pipeline" in result.lower() or "job" in result.lower()
    )


def test_cicd_architect_best_practices():
    """Test that CI/CD Architect can discuss best practices."""
    agent = CICDArchitectAgent()
    result = agent.process("What are CI/CD best practices?")
    assert result is not None
    assert len(result) > 0
    assert (
        "best practice" in result.lower()
        or "practice" in result.lower()
        or "recommend" in result.lower()
    )


def test_cicd_architect_testing():
    """Test that CI/CD Architect can discuss testing in CI/CD."""
    agent = CICDArchitectAgent()
    result = agent.process("How do I integrate automated testing?")
    assert result is not None
    assert len(result) > 0
    assert (
        "test" in result.lower()
        or "automated" in result.lower()
        or "unit" in result.lower()
    )


def test_cicd_architect_deployment_strategies():
    """Test that CI/CD Architect can discuss deployment strategies."""
    agent = CICDArchitectAgent()
    result = agent.process("What deployment strategies should I use?")
    assert result is not None
    assert len(result) > 0
    assert (
        "deploy" in result.lower()
        or "strategy" in result.lower()
        or "blue" in result.lower()
        or "canary" in result.lower()
    )


if __name__ == "__main__":
    print("Running CI/CD Architect Agent Scenario Tests...")
    print()

    tests = [
        ("Basic Info", test_cicd_architect_basic_info),
        ("GitHub Actions", test_cicd_architect_github_actions),
        ("Azure DevOps", test_cicd_architect_azure_devops),
        ("Jenkins", test_cicd_architect_jenkins),
        ("Best Practices", test_cicd_architect_best_practices),
        ("Testing", test_cicd_architect_testing),
        ("Deployment Strategies", test_cicd_architect_deployment_strategies),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            print(f"✓ {name}")
            passed += 1
        except Exception as e:
            print(f"✗ {name}: {e}")
            failed += 1

    print()
    print(f"Results: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
