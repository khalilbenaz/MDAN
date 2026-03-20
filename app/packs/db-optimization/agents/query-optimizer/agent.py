"""
Query Optimizer Agent

Specialized agent for SQL query optimization, execution plan analysis, and query refactoring.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import asyncio


@dataclass
class QueryOptimizationRequest:
    """Request data structure for the Query Optimizer agent."""

    action: str
    db_type: Optional[str] = None
    query: Optional[str] = None
    execution_plan: Optional[Dict[str, Any]] = None
    schema_info: Optional[Dict[str, Any]] = None
    performance_goal: Optional[str] = None


class QueryOptimizerAgent:
    """
    Query Optimizer - Expert in SQL query optimization and execution plan analysis.

    Specialized in analyzing SQL queries, understanding execution plans, and providing
    optimization recommendations. Expert in query refactoring, index utilization, and
    join optimization strategies.
    """

    def __init__(self):
        """Initialize the Query Optimizer agent."""
        self.name = "Query Optimizer"
        self.title = "SQL Query Optimization and Execution Plan Expert"
        self.icon = "⚡"
        self.capabilities = [
            "SQL query analysis and optimization",
            "Execution plan interpretation",
            "Query refactoring and rewriting",
            "Index utilization optimization",
            "Join strategy optimization",
            "Subquery optimization",
            "CTE and window function optimization",
            "Query performance prediction",
            "Index design for queries",
            "Query caching strategies",
        ]
        self.role = "Query Optimization Expert"
        self.identity = (
            "Expert query optimizer with deep understanding of SQL query execution, "
            "database query planners, and optimization techniques. Specialized in "
            "transforming inefficient queries into high-performing alternatives."
        )
        self.communication_style = (
            "Technical and precise, focusing on query mechanics, execution plans, "
            "and optimization techniques. Provides concrete query rewrites with "
            "explanations of why they perform better."
        )
        self.principles = [
            "Understand the execution plan before optimizing",
            "Optimize for the actual data distribution",
            "Consider the query's place in the overall workload",
            "Balance query complexity with maintainability",
            "Use appropriate join types and orders",
            "Leverage indexes effectively",
            "Avoid unnecessary data processing",
            "Test optimizations with realistic data volumes",
        ]

    async def process(self, request: QueryOptimizationRequest) -> Dict[str, Any]:
        """
        Process the query optimization request and return a response.

        Args:
            request: The query optimization request to process

        Returns:
            A dictionary containing the optimization analysis and recommendations
        """
        action = request.action.lower()

        if action == "analyze":
            return await self._analyze_query(request)
        elif action == "optimize":
            return await self._optimize_query(request)
        elif action == "rewrite":
            return await self._rewrite_query(request)
        elif action == "explain":
            return await self._explain_plan(request)
        elif action == "index":
            return await self._design_indexes(request)
        else:
            return await self._handle_unknown_action(request)

    async def _analyze_query(self, request: QueryOptimizationRequest) -> Dict[str, Any]:
        """
        Analyze query performance.

        Args:
            request: The request to process

        Returns:
            Query analysis results
        """
        db_type = request.db_type or "PostgreSQL"
        query = request.query or ""
        execution_plan = request.execution_plan or {}

        analysis = {
            "status": "success",
            "action": "analyze",
            "db_type": db_type,
            "query": query,
            "query_type": self._identify_query_type(query),
            "complexity": self._assess_complexity(query),
            "performance_issues": self._identify_performance_issues(
                query, execution_plan
            ),
            "bottlenecks": self._identify_bottlenecks(execution_plan),
            "optimization_potential": self._estimate_optimization_potential(
                query, execution_plan
            ),
        }

        return analysis

    async def _optimize_query(
        self, request: QueryOptimizationRequest
    ) -> Dict[str, Any]:
        """
        Optimize query performance.

        Args:
            request: The request to process

        Returns:
            Query optimization recommendations
        """
        db_type = request.db_type or "PostgreSQL"
        query = request.query or ""
        execution_plan = request.execution_plan or {}

        optimization = {
            "status": "success",
            "action": "optimize",
            "db_type": db_type,
            "original_query": query,
            "optimized_query": self._generate_optimized_query(query, db_type),
            "optimizations_applied": self._list_optimizations(query, db_type),
            "expected_improvement": self._estimate_improvement(query, execution_plan),
            "index_recommendations": self._recommend_indexes_for_query(query, db_type),
            "configuration_suggestions": self._suggest_configuration(query, db_type),
        }

        return optimization

    async def _rewrite_query(self, request: QueryOptimizationRequest) -> Dict[str, Any]:
        """
        Rewrite query for better performance.

        Args:
            request: The request to process

        Returns:
            Query rewrite recommendations
        """
        db_type = request.db_type or "PostgreSQL"
        query = request.query or ""

        rewrite = {
            "status": "success",
            "action": "rewrite",
            "db_type": db_type,
            "original_query": query,
            "rewritten_query": self._rewrite_query_for_performance(query, db_type),
            "rewrite_explanation": self._explain_rewrite(query, db_type),
            "alternative_approaches": self._provide_alternatives(query, db_type),
            "trade_offs": self._explain_trade_offs(query, db_type),
        }

        return rewrite

    async def _explain_plan(self, request: QueryOptimizationRequest) -> Dict[str, Any]:
        """
        Explain execution plan.

        Args:
            request: The request to process

        Returns:
            Execution plan explanation
        """
        db_type = request.db_type or "PostgreSQL"
        execution_plan = request.execution_plan or {}

        explanation = {
            "status": "success",
            "action": "explain",
            "db_type": db_type,
            "plan_summary": self._summarize_plan(execution_plan),
            "step_by_step": self._explain_plan_steps(execution_plan),
            "cost_analysis": self._analyze_plan_cost(execution_plan),
            "bottlenecks": self._identify_plan_bottlenecks(execution_plan),
            "optimization_opportunities": self._find_plan_optimizations(execution_plan),
        }

        return explanation

    async def _design_indexes(
        self, request: QueryOptimizationRequest
    ) -> Dict[str, Any]:
        """
        Design indexes for query optimization.

        Args:
            request: The request to process

        Returns:
            Index design recommendations
        """
        db_type = request.db_type or "PostgreSQL"
        query = request.query or ""
        schema_info = request.schema_info or {}

        index_design = {
            "status": "success",
            "action": "index",
            "db_type": db_type,
            "query": query,
            "recommended_indexes": self._design_query_indexes(
                query, schema_info, db_type
            ),
            "index_types": self._recommend_index_types(query, db_type),
            "index_ordering": self._recommend_index_ordering(query, db_type),
            "partial_indexes": self._suggest_partial_indexes(query, db_type),
            "covering_indexes": self._suggest_covering_indexes(query, db_type),
            "maintenance_considerations": self._explain_index_maintenance(db_type),
        }

        return index_design

    async def _handle_unknown_action(
        self, request: QueryOptimizationRequest
    ) -> Dict[str, Any]:
        """
        Handle unknown action.

        Args:
            request: The request to process

        Returns:
            Error response
        """
        return {
            "status": "error",
            "action": request.action,
            "message": f"Unknown action: {request.action}",
            "available_actions": [
                "analyze",
                "optimize",
                "rewrite",
                "explain",
                "index",
            ],
        }

    def _identify_query_type(self, query: str) -> str:
        """Identify query type."""
        query_upper = query.upper().strip()
        if query_upper.startswith("SELECT"):
            return "SELECT"
        elif query_upper.startswith("INSERT"):
            return "INSERT"
        elif query_upper.startswith("UPDATE"):
            return "UPDATE"
        elif query_upper.startswith("DELETE"):
            return "DELETE"
        else:
            return "UNKNOWN"

    def _assess_complexity(self, query: str) -> str:
        """Assess query complexity."""
        complexity_indicators = [
            "JOIN",
            "SUBQUERY",
            "UNION",
            "GROUP BY",
            "HAVING",
            "WINDOW",
            "CTE",
        ]

        count = sum(
            1 for indicator in complexity_indicators if indicator in query.upper()
        )

        if count == 0:
            return "simple"
        elif count <= 2:
            return "moderate"
        else:
            return "complex"

    def _identify_performance_issues(
        self, query: str, execution_plan: Dict[str, Any]
    ) -> List[str]:
        """Identify performance issues."""
        issues = []

        query_upper = query.upper()

        if "SELECT *" in query_upper:
            issues.append("Using SELECT * instead of specific columns")

        if "ORDER BY" in query_upper and "LIMIT" not in query_upper:
            issues.append("ORDER BY without LIMIT may process many rows")

        if query_upper.count("JOIN") > 3:
            issues.append("Multiple joins may benefit from optimization")

        if execution_plan.get("seq_scan", False):
            issues.append("Sequential scan detected - consider indexing")

        if execution_plan.get("nested_loop", False):
            issues.append("Nested loop join may be inefficient for large datasets")

        return issues

    def _identify_bottlenecks(self, execution_plan: Dict[str, Any]) -> List[str]:
        """Identify execution plan bottlenecks."""
        bottlenecks = []

        if execution_plan.get("high_cost", False):
            bottlenecks.append("High cost operation detected")

        if execution_plan.get("large_rows", False):
            bottlenecks.append("Processing large number of rows")

        if execution_plan.get("disk_spill", False):
            bottlenecks.append("Disk spill detected - increase work_mem")

        return bottlenecks

    def _estimate_optimization_potential(
        self, query: str, execution_plan: Dict[str, Any]
    ) -> str:
        """Estimate optimization potential."""
        issues = self._identify_performance_issues(query, execution_plan)

        if len(issues) == 0:
            return "low"
        elif len(issues) <= 2:
            return "medium"
        else:
            return "high"

    def _generate_optimized_query(self, query: str, db_type: str) -> str:
        """Generate optimized query."""
        # Simple optimization examples
        optimized = query

        # Replace SELECT * with specific columns (placeholder)
        if "SELECT *" in optimized.upper():
            optimized = optimized.replace("SELECT *", "SELECT id, name, created_at")

        # Add LIMIT if missing (placeholder)
        if "ORDER BY" in optimized.upper() and "LIMIT" not in optimized.upper():
            optimized += " LIMIT 1000"

        return optimized

    def _list_optimizations(self, query: str, db_type: str) -> List[Dict[str, Any]]:
        """List optimizations applied."""
        optimizations = []

        if "SELECT *" in query.upper():
            optimizations.append(
                {
                    "type": "column_selection",
                    "description": "Replaced SELECT * with specific columns",
                    "impact": "Reduces I/O and network transfer",
                }
            )

        if "ORDER BY" in query.upper() and "LIMIT" not in query.upper():
            optimizations.append(
                {
                    "type": "limit_clause",
                    "description": "Added LIMIT clause",
                    "impact": "Prevents processing unnecessary rows",
                }
            )

        return optimizations

    def _estimate_improvement(
        self, query: str, execution_plan: Dict[str, Any]
    ) -> Dict[str, str]:
        """Estimate performance improvement."""
        return {
            "execution_time": "30-70% faster",
            "resource_usage": "40-60% reduction",
            "io_operations": "50-80% reduction",
        }

    def _recommend_indexes_for_query(
        self, query: str, db_type: str
    ) -> List[Dict[str, Any]]:
        """Recommend indexes for query."""
        return [
            {
                "table": "users",
                "columns": ["email"],
                "type": "btree",
                "unique": True,
                "reason": "Frequent WHERE clause on email",
            },
        ]

    def _suggest_configuration(self, query: str, db_type: str) -> List[Dict[str, Any]]:
        """Suggest configuration changes."""
        return [
            {
                "parameter": "work_mem",
                "value": "16MB",
                "reason": "Improve sort and hash operations",
            },
        ]

    def _rewrite_query_for_performance(self, query: str, db_type: str) -> str:
        """Rewrite query for performance."""
        # Example rewrite: subquery to JOIN
        if "IN (SELECT" in query.upper():
            # Simple placeholder rewrite
            return query.replace("IN (SELECT", "JOIN")

        return query

    def _explain_rewrite(self, query: str, db_type: str) -> str:
        """Explain query rewrite."""
        return "Rewritten to use JOIN instead of subquery for better performance"

    def _provide_alternatives(self, query: str, db_type: str) -> List[Dict[str, Any]]:
        """Provide alternative approaches."""
        return [
            {
                "approach": "Use EXISTS instead of IN",
                "when": "Checking for existence in subquery",
                "benefit": "Can be faster with proper indexing",
            },
        ]

    def _explain_trade_offs(self, query: str, db_type: str) -> List[str]:
        """Explain trade-offs."""
        return [
            "More complex queries may be harder to maintain",
            "Indexing improves read performance but slows writes",
            "Denormalization improves read speed but complicates updates",
        ]

    def _summarize_plan(self, execution_plan: Dict[str, Any]) -> str:
        """Summarize execution plan."""
        return "Query uses index scan with nested loop join"

    def _explain_plan_steps(
        self, execution_plan: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Explain plan steps."""
        return [
            {"step": 1, "operation": "Index Scan", "table": "users", "cost": "low"},
            {"step": 2, "operation": "Nested Loop", "cost": "medium"},
            {"step": 3, "operation": "Sort", "cost": "medium"},
        ]

    def _analyze_plan_cost(self, execution_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze plan cost."""
        return {
            "total_cost": "medium",
            "startup_cost": "low",
            "rows_estimated": 1000,
            "width": "100 bytes",
        }

    def _identify_plan_bottlenecks(self, execution_plan: Dict[str, Any]) -> List[str]:
        """Identify plan bottlenecks."""
        return ["Sort operation on large dataset"]

    def _find_plan_optimizations(self, execution_plan: Dict[str, Any]) -> List[str]:
        """Find plan optimizations."""
        return ["Add index on sort column", "Increase work_mem for sort"]

    def _design_query_indexes(
        self, query: str, schema_info: Dict[str, Any], db_type: str
    ) -> List[Dict[str, Any]]:
        """Design indexes for query."""
        return [
            {
                "name": "idx_users_email",
                "table": "users",
                "columns": ["email"],
                "type": "btree",
                "unique": True,
            },
        ]

    def _recommend_index_types(self, query: str, db_type: str) -> List[Dict[str, Any]]:
        """Recommend index types."""
        return [
            {"type": "btree", "use_case": "Equality and range queries"},
            {"type": "hash", "use_case": "Equality queries only"},
            {"type": "gin", "use_case": "JSONB and array columns"},
        ]

    def _recommend_index_ordering(self, query: str, db_type: str) -> List[str]:
        """Recommend index column ordering."""
        return ["Most selective column first", "Equality columns before range columns"]

    def _suggest_partial_indexes(
        self, query: str, db_type: str
    ) -> List[Dict[str, Any]]:
        """Suggest partial indexes."""
        return [
            {
                "condition": "WHERE active = true",
                "benefit": "Smaller index, faster queries",
            },
        ]

    def _suggest_covering_indexes(
        self, query: str, db_type: str
    ) -> List[Dict[str, Any]]:
        """Suggest covering indexes."""
        return [
            {
                "columns": ["user_id", "created_at", "status"],
                "benefit": "Index-only scan, no table access needed",
            },
        ]

    def _explain_index_maintenance(self, db_type: str) -> List[str]:
        """Explain index maintenance considerations."""
        return [
            "Indexes slow down INSERT, UPDATE, DELETE operations",
            "Regular index maintenance (VACUUM, ANALYZE) required",
            "Monitor index usage and remove unused indexes",
        ]

    def get_info(self) -> Dict[str, Any]:
        """
        Get agent information.

        Returns:
            Agent information dictionary
        """
        return {
            "name": self.name,
            "title": self.title,
            "icon": self.icon,
            "role": self.role,
            "capabilities": self.capabilities,
            "identity": self.identity,
            "communication_style": self.communication_style,
            "principles": self.principles,
        }
