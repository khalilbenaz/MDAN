"""Scenario tests for Azure Specialist Agent."""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))

from app.packs.devops_azure.agents.azure_specialist.agent import AzureSpecialistAgent


def test_azure_specialist_basic_info():
    """Test that Azure Specialist provides basic information."""
    agent = AzureSpecialistAgent()
    result = agent.process("What is Microsoft Azure?")
    assert result is not None
    assert len(result) > 0
    assert "Azure" in result or "Microsoft" in result or "cloud" in result.lower()


def test_azure_specialist_vm():
    """Test that Azure Specialist can discuss Virtual Machines."""
    agent = AzureSpecialistAgent()
    result = agent.process("How do I create an Azure VM?")
    assert result is not None
    assert len(result) > 0
    assert "VM" in result or "virtual machine" in result.lower() or "Azure" in result


def test_azure_specialist_storage():
    """Test that Azure Specialist can discuss Azure Storage."""
    agent = AzureSpecialistAgent()
    result = agent.process("What storage options does Azure offer?")
    assert result is not None
    assert len(result) > 0
    assert (
        "storage" in result.lower()
        or "blob" in result.lower()
        or "disk" in result.lower()
    )


def test_azure_specialist_functions():
    """Test that Azure Specialist can discuss Azure Functions."""
    agent = AzureSpecialistAgent()
    result = agent.process("What are Azure Functions?")
    assert result is not None
    assert len(result) > 0
    assert (
        "Function" in result
        or "serverless" in result.lower()
        or "compute" in result.lower()
    )


def test_azure_specialist_cosmos_db():
    """Test that Azure Specialist can discuss Cosmos DB."""
    agent = AzureSpecialistAgent()
    result = agent.process("Tell me about Azure Cosmos DB")
    assert result is not None
    assert len(result) > 0
    assert (
        "Cosmos" in result
        or "database" in result.lower()
        or "NoSQL" in result
        or "SQL" in result
    )


def test_azure_specialist_networking():
    """Test that Azure Specialist can discuss Azure Networking."""
    agent = AzureSpecialistAgent()
    result = agent.process("How do I set up a VNet in Azure?")
    assert result is not None
    assert len(result) > 0
    assert (
        "VNet" in result
        or "virtual network" in result.lower()
        or "network" in result.lower()
    )


def test_azure_specialist_security():
    """Test that Azure Specialist can discuss Azure Security."""
    agent = AzureSpecialistAgent()
    result = agent.process("What security features does Azure provide?")
    assert result is not None
    assert len(result) > 0
    assert (
        "security" in result.lower()
        or "IAM" in result
        or "RBAC" in result
        or "firewall" in result.lower()
    )


if __name__ == "__main__":
    print("Running Azure Specialist Agent Scenario Tests...")
    print()

    tests = [
        ("Basic Info", test_azure_specialist_basic_info),
        ("Virtual Machines", test_azure_specialist_vm),
        ("Storage", test_azure_specialist_storage),
        ("Azure Functions", test_azure_specialist_functions),
        ("Cosmos DB", test_azure_specialist_cosmos_db),
        ("Networking", test_azure_specialist_networking),
        ("Security", test_azure_specialist_security),
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
