#!/usr/bin/env python3
"""
CrewAI SQL Integration Example

This example demonstrates how to use the CrewAI SQL tool for database operations.
Uses in-memory SQLite for demonstration.
"""

import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
import sys

sys.path.insert(0, str(project_root))

from integrations.crewai.tools.sql_tool import SQLTool


async def main():
    """Run SQL integration example."""

    print("🗄️  SQL Integration Example\n")

    # Initialize SQL tool with in-memory SQLite
    sql_tool = SQLTool(
        db_type="sqlite",
        database=":memory:",
    )

    try:
        # Connect to database
        print("📡 Connecting to database...")
        await sql_tool.connect()
        print("✅ Connected successfully!\n")

        # Create a table
        print("📝 Creating table...")
        await sql_tool.execute_query("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table 'users' created!\n")

        # Insert data
        print("➕ Inserting data...")
        await sql_tool.execute_query(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ("Alice", "alice@example.com", 30),
        )
        await sql_tool.execute_query(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ("Bob", "bob@example.com", 25),
        )
        await sql_tool.execute_query(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            ("Charlie", "charlie@example.com", 35),
        )
        print("✅ Inserted 3 users!\n")

        # Query data
        print("📊 Querying data...")
        users = await sql_tool.execute_query("SELECT * FROM users")
        print(f"✅ Found {len(users)} users:")
        for user in users:
            print(f"  • {user['name']} ({user['email']}) - Age: {user['age']}")
        print()

        # Use transaction
        print("🔄 Using transaction...")
        async with sql_tool.transaction():
            await sql_tool.execute_query(
                "UPDATE users SET age = age + 1 WHERE name = ?", ("Alice",)
            )
            await sql_tool.execute_query(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                ("David", "david@example.com", 28),
            )
        print("✅ Transaction completed!\n")

        # Query updated data
        print("📊 Querying updated data...")
        users = await sql_tool.execute_query("SELECT * FROM users ORDER BY name")
        print(f"✅ Found {len(users)} users:")
        for user in users:
            print(f"  • {user['name']} ({user['email']}) - Age: {user['age']}")
        print()

        # Get schema
        print("📋 Getting schema...")
        schema = await sql_tool.get_schema()
        print("✅ Database schema:")
        for table_name, columns in schema.items():
            print(f"  Table: {table_name}")
            for column in columns:
                print(f"    • {column}")
        print()

        # Disconnect
        print("📡 Disconnecting from database...")
        await sql_tool.disconnect()
        print("✅ Disconnected successfully!\n")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if sql_tool.connection:
            await sql_tool.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
