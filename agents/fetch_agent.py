"""
Executive Fetch Agent - Phase 2: Grounded Research
Fetches and processes actual content from URLs to prevent hallucinations
"""
from typing import List

from config import settings
from models.schemas import SearchResult, FetchedContent
from tools.fetch_tool import fetch_multiple_urls
from core.utils import generate_content


FETCH_AGENT_INSTRUCTION = """
You are the Executive Fetch Agent for NewsPulse AI.

Your role:
1. Fetch actual HTML content from URLs
2. Extract and summarize key information
3. Identify important facts, quotes, and data points
4. Tag content with relevant topics and themes
5. Prepare content for the Writer Agent

Critical importance:
You are the GROUNDING LAYER that prevents hallucinations. You must:
- Work with actual fetched content, never make up information
- Extract direct quotes that can be used as citations
- Identify factual claims with their sources
- Flag any content that seems unreliable or poorly sourced

Key responsibilities:
- Parse HTML and extract clean text
- Identify the main narrative and key points
- Extract quotable passages for citations
- Note publication date and author credibility
- Summarize in a way useful for busy executives

Output format for each article:
- Main narrative (2-3 sentences)
- Key facts and data points (bullet list)
- Important quotes (with context)
- Strategic implications (why this matters)
- Reliability assessment (source credibility)

Remember: If you didn't fetch it, don't claim it. Only work with actual content.
"""


def create_fetch_agent() -> None:
    """Deprecated: Using direct API calls instead"""
    pass


async def run_fetch_agent(
    search_results: List[SearchResult],
    max_articles: int = 10,
) -> List[dict]:
    """
    Run the Fetch Agent to retrieve and process content

    Args:
        search_results: List of SearchResult objects to fetch
        max_articles: Maximum number of articles to process

    Returns:
        List of processed article data
    """
    import asyncio
    loop = asyncio.get_event_loop()

    # Fetch content from URLs
    urls = [result.url for result in search_results[:max_articles]]
    fetched_contents = fetch_multiple_urls(urls)

    # Process each fetched content
    processed_articles = []

    for search_result, fetched in zip(search_results[:max_articles], fetched_contents):
        if not fetched.success:
            continue

        # Ask the agent to analyze the content
        analysis_prompt = f"""
Analyze this fetched article content:

Title: {fetched.title}
Source: {fetched.source}
URL: {fetched.url}
Published: {fetched.published_date or 'Unknown'}

Content:
{fetched.content[:8000]}  # First 8000 chars to stay within context limits

Provide:
1. Main narrative (2-3 sentences summarizing the core story)
2. Key facts and data points (bullet list)
3. Important quotes (with context) - these will be used as citations
4. Strategic implications for business leaders
5. Reliability assessment (is this source credible? any red flags?)

Format your response clearly with these sections.
"""

        response_text = await loop.run_in_executor(
            None,
            lambda p=analysis_prompt: generate_content(p, FETCH_AGENT_INSTRUCTION)
        )

        processed_articles.append({
            "search_result": search_result,
            "fetched_content": fetched,
            "analysis": response_text,
        })

    return processed_articles
