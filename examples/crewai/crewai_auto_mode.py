#!/usr/bin/env python3
"""
CrewAI Auto Mode Example

This example demonstrates how to use the CrewAI orchestrator in autonomous mode
to build a complete application from start to finish.
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
    """Run autonomous mode example."""

    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set")
        print("Set it with: export OPENAI_API_KEY=your-key")
        return

    # Initialize orchestrator
    orchestrator = CrewAIOrchestrator(
        project_path=str(project_root),
        auto_mode=True,
        serper_api_key=os.getenv("SERPER_API_KEY"),
    )

    # Enable auto mode
    orchestrator.enable_auto_mode()

    # Define the task
    task = "Build a simple todo application with React and Node.js"

    print("🚀 Starting autonomous mode...")
    print(f"📋 Task: {task}\n")

    # Run autonomous mode
    result = await orchestrator.run_auto_mode(task)

    if result.get("status") == "success":
        print("\n✅ Autonomous mode completed successfully!")

        # Save state
        state_file = project_root / "mdan_crewai_state.json"
        orchestrator.save_state(str(state_file))
        print(f"📁 State saved to: {state_file}")
    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    asyncio.run(main())
