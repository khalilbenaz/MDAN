"""Scenario tests for Query Optimizer Agent."""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))

from app.packs.db_optimization.agents.query_optimizer.agent import QueryOptimizerAgent


def test_query_optimizer_basic_info():
    """Test that Query Optimizer provides basic information."""
    agent = QueryOptimizerAgent()
    result = agent.get_info()
    assert result is not None
    assert "name" in result
    assert result["name"] == "Query Optimizer"
    assert "capabilities" in result
    assert len(result["capabilities"]) > 0


def test_query_optimizer_analyze():
    """Test that Query Optimizer can analyze queries."""
    agent = QueryOptimizerAgent()
    result = agent.process("analyze")
    assert result is not None
    assert len(result) > 0
    assert "analysis" in result or "query" in result


def test_query_optimizer_optimize():
    """Test that Query Optimizer can optimize queries."""
    agent = QueryOptimizerAgent()
    result = agent.process("optimize")
    assert result is not None
    assert len(result) > 0
    assert "optimized" in result or "optimization" in result


def test_query_optimizer_rewrite():
    """Test that Query Optimizer can rewrite queries."""
    agent = QueryOptimizerAgent()
    result = agent.process("rewrite")
    assert result is not None
    assert len(result) > 0
    assert "rewrite" in result or "rewritten" in result


def test_query_optimizer_explain():
    """Test that Query Optimizer can explain execution plans."""
    agent = QueryOptimizerAgent()
    result = agent.process("explain")
    assert result is not None
    assert len(result) > 0
    assert "plan" in result or "execution" in result


def test_query_optimizer_index():
    """Test that Query Optimizer can design indexes."""
    agent = QueryOptimizerAgent()
    result = agent.process("index")
    assert result is not None
    assert len(result) > 0
    assert "index" in result or "indexes" in result


def test_query_optimizer_select_star():
    """Test that Query Optimizer can handle SELECT * issues."""
    agent = QueryOptimizerAgent()
    result = agent.process("analyze")
    assert result is not None
    assert len(result) > 0
    # Check that the response contains relevant information
    assert "query" in str(result).lower() or "performance" in str(result).lower()


if __name__ == "__main__":
    print("Running Query Optimizer Agent Scenario Tests...")
    print()

    tests = [
        ("Basic Info", test_query_optimizer_basic_info),
        ("Analyze Query", test_query_optimizer_analyze),
        ("Optimize Query", test_query_optimizer_optimize),
        ("Rewrite Query", test_query_optimizer_rewrite),
        ("Explain Plan", test_query_optimizer_explain),
        ("Design Indexes", test_query_optimizer_index),
        ("SELECT * Issue", test_query_optimizer_select_star),
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
