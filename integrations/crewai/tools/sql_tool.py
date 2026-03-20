"""Async SQL Database Connector Tool"""

import os
import asyncio
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class DatabaseType(Enum):
    """Supported database types"""

    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLSERVER = "sqlserver"
    SQLITE = "sqlite"


@dataclass
class QueryResult:
    """Represents a query result"""

    columns: List[str]
    rows: List[Dict[str, Any]]
    row_count: int
    execution_time: float


class SQLTool:
    """Async SQL database connector with support for multiple database types"""

    def __init__(
        self,
        connection_string: Optional[str] = None,
        db_type: DatabaseType = DatabaseType.POSTGRESQL,
        **kwargs,
    ):
        """
        Initialize SQLTool

        Args:
            connection_string: Database connection string. If None, reads from DATABASE_URL
            db_type: Type of database (POSTGRESQL, MYSQL, SQLSERVER, SQLITE)
            **kwargs: Additional connection parameters
        """
        self.connection_string = connection_string or os.getenv("DATABASE_URL")
        self.db_type = db_type
        self.connection_params = kwargs
        self._pool = None
        self._driver = None

        if not self.connection_string and db_type != DatabaseType.SQLLITE:
            raise ValueError(
                "DATABASE_URL not found. Set it as environment variable "
                "or pass connection_string to the constructor."
            )

        self._initialize_driver()

    def _initialize_driver(self):
        """Initialize the appropriate database driver"""
        if self.db_type == DatabaseType.POSTGRESQL:
            try:
                import asyncpg

                self._driver = asyncpg
            except ImportError:
                raise ImportError(
                    "asyncpg is not installed. Install it with: pip install asyncpg"
                )

        elif self.db_type == DatabaseType.MYSQL:
            try:
                import aiomysql

                self._driver = aiomysql
            except ImportError:
                raise ImportError(
                    "aiomysql is not installed. Install it with: pip install aiomysql"
                )

        elif self.db_type == DatabaseType.SQLSERVER:
            try:
                import aioodbc

                self._driver = aioodbc
            except ImportError:
                raise ImportError(
                    "aioodbc is not installed. Install it with: pip install aioodbc"
                )

        elif self.db_type == DatabaseType.SQLLITE:
            try:
                import aiosqlite

                self._driver = aiosqlite
            except ImportError:
                raise ImportError(
                    "aiosqlite is not installed. Install it with: pip install aiosqlite"
                )

    async def connect(self):
        """Establish database connection pool"""
        if self._pool:
            return

        if self.db_type == DatabaseType.POSTGRESQL:
            self._pool = await self._driver.create_pool(
                self.connection_string, **self.connection_params
            )

        elif self.db_type == DatabaseType.MYSQL:
            self._pool = await self._driver.create_pool(
                host=self.connection_params.get("host", "localhost"),
                port=self.connection_params.get("port", 3306),
                user=self.connection_params.get("user"),
                password=self.connection_params.get("password"),
                db=self.connection_params.get("database"),
                **self.connection_params,
            )

        elif self.db_type == DatabaseType.SQLSERVER:
            self._pool = await self._driver.create_pool(
                dsn=self.connection_string, **self.connection_params
            )

        elif self.db_type == DatabaseType.SQLLITE:
            self._pool = await self._driver.connect(
                self.connection_string or ":memory:"
            )

    async def disconnect(self):
        """Close database connection pool"""
        if self._pool:
            if self.db_type == DatabaseType.SQLLITE:
                await self._pool.close()
            else:
                self._pool.close()
                await self._pool.wait_closed()
            self._pool = None

    async def execute_query(
        self, query: str, params: Optional[tuple] = None
    ) -> QueryResult:
        """
        Execute a SELECT query and return results

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            QueryResult with columns, rows, and metadata
        """
        import time

        start_time = time.time()

        if not self._pool:
            await self.connect()

        try:
            if self.db_type == DatabaseType.POSTGRESQL:
                async with self._pool.acquire() as conn:
                    rows = (
                        await conn.fetch(query, *params)
                        if params
                        else await conn.fetch(query)
                    )
                    columns = list(rows[0].keys()) if rows else []
                    row_dicts = [dict(row) for row in rows]

            elif self.db_type == DatabaseType.MYSQL:
                async with self._pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute(query, params or ())
                        rows = await cursor.fetchall()
                        columns = (
                            [desc[0] for desc in cursor.description]
                            if cursor.description
                            else []
                        )
                        row_dicts = [dict(zip(columns, row)) for row in rows]

            elif self.db_type == DatabaseType.SQLSERVER:
                async with self._pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute(query, params or ())
                        rows = await cursor.fetchall()
                        columns = (
                            [column[0] for column in cursor.description]
                            if cursor.description
                            else []
                        )
                        row_dicts = [dict(zip(columns, row)) for row in rows]

            elif self.db_type == DatabaseType.SQLLITE:
                rows = await self._pool.execute_fetchall(query, params or ())
                columns = (
                    [desc[0] for desc in self._pool.description]
                    if self._pool.description
                    else []
                )
                row_dicts = [dict(zip(columns, row)) for row in rows]

            execution_time = time.time() - start_time

            return QueryResult(
                columns=columns,
                rows=row_dicts,
                row_count=len(row_dicts),
                execution_time=execution_time,
            )

        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise RuntimeError(f"Query execution failed: {str(e)}") from e

    async def execute_command(
        self, command: str, params: Optional[tuple] = None
    ) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE command

        Args:
            command: SQL command string
            params: Command parameters

        Returns:
            Number of affected rows
        """
        if not self._pool:
            await self.connect()

        try:
            if self.db_type == DatabaseType.POSTGRESQL:
                async with self._pool.acquire() as conn:
                    result = (
                        await conn.execute(command, *params)
                        if params
                        else await conn.execute(command)
                    )
                    return result.split()[-1] if isinstance(result, str) else result

            elif self.db_type == DatabaseType.MYSQL:
                async with self._pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute(command, params or ())
                        await conn.commit()
                        return cursor.rowcount

            elif self.db_type == DatabaseType.SQLSERVER:
                async with self._pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute(command, params or ())
                        return cursor.rowcount

            elif self.db_type == DatabaseType.SQLLITE:
                await self._pool.execute(command, params or ())
                await self._pool.commit()
                return self._pool.total_changes

        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            raise RuntimeError(f"Command execution failed: {str(e)}") from e

    async def execute_transaction(self, commands: List[tuple]) -> List[int]:
        """
        Execute multiple commands in a transaction

        Args:
            commands: List of (command, params) tuples

        Returns:
            List of affected row counts
        """
        if not self._pool:
            await self.connect()

        results = []

        try:
            if self.db_type == DatabaseType.POSTGRESQL:
                async with self._pool.acquire() as conn:
                    async with conn.transaction():
                        for command, params in commands:
                            result = (
                                await conn.execute(command, *params)
                                if params
                                else await conn.execute(command)
                            )
                            results.append(
                                int(result.split()[-1])
                                if isinstance(result, str)
                                else result
                            )

            elif self.db_type in [DatabaseType.MYSQL, DatabaseType.SQLSERVER]:
                async with self._pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        for command, params in commands:
                            await cursor.execute(command, params or ())
                            results.append(cursor.rowcount)
                        await conn.commit()

            elif self.db_type == DatabaseType.SQLLITE:
                for command, params in commands:
                    await self._pool.execute(command, params or ())
                    results.append(self._pool.total_changes)
                await self._pool.commit()

            return results

        except Exception as e:
            logger.error(f"Transaction failed: {str(e)}")
            raise RuntimeError(f"Transaction failed: {str(e)}") from e

    async def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get schema information for a table"""
        if self.db_type == DatabaseType.POSTGRESQL:
            query = """
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = $1
                ORDER BY ordinal_position
            """
            result = await self.execute_query(query, (table_name,))
            return result.rows

        elif self.db_type == DatabaseType.MYSQL:
            query = """
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
            """
            result = await self.execute_query(query, (table_name,))
            return result.rows

        elif self.db_type == DatabaseType.SQLSERVER:
            query = """
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = ?
                ORDER BY ordinal_position
            """
            result = await self.execute_query(query, (table_name,))
            return result.rows

        elif self.db_type == DatabaseType.SQLLITE:
            query = f"PRAGMA table_info({table_name})"
            result = await self.execute_query(query)
            return result.rows

    async def list_tables(self) -> List[str]:
        """List all tables in the database"""
        if self.db_type == DatabaseType.POSTGRESQL:
            query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """
        elif self.db_type == DatabaseType.MYSQL:
            query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = DATABASE()
                ORDER BY table_name
            """
        elif self.db_type == DatabaseType.SQLSERVER:
            query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_type = 'BASE TABLE'
                ORDER BY table_name
            """
        elif self.db_type == DatabaseType.SQLLITE:
            query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"

        result = await self.execute_query(query)
        return [
            row["table_name"] if "table_name" in row else row["name"]
            for row in result.rows
        ]

    def format_results(self, result: QueryResult) -> str:
        """Format query results as readable text"""
        lines = [
            f"Query returned {result.row_count} rows in {result.execution_time:.3f}s",
            "",
        ]

        if result.columns:
            header = " | ".join(result.columns)
            lines.append(header)
            lines.append("-" * len(header))

        for row in result.rows:
            values = " | ".join(str(v) for v in row.values())
            lines.append(values)

        return "\n".join(lines)

    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()


def run_query_sync(query: str, params: Optional[tuple] = None, **kwargs) -> QueryResult:
    """
    Synchronous wrapper for async query execution

    Args:
        query: SQL query string
        params: Query parameters
        **kwargs: Additional SQLTool parameters

    Returns:
        QueryResult with columns, rows, and metadata
    """

    async def _run():
        async with SQLTool(**kwargs) as db:
            return await db.execute_query(query, params)

    return asyncio.run(_run())
