"""Simple test script for DB Optimization Pack agents."""

import sys
import os
import asyncio
import importlib.util


def load_agent(module_path, class_name):
    """Load an agent class from a file path."""
    spec = importlib.util.spec_from_file_location("agent_module", module_path)
    if spec is None:
        raise ImportError(f"Could not load spec from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)


# Load agents
DBPerformanceAnalystAgent = load_agent(
    os.path.join(
        os.path.dirname(__file__),
        "../app/packs/db-optimization/agents/db-performance-analyst/agent.py",
    ),
    "DBPerformanceAnalystAgent",
)
QueryOptimizerAgent = load_agent(
    os.path.join(
        os.path.dirname(__file__),
        "../app/packs/db-optimization/agents/query-optimizer/agent.py",
    ),
    "QueryOptimizerAgent",
)
IndexingSpecialistAgent = load_agent(
    os.path.join(
        os.path.dirname(__file__),
        "../app/packs/db-optimization/agents/indexing-specialist/agent.py",
    ),
    "IndexingSpecialistAgent",
)


async def test_db_performance_analyst():
    """Test DB Performance Analyst agent."""
    print("Testing DB Performance Analyst agent...")
    agent = DBPerformanceAnalystAgent()

    # Test get_info method
    info = agent.get_info()
    assert info is not None
    assert "name" in info
    assert info["name"] == "DB Performance Analyst"
    assert "capabilities" in info
    assert len(info["capabilities"]) > 0

    # Test process method with a simple request
    from dataclasses import dataclass

    @dataclass
    class DBPerformanceRequest:
        action: str
        db_type: str = None
        performance_issue: str = None
        metrics: dict = None
        query_samples: list = None
        schema_info: dict = None

    request = DBPerformanceRequest(action="analyze", db_type="PostgreSQL")

    result = await agent.process(request)
    assert result is not None
    assert len(result) > 0
    print("✓ DB Performance Analyst agent test passed")
    return True


async def test_query_optimizer():
    """Test Query Optimizer agent."""
    print("Testing Query Optimizer agent...")
    agent = QueryOptimizerAgent()

    # Test get_info method
    info = agent.get_info()
    assert info is not None
    assert "name" in info
    assert info["name"] == "Query Optimizer"
    assert "capabilities" in info
    assert len(info["capabilities"]) > 0

    # Test process method with a simple request
    from dataclasses import dataclass

    @dataclass
    class QueryOptimizationRequest:
        action: str
        db_type: str = None
        query: str = None
        execution_plan: dict = None
        schema_info: dict = None
        performance_goal: str = None

    request = QueryOptimizationRequest(action="analyze", db_type="PostgreSQL")

    result = await agent.process(request)
    assert result is not None
    assert len(result) > 0
    print("✓ Query Optimizer agent test passed")
    return True


async def test_indexing_specialist():
    """Test Indexing Specialist agent."""
    print("Testing Indexing Specialist agent...")
    agent = IndexingSpecialistAgent()

    # Test get_info method
    info = agent.get_info()
    assert info is not None
    assert "name" in info
    assert info["name"] == "Indexing Specialist"
    assert "capabilities" in info
    assert len(info["capabilities"]) > 0

    # Test process method with a simple request
    from dataclasses import dataclass

    @dataclass
    class IndexingRequest:
        action: str
        db_type: str = None
        table_name: str = None
        query_patterns: list = None
        schema_info: dict = None
        current_indexes: list = None
        workload_type: str = None

    request = IndexingRequest(action="design", db_type="PostgreSQL")

    result = await agent.process(request)
    assert result is not None
    assert len(result) > 0
    print("✓ Indexing Specialist agent test passed")
    return True


async def main():
    """Run all tests."""
    print("=" * 60)
    print("DB Optimization Pack - Simple Agent Tests")
    print("=" * 60)
    print()

    all_passed = True

    try:
        all_passed &= await test_db_performance_analyst()
    except Exception as e:
        print(f"✗ DB Performance Analyst agent test failed: {e}")
        import traceback

        traceback.print_exc()
        all_passed = False

    print()

    try:
        all_passed &= await test_query_optimizer()
    except Exception as e:
        print(f"✗ Query Optimizer agent test failed: {e}")
        import traceback

        traceback.print_exc()
        all_passed = False

    print()

    try:
        all_passed &= await test_indexing_specialist()
    except Exception as e:
        print(f"✗ Indexing Specialist agent test failed: {e}")
        import traceback

        traceback.print_exc()
        all_passed = False

    print()
    print("=" * 60)
    if all_passed:
        print("All DB Optimization Pack tests passed! ✓")
    else:
        print("Some tests failed! ✗")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    all_passed = asyncio.run(main())
    sys.exit(0 if all_passed else 1)
