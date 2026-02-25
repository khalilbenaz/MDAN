#!/usr/bin/env python3
"""
CrewAI Debate Example

This example demonstrates how to use the CrewAI orchestrator to start
a multi-agent debate on a complex topic.
"""

import asyncio
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
import sys

sys.path.insert(0, str(project_root))

from integrations.crewai.orchestrator import CrewAIOrchestrator


async def main():
    """Run debate example."""

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

    # Define the debate topic
    topic = "Should we use PostgreSQL or MongoDB for this project?"

    print("🎯 Starting multi-agent debate...")
    print(f"📋 Topic: {topic}\n")

    # Start debate
    result = await orchestrator.start_debate(topic)

    if result.get("status") == "success":
        print("\n✅ Debate completed successfully!")

        if "result" in result:
            print("\n📊 Debate Summary:")
            print(result["result"])
    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    asyncio.run(main())
