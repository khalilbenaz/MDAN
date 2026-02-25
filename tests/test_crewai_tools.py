"""Tests for CrewAI tools."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from pathlib import Path
import tempfile
import json
import asyncio
import importlib.util

# Skip all tests if CrewAI is not installed
pytestmark = pytest.mark.skipif(
    importlib.util.find_spec("crewai") is None,
    reason="CrewAI not installed - optional integration",
)


class TestSerperTool:
    """Test Serper Tool."""

    @pytest.fixture
    def serper_tool(self):
        """Create a Serper Tool instance."""
        from integrations.crewai.tools.serper_tool import SerperTool

        return SerperTool(api_key="test-api-key")

    def test_serper_tool_creation(self, serper_tool):
        """Test that Serper Tool is created successfully."""
        assert serper_tool is not None
        assert serper_tool.api_key == "test-api-key"

    @patch("integrations.crewai.tools.serper_tool.SerpAPIWrapper")
    def test_serper_search(self, mock_serpapi, serper_tool):
        """Test Serper search functionality."""
        mock_wrapper = Mock()
        mock_wrapper.run.return_value = "Search results"
        mock_serpapi.return_value = mock_wrapper

        result = serper_tool.search("test query")
        assert result is not None
        mock_wrapper.run.assert_called_once()

    @patch("integrations.crewai.tools.serper_tool.SerpAPIWrapper")
    def test_serper_news(self, mock_serpapi, serper_tool):
        """Test Serper news search functionality."""
        mock_wrapper = Mock()
        mock_wrapper.run.return_value = "News results"
        mock_serpapi.return_value = mock_wrapper

        result = serper_tool.search_news("test query")
        assert result is not None

    @patch("integrations.crewai.tools.serper_tool.SerpAPIWrapper")
    def test_serper_images(self, mock_serpapi, serper_tool):
        """Test Serper image search functionality."""
        mock_wrapper = Mock()
        mock_wrapper.run.return_value = "Image results"
        mock_serpapi.return_value = mock_wrapper

        result = serper_tool.search_images("test query")
        assert result is not None


class TestSQLTool:
    """Test SQL Tool."""

    @pytest.fixture
    def sql_tool(self):
        """Create a SQL Tool instance with in-memory SQLite."""
        from integrations.crewai.tools.sql_tool import SQLTool

        return SQLTool(
            db_type="sqlite",
            database=":memory:",
        )

    def test_sql_tool_creation(self, sql_tool):
        """Test that SQL Tool is created successfully."""
        assert sql_tool is not None
        assert sql_tool.config["db_type"] == "sqlite"

    @pytest.mark.asyncio
    async def test_sql_tool_connect(self, sql_tool):
        """Test SQL Tool connection."""
        await sql_tool.connect()
        assert sql_tool.connection is not None
        await sql_tool.disconnect()

    @pytest.mark.asyncio
    async def test_sql_tool_execute_query(self, sql_tool):
        """Test SQL Tool query execution."""
        await sql_tool.connect()

        # Create a test table
        await sql_tool.execute_query(
            "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
        )

        # Insert data
        await sql_tool.execute_query("INSERT INTO test (name) VALUES ('test1')")

        # Query data
        result = await sql_tool.execute_query("SELECT * FROM test")
        assert len(result) == 1
        assert result[0]["name"] == "test1"

        await sql_tool.disconnect()

    @pytest.mark.asyncio
    async def test_sql_tool_transaction(self, sql_tool):
        """Test SQL Tool transaction handling."""
        await sql_tool.connect()

        async with sql_tool.transaction():
            await sql_tool.execute_query(
                "CREATE TABLE test_tx (id INTEGER PRIMARY KEY, value TEXT)"
            )
            await sql_tool.execute_query("INSERT INTO test_tx (value) VALUES ('test')")

        result = await sql_tool.execute_query("SELECT * FROM test_tx")
        assert len(result) == 1

        await sql_tool.disconnect()

    @pytest.mark.asyncio
    async def test_sql_tool_get_schema(self, sql_tool):
        """Test SQL Tool schema retrieval."""
        await sql_tool.connect()

        await sql_tool.execute_query(
            "CREATE TABLE schema_test (id INTEGER, name TEXT, age INTEGER)"
        )

        schema = await sql_tool.get_schema()
        assert "schema_test" in schema

        await sql_tool.disconnect()


class TestFileTool:
    """Test File Tool."""

    @pytest.fixture
    def file_tool(self, temp_dir):
        """Create a File Tool instance."""
        from integrations.crewai.tools.file_tool import FileTool

        return FileTool(base_path=str(temp_dir))

    def test_file_tool_creation(self, file_tool):
        """Test that File Tool is created successfully."""
        assert file_tool is not None
        assert file_tool.base_path is not None

    def test_file_tool_read(self, file_tool, temp_dir):
        """Test File Tool read functionality."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        content = file_tool.read("test.txt")
        assert content == "test content"

    def test_file_tool_write(self, file_tool, temp_dir):
        """Test File Tool write functionality."""
        file_tool.write("test.txt", "new content")

        test_file = temp_dir / "test.txt"
        assert test_file.exists()
        assert test_file.read_text() == "new content"

    def test_file_tool_list(self, file_tool, temp_dir):
        """Test File Tool list functionality."""
        (temp_dir / "file1.txt").write_text("content1")
        (temp_dir / "file2.txt").write_text("content2")

        files = file_tool.list_files()
        assert len(files) == 2
        assert "file1.txt" in files
        assert "file2.txt" in files

    def test_file_tool_copy(self, file_tool, temp_dir):
        """Test File Tool copy functionality."""
        source = temp_dir / "source.txt"
        source.write_text("source content")

        file_tool.copy("source.txt", "dest.txt")

        dest = temp_dir / "dest.txt"
        assert dest.exists()
        assert dest.read_text() == "source content"

    def test_file_tool_move(self, file_tool, temp_dir):
        """Test File Tool move functionality."""
        source = temp_dir / "source.txt"
        source.write_text("source content")

        file_tool.move("source.txt", "dest.txt")

        dest = temp_dir / "dest.txt"
        assert dest.exists()
        assert not source.exists()

    def test_file_tool_delete(self, file_tool, temp_dir):
        """Test File Tool delete functionality."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("content")

        file_tool.delete("test.txt")

        assert not test_file.exists()


class TestAllTools:
    """Test all tools together."""

    def test_all_tools_are_importable(self):
        """Test that all tools can be imported."""
        from integrations.crewai.tools.serper_tool import SerperTool
        from integrations.crewai.tools.sql_tool import SQLTool
        from integrations.crewai.tools.file_tool import FileTool

        assert SerperTool is not None
        assert SQLTool is not None
        assert FileTool is not None
