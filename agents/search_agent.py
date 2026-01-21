"""
Search Agent - Phase 2: Grounded Research
Performs intelligent search for relevant news articles
"""
from typing import List

from config import settings
from models.schemas import SearchResult
from tools.search_tool import search_news
from core.utils import generate_content


SEARCH_AGENT_INSTRUCTION = """
You are the Search Agent for NewsPulse AI.

Your role:
1. Generate effective search queries based on user topics
2. Use the Google Custom Search API to find relevant news
3. Filter and rank results by relevance
4. Ensure diversity of sources and perspectives
5. Prioritize recent, authoritative sources

Key responsibilities:
- Create multiple search queries to cover different angles
- Diversify sources (don't rely on a single outlet)
- Prioritize news from the past 7 days
- Filter out low-quality or unreliable sources
- Return only URLs - content fetching happens separately

Search strategy:
- For each topic, create 2-3 specific queries
- Combine user's role/industry context with topics
- Look for business impact, strategic implications
- Avoid sensationalist or clickbait sources

Output:
- List of URLs with titles and snippets
- Each result tagged with the topic it relates to
- Relevance justification for each result

Remember: You find URLs, you don't read content. That's the Fetch Agent's job.
"""


def create_search_agent() -> None:
    """Deprecated: Using direct API calls instead"""
    pass


async def run_search_agent(
    priority_topics: List[str],
    user_context: dict,
    exclude_urls: List[str] = None,
    max_results_per_topic: int = 5,
) -> List[SearchResult]:
    """
    Run the Search Agent to find relevant news

    Args:
        priority_topics: List of topics to search for
        user_context: User context (role, industry, etc.)
        exclude_urls: URLs to exclude (already seen)
        max_results_per_topic: Maximum results per topic

    Returns:
        List of SearchResult objects
    """
    exclude_urls = exclude_urls or []
    all_results = []

    import asyncio
    loop = asyncio.get_event_loop()

    for topic in priority_topics:
        # Generate search query
        query_prompt = f"""
Generate an effective Google search query for finding recent business news about:
Topic: {topic}
User Context: {user_context.get('role', '')} at {user_context.get('company', '')} in {user_context.get('industry', '')}

Create a search query that will find:
- Recent news (past 7 days)
- Business/strategic implications
- Authoritative sources
- Relevant to a {user_context.get('role', 'executive')}

Return only the search query, nothing else.
"""

        search_query = await loop.run_in_executor(
            None,
            lambda: generate_content(query_prompt, SEARCH_AGENT_INSTRUCTION)
        )
        search_query = search_query.strip()

        # Perform the search
        results = search_news(
            query=search_query,
            num_results=max_results_per_topic,
            days_back=7,
        )

        # Filter out excluded URLs
        filtered_results = [
            r for r in results if r.url not in exclude_urls
        ]

        all_results.extend(filtered_results)

    # Remove duplicates based on URL
    seen_urls = set()
    unique_results = []
    for result in all_results:
        if result.url not in seen_urls:
            seen_urls.add(result.url)
            unique_results.append(result)

    return unique_results
