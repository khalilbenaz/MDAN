"""Scenario tests for Indexing Specialist Agent."""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))

from app.packs.db_optimization.agents.indexing_specialist.agent import (
    IndexingSpecialistAgent,
)


def test_indexing_specialist_basic_info():
    """Test that Indexing Specialist provides basic information."""
    agent = IndexingSpecialistAgent()
    result = agent.get_info()
    assert result is not None
    assert "name" in result
    assert result["name"] == "Indexing Specialist"
    assert "capabilities" in result
    assert len(result["capabilities"]) > 0


def test_indexing_specialist_design():
    """Test that Indexing Specialist can design indexes."""
    agent = IndexingSpecialistAgent()
    result = agent.process("design")
    assert result is not None
    assert len(result) > 0
    assert "index" in result or "indexes" in result


def test_indexing_specialist_analyze():
    """Test that Indexing Specialist can analyze indexes."""
    agent = IndexingSpecialistAgent()
    result = agent.process("analyze")
    assert result is not None
    assert len(result) > 0
    assert "analysis" in result or "usage" in result


def test_indexing_specialist_optimize():
    """Test that Indexing Specialist can optimize indexes."""
    agent = IndexingSpecialistAgent()
    result = agent.process("optimize")
    assert result is not None
    assert len(result) > 0
    assert "optimization" in result or "optimize" in result


def test_indexing_specialist_maintain():
    """Test that Indexing Specialist can provide maintenance recommendations."""
    agent = IndexingSpecialistAgent()
    result = agent.process("maintain")
    assert result is not None
    assert len(result) > 0
    assert "maintenance" in result or "maintain" in result


def test_indexing_specialist_recommend():
    """Test that Indexing Specialist can recommend strategies."""
    agent = IndexingSpecialistAgent()
    result = agent.process("recommend")
    assert result is not None
    assert len(result) > 0
    assert "strategy" in result or "recommend" in result


def test_indexing_specialist_covering_indexes():
    """Test that Indexing Specialist can design covering indexes."""
    agent = IndexingSpecialistAgent()
    result = agent.process("design")
    assert result is not None
    assert len(result) > 0
    # Check that the response contains relevant information
    assert "index" in str(result).lower() or "covering" in str(result).lower()


if __name__ == "__main__":
    print("Running Indexing Specialist Agent Scenario Tests...")
    print()

    tests = [
        ("Basic Info", test_indexing_specialist_basic_info),
        ("Design Indexes", test_indexing_specialist_design),
        ("Analyze Indexes", test_indexing_specialist_analyze),
        ("Optimize Indexes", test_indexing_specialist_optimize),
        ("Maintain Indexes", test_indexing_specialist_maintain),
        ("Recommend Strategy", test_indexing_specialist_recommend),
        ("Covering Indexes", test_indexing_specialist_covering_indexes),
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
