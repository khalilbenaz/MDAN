#!/usr/bin/env python3
"""
CrewAI Custom Crew Example

This example demonstrates how to create a custom crew with specific agents
and execute tasks with them.
"""

import asyncio
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
import sys

sys.path.insert(0, str(project_root))

from integrations.crewai.orchestrator import CrewAIOrchestrator
from crewai import Task, Process


async def main():
    """Run custom crew example."""

    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set")
        print("Set it with: export OPENAI_API_KEY=your-key")
        return

    # Initialize orchestrator
    orchestrator = CrewAIOrchestrator(
        project_path=str(project_root),
        serper_api_key=os.getenv("SERPER_API_KEY"),
    )

    print("🤖 Creating custom crew...\n")

    # Create a custom crew with specific agents
    crew = orchestrator.create_crew(
        agent_names=["product", "architect", "dev"],
        process=Process.sequential,
        verbose=True,
    )

    print(f"✅ Crew created with {len(crew.agents)} agents:")
    for agent in crew.agents:
        print(f"  • {agent.role} ({agent.name})")

    # Define tasks
    tasks = [
        Task(
            description="Create a PRD for a simple blog application",
            agent=crew.agents[0],
            expected_output="A complete PRD document",
        ),
        Task(
            description="Design the system architecture for the blog",
            agent=crew.agents[1],
            expected_output="Architecture document with tech stack",
        ),
        Task(
            description="Implement the core features of the blog",
            agent=crew.agents[2],
            expected_output="Working blog application code",
        ),
    ]

    print(f"\n📋 Created {len(tasks)} tasks:")
    for i, task in enumerate(tasks, 1):
        print(f"  {i}. {task.description[:50]}...")

    # Execute crew
    print("\n🚀 Executing crew...\n")
    result = await orchestrator.execute_crew(crew, tasks)

    if result.get("status") == "success":
        print("\n✅ Crew execution completed successfully!")
    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    asyncio.run(main())
