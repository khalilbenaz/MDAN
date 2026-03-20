"""Scenario tests for Compliance Officer agent."""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from app.packs.fintech.agents.compliance_officer.agent import ComplianceOfficer


def test_regulatory_assessment():
    """Test regulatory compliance assessment capability."""
    agent = ComplianceOfficer()

    input_data = {
        "task": "Assess regulatory compliance requirements",
        "jurisdiction": "United States",
        "industry": "Banking",
        "company_size": "Medium (500-1000 employees)",
    }

    result = agent.process(input_data)

    assert result is not None
    assert "compliance" in result.lower()
    assert "regulatory" in result.lower()
    print("✓ Regulatory assessment test passed")


def test_gdpr_compliance():
    """Test GDPR compliance assessment capability."""
    agent = ComplianceOfficer()

    input_data = {
        "task": "Assess GDPR compliance",
        "data_types": ["Personal data", "Financial data", "Contact information"],
        "data_processing": ["Storage", "Transfer", "Analysis"],
        "eu_residents": True,
    }

    result = agent.process(input_data)

    assert result is not None
    assert "gdpr" in result.lower() or "data protection" in result.lower()
    assert "consent" in result.lower() or "rights" in result.lower()
    print("✓ GDPR compliance test passed")


def test_aml_compliance():
    """Test AML compliance assessment capability."""
    agent = ComplianceOfficer()

    input_data = {
        "task": "Assess Anti-Money Laundering compliance",
        "transaction_types": [
            "Wire transfers",
            "Cash deposits",
            "International transfers",
        ],
        "customer_types": ["Individuals", "Businesses", "High-net-worth individuals"],
        "transaction_volume": "High",
    }

    result = agent.process(input_data)

    assert result is not None
    assert "aml" in result.lower() or "anti-money laundering" in result.lower()
    assert "kyc" in result.lower() or "know your customer" in result.lower()
    print("✓ AML compliance test passed")


def test_policy_development():
    """Test compliance policy development capability."""
    agent = ComplianceOfficer()

    input_data = {
        "task": "Develop compliance policy",
        "policy_type": "Data Privacy Policy",
        "scope": "All employees and contractors",
        "regulations": ["GDPR", "CCPA", "HIPAA"],
    }

    result = agent.process(input_data)

    assert result is not None
    assert "policy" in result.lower()
    assert "procedures" in result.lower() or "guidelines" in result.lower()
    print("✓ Policy development test passed")


def test_audit_preparation():
    """Test audit preparation capability."""
    agent = ComplianceOfficer()

    input_data = {
        "task": "Prepare for regulatory audit",
        "audit_type": "SOC 2 Type II",
        "audit_scope": ["Security", "Availability", "Processing Integrity"],
        "audit_date": "2026-06-01",
    }

    result = agent.process(input_data)

    assert result is not None
    assert "audit" in result.lower()
    assert "preparation" in result.lower() or "readiness" in result.lower()
    print("✓ Audit preparation test passed")


def test_risk_assessment():
    """Test compliance risk assessment capability."""
    agent = ComplianceOfficer()

    input_data = {
        "task": "Assess compliance risks",
        "business_areas": [
            "Data handling",
            "Financial reporting",
            "Third-party vendors",
        ],
        "regulations": ["SOX", "GDPR", "PCI DSS"],
    }

    result = agent.process(input_data)

    assert result is not None
    assert "risk" in result.lower()
    assert "mitigation" in result.lower() or "controls" in result.lower()
    print("✓ Risk assessment test passed")


def test_training_program():
    """Test compliance training program development capability."""
    agent = ComplianceOfficer()

    input_data = {
        "task": "Develop compliance training program",
        "target_audience": "All employees",
        "topics": ["Data privacy", "Anti-corruption", "Insider trading"],
        "duration": "Annual",
    }

    result = agent.process(input_data)

    assert result is not None
    assert "training" in result.lower()
    assert "program" in result.lower() or "curriculum" in result.lower()
    print("✓ Training program test passed")


if __name__ == "__main__":
    print("Running Compliance Officer scenario tests...")
    print()

    test_regulatory_assessment()
    test_gdpr_compliance()
    test_aml_compliance()
    test_policy_development()
    test_audit_preparation()
    test_risk_assessment()
    test_training_program()

    print()
    print("All Compliance Officer tests passed! ✓")
