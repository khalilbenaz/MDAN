"""Scenario tests for DB Performance Analyst Agent."""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))

from app.packs.db_optimization.agents.db_performance_analyst.agent import (
    DBPerformanceAnalystAgent,
)


def test_db_performance_analyst_basic_info():
    """Test that DB Performance Analyst provides basic information."""
    agent = DBPerformanceAnalystAgent()
    result = agent.get_info()
    assert result is not None
    assert "name" in result
    assert result["name"] == "DB Performance Analyst"
    assert "capabilities" in result
    assert len(result["capabilities"]) > 0


def test_db_performance_analyst_analyze():
    """Test that DB Performance Analyst can analyze performance."""
    agent = DBPerformanceAnalystAgent()
    result = agent.process("analyze")
    assert result is not None
    assert len(result) > 0
    assert "analysis" in result or "recommendations" in result


def test_db_performance_analyst_optimize():
    """Test that DB Performance Analyst can optimize performance."""
    agent = DBPerformanceAnalystAgent()
    result = agent.process("optimize")
    assert result is not None
    assert len(result) > 0
    assert "optimizations" in result or "recommendations" in result


def test_db_performance_analyst_monitor():
    """Test that DB Performance Analyst can set up monitoring."""
    agent = DBPerformanceAnalystAgent()
    result = agent.process("monitor")
    assert result is not None
    assert len(result) > 0
    assert "monitoring" in result or "metrics" in result


def test_db_performance_analyst_tune():
    """Test that DB Performance Analyst can tune configuration."""
    agent = DBPerformanceAnalystAgent()
    result = agent.process("tune")
    assert result is not None
    assert len(result) > 0
    assert "configuration" in result or "tuning" in result


def test_db_performance_analyst_scale():
    """Test that DB Performance Analyst can recommend scaling."""
    agent = DBPerformanceAnalystAgent()
    result = agent.process("scale")
    assert result is not None
    assert len(result) > 0
    assert "scaling" in result or "strategy" in result


def test_db_performance_analyst_slow_queries():
    """Test that DB Performance Analyst can handle slow query issues."""
    agent = DBPerformanceAnalystAgent()
    result = agent.process("analyze")
    assert result is not None
    assert len(result) > 0
    # Check that the response contains relevant information
    assert "performance" in str(result).lower() or "query" in str(result).lower()


if __name__ == "__main__":
    print("Running DB Performance Analyst Agent Scenario Tests...")
    print()

    tests = [
        ("Basic Info", test_db_performance_analyst_basic_info),
        ("Analyze Performance", test_db_performance_analyst_analyze),
        ("Optimize Performance", test_db_performance_analyst_optimize),
        ("Setup Monitoring", test_db_performance_analyst_monitor),
        ("Tune Configuration", test_db_performance_analyst_tune),
        ("Recommend Scaling", test_db_performance_analyst_scale),
        ("Slow Queries", test_db_performance_analyst_slow_queries),
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
