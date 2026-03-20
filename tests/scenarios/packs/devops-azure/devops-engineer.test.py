"""Scenario tests for DevOps Engineer Agent."""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))

from app.packs.devops_azure.agents.devops_engineer.agent import DevOpsEngineerAgent


def test_devops_engineer_basic_info():
    """Test that DevOps Engineer provides basic information."""
    agent = DevOpsEngineerAgent()
    result = agent.process("What is DevOps?")
    assert result is not None
    assert len(result) > 0
    assert (
        "DevOps" in result
        or "development" in result.lower()
        or "operations" in result.lower()
    )


def test_devops_engineer_ci_cd():
    """Test that DevOps Engineer can explain CI/CD."""
    agent = DevOpsEngineerAgent()
    result = agent.process("Explain CI/CD pipeline")
    assert result is not None
    assert len(result) > 0
    assert "CI" in result or "CD" in result or "pipeline" in result.lower()


def test_devops_engineer_docker():
    """Test that DevOps Engineer can discuss Docker."""
    agent = DevOpsEngineerAgent()
    result = agent.process("How do I create a Dockerfile?")
    assert result is not None
    assert len(result) > 0
    assert (
        "Docker" in result
        or "dockerfile" in result.lower()
        or "container" in result.lower()
    )


def test_devops_engineer_kubernetes():
    """Test that DevOps Engineer can discuss Kubernetes."""
    agent = DevOpsEngineerAgent()
    result = agent.process("What is Kubernetes?")
    assert result is not None
    assert len(result) > 0
    assert (
        "Kubernetes" in result
        or "k8s" in result.lower()
        or "orchestration" in result.lower()
    )


def test_devops_engineer_monitoring():
    """Test that DevOps Engineer can discuss monitoring."""
    agent = DevOpsEngineerAgent()
    result = agent.process("What monitoring tools do you recommend?")
    assert result is not None
    assert len(result) > 0
    assert (
        "monitor" in result.lower()
        or "prometheus" in result.lower()
        or "grafana" in result.lower()
    )


def test_devops_engineer_automation():
    """Test that DevOps Engineer can discuss automation."""
    agent = DevOpsEngineerAgent()
    result = agent.process("How can I automate deployments?")
    assert result is not None
    assert len(result) > 0
    assert (
        "automat" in result.lower()
        or "deploy" in result.lower()
        or "script" in result.lower()
    )


def test_devops_engineer_troubleshooting():
    """Test that DevOps Engineer can help with troubleshooting."""
    agent = DevOpsEngineerAgent()
    result = agent.process("My deployment is failing, what should I check?")
    assert result is not None
    assert len(result) > 0
    assert (
        "check" in result.lower()
        or "log" in result.lower()
        or "error" in result.lower()
        or "debug" in result.lower()
    )


if __name__ == "__main__":
    print("Running DevOps Engineer Agent Scenario Tests...")
    print()

    tests = [
        ("Basic Info", test_devops_engineer_basic_info),
        ("CI/CD", test_devops_engineer_ci_cd),
        ("Docker", test_devops_engineer_docker),
        ("Kubernetes", test_devops_engineer_kubernetes),
        ("Monitoring", test_devops_engineer_monitoring),
        ("Automation", test_devops_engineer_automation),
        ("Troubleshooting", test_devops_engineer_troubleshooting),
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
