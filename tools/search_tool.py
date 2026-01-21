"""
Google Custom Search API tool
Separates search (finding URLs) from content fetching to minimize hallucinations
"""
from typing import List, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import settings
from models.schemas import SearchResult


def google_search(
    query: str,
    num_results: int = 10,
    date_restrict: Optional[str] = None,
    site_restrict: Optional[str] = None,
) -> List[SearchResult]:
    """
    Perform Google Custom Search and return structured results

    Args:
        query: Search query string
        num_results: Number of results to return (max 10 per request)
        date_restrict: Date restriction (e.g., 'd7' for last 7 days, 'm1' for last month)
        site_restrict: Restrict to specific site (e.g., 'bloomberg.com')

    Returns:
        List of SearchResult objects with URLs and metadata

    Note:
        This function ONLY returns URLs and snippets, NOT full content.
        Content must be fetched separately using fetch_url_content.
    """
    try:
        # Build the Custom Search service
        service = build(
            "customsearch",
            "v1",
            developerKey=settings.google_search_api_key,
        )

        # Prepare search parameters
        search_params = {
            "q": query,
            "cx": settings.google_search_engine_id,
            "num": min(num_results, 10),  # API limit is 10 per request
        }

        if date_restrict:
            search_params["dateRestrict"] = date_restrict

        if site_restrict:
            search_params["siteSearch"] = site_restrict
            search_params["siteSearchFilter"] = "i"  # Include only

        # Execute search
        result = service.cse().list(**search_params).execute()

        # Parse results
        search_results = []
        if "items" in result:
            for item in result["items"]:
                search_result = SearchResult(
                    query=query,
                    url=item.get("link", ""),
                    title=item.get("title", ""),
                    snippet=item.get("snippet", ""),
                    source=item.get("displayLink", ""),
                    published_date=item.get("pagemap", {})
                    .get("metatags", [{}])[0]
                    .get("article:published_time"),
                )
                search_results.append(search_result)

        return search_results

    except HttpError as e:
        print(f"Search API error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected search error: {e}")
        return []


def search_news(
    query: str, num_results: int = 10, days_back: int = 7
) -> List[SearchResult]:
    """
    Search for recent news articles

    Args:
        query: News search query
        num_results: Number of results to return
        days_back: How many days back to search

    Returns:
        List of SearchResult objects
    """
    date_restrict = f"d{days_back}"
    return google_search(
        query=query, num_results=num_results, date_restrict=date_restrict
    )
