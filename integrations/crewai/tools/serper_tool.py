"""SerperDevTool Wrapper for Web Search"""

import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

try:
    from crewai_tools import SerperDevTool as CrewAISerperTool

    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False


@dataclass
class SearchResult:
    """Represents a single search result"""

    title: str
    link: str
    snippet: str
    position: int


@dataclass
class SearchResponse:
    """Represents the complete search response"""

    query: str
    results: List[SearchResult]
    total_results: int
    search_time: float


class SerperTool:
    """Wrapper around CrewAI SerperDevTool for web search capabilities"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize SerperTool

        Args:
            api_key: Serper API key. If None, reads from SERPER_API_KEY env var
        """
        self.api_key = api_key or os.getenv("SERPER_API_KEY")

        if not self.api_key:
            raise ValueError(
                "SERPER_API_KEY not found. Set it as environment variable "
                "or pass it to the constructor."
            )

        if not CREWAI_AVAILABLE:
            raise ImportError(
                "crewai-tools is not installed. Install it with: "
                "pip install 'crewai[tools]'"
            )

        self._tool = CrewAISerperTool()

    def search(
        self, query: str, num_results: int = 10, search_type: str = "search"
    ) -> SearchResponse:
        """
        Perform a web search using Serper API

        Args:
            query: Search query string
            num_results: Number of results to return (default: 10)
            search_type: Type of search - 'search', 'news', 'images', 'places'

        Returns:
            SearchResponse with results
        """
        try:
            import time

            start_time = time.time()

            result = self._tool._run(
                query=query, n=num_results, search_type=search_type
            )

            search_time = time.time() - start_time

            return self._parse_response(query, result, search_time)

        except Exception as e:
            raise RuntimeError(f"Search failed: {str(e)}") from e

    def _parse_response(
        self, query: str, raw_result: Any, search_time: float
    ) -> SearchResponse:
        """Parse raw Serper response into structured format"""
        results = []

        if isinstance(raw_result, dict):
            organic = raw_result.get("organic", [])
            total = raw_result.get("searchInformation", {}).get(
                "totalResults", len(organic)
            )

            for idx, item in enumerate(organic):
                results.append(
                    SearchResult(
                        title=item.get("title", ""),
                        link=item.get("link", ""),
                        snippet=item.get("snippet", ""),
                        position=idx + 1,
                    )
                )
        elif isinstance(raw_result, str):
            results.append(
                SearchResult(
                    title="Search Result", link="", snippet=raw_result, position=1
                )
            )
            total = 1

        return SearchResponse(
            query=query, results=results, total_results=total, search_time=search_time
        )

    def search_news(self, query: str, num_results: int = 10) -> SearchResponse:
        """Search for news articles"""
        return self.search(query, num_results, search_type="news")

    def search_images(self, query: str, num_results: int = 10) -> SearchResponse:
        """Search for images"""
        return self.search(query, num_results, search_type="images")

    def search_places(self, query: str, num_results: int = 10) -> SearchResponse:
        """Search for places"""
        return self.search(query, num_results, search_type="places")

    def get_top_result(self, query: str) -> Optional[SearchResult]:
        """Get the top search result only"""
        response = self.search(query, num_results=1)
        return response.results[0] if response.results else None

    def format_results(
        self, response: SearchResponse, max_snippet_length: int = 200
    ) -> str:
        """Format search results as readable text"""
        lines = [
            f"Query: {response.query}",
            f"Found {response.total_results} results in {response.search_time:.2f}s",
            "",
        ]

        for result in response.results:
            snippet = result.snippet[:max_snippet_length]
            if len(result.snippet) > max_snippet_length:
                snippet += "..."

            lines.extend(
                [
                    f"{result.position}. {result.title}",
                    f"   {result.link}",
                    f"   {snippet}",
                    "",
                ]
            )

        return "\n".join(lines)

    def to_crewai_tool(self):
        """Return the underlying CrewAI tool for direct use"""
        return self._tool
