#!/usr/bin/env python3
"""
CrewAI Serper Integration Example

This example demonstrates how to use the CrewAI Serper tool for web search.
Requires SERPER_API_KEY environment variable.
"""

import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
import sys

sys.path.insert(0, str(project_root))

from integrations.crewai.tools.serper_tool import SerperTool


def main():
    """Run Serper integration example."""

    # Check for API key
    if not os.getenv("SERPER_API_KEY"):
        print("❌ SERPER_API_KEY not set")
        print("Set it with: export SERPER_API_KEY=your-key")
        print("Get your key at: https://serper.dev/")
        return

    print("🔍 Serper Web Search Example\n")

    # Initialize Serper tool
    serper_tool = SerperTool(api_key=os.getenv("SERPER_API_KEY"))

    try:
        # Web search
        print("📡 Performing web search...")
        query = "Python async programming best practices"
        print(f"Query: {query}\n")

        results = serper_tool.search(query)
        print("✅ Search results:")
        print(results)
        print()

        # News search
        print("📰 Performing news search...")
        news_query = "artificial intelligence latest news"
        print(f"Query: {news_query}\n")

        news_results = serper_tool.search_news(news_query)
        print("✅ News results:")
        print(news_results)
        print()

        # Image search
        print("🖼️  Performing image search...")
        image_query = "Python logo"
        print(f"Query: {image_query}\n")

        image_results = serper_tool.search_images(image_query)
        print("✅ Image results:")
        print(image_results)
        print()

        # Places search
        print("📍 Performing places search...")
        places_query = "coffee shops near me"
        print(f"Query: {places_query}\n")

        places_results = serper_tool.search_places(places_query)
        print("✅ Places results:")
        print(places_results)
        print()

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
