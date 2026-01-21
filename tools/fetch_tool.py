"""
Content fetching tool using BeautifulSoup
Scrapes actual HTML to ground the model in real-time data and prevent hallucinations
"""
import requests
from bs4 import BeautifulSoup
from typing import Optional
from datetime import datetime
import time

from models.schemas import FetchedContent


def fetch_url_content(
    url: str,
    timeout: int = 10,
    retry_count: int = 2,
    retry_delay: int = 2,
) -> FetchedContent:
    """
    Fetch and parse content from a URL

    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds
        retry_count: Number of retries on failure
        retry_delay: Delay between retries in seconds

    Returns:
        FetchedContent object with parsed content or error information

    Note:
        This function forces the model to read ACTUAL live content rather than
        relying on search snippets, which is critical for minimizing hallucinations.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for attempt in range(retry_count + 1):
        try:
            # Fetch the page
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract title
            title = ""
            if soup.title:
                title = soup.title.string.strip()
            elif soup.find("h1"):
                title = soup.find("h1").get_text().strip()

            # Extract author
            author = None
            author_meta = soup.find("meta", {"name": "author"}) or soup.find(
                "meta", {"property": "article:author"}
            )
            if author_meta:
                author = author_meta.get("content")

            # Extract published date
            published_date = None
            date_meta = soup.find(
                "meta", {"property": "article:published_time"}
            ) or soup.find("meta", {"name": "publication_date"})
            if date_meta:
                published_date = date_meta.get("content")

            # Extract main content
            # Try to find article content (common patterns)
            content = ""
            article_tags = [
                soup.find("article"),
                soup.find("div", class_="article-body"),
                soup.find("div", class_="content"),
                soup.find("div", class_="post-content"),
                soup.find("main"),
            ]

            for tag in article_tags:
                if tag:
                    # Remove script and style tags
                    for script in tag(["script", "style", "nav", "footer"]):
                        script.decompose()

                    # Get text
                    content = tag.get_text(separator="\n", strip=True)
                    break

            # Fallback: get body text
            if not content:
                body = soup.find("body")
                if body:
                    for script in body(["script", "style", "nav", "footer"]):
                        script.decompose()
                    content = body.get_text(separator="\n", strip=True)

            # Clean up content
            lines = [
                line.strip() for line in content.split("\n") if line.strip()
            ]
            content = "\n".join(lines)

            # Extract source domain
            from urllib.parse import urlparse

            source = urlparse(url).netloc

            return FetchedContent(
                url=url,
                title=title,
                content=content,
                author=author,
                published_date=published_date,
                source=source,
                success=True,
            )

        except requests.exceptions.RequestException as e:
            if attempt < retry_count:
                time.sleep(retry_delay)
                continue

            # Final attempt failed
            return FetchedContent(
                url=url,
                title="",
                content="",
                source="",
                success=False,
                error_message=f"Failed to fetch URL: {str(e)}",
            )

        except Exception as e:
            return FetchedContent(
                url=url,
                title="",
                content="",
                source="",
                success=False,
                error_message=f"Error parsing content: {str(e)}",
            )

    # Should not reach here, but just in case
    return FetchedContent(
        url=url,
        title="",
        content="",
        source="",
        success=False,
        error_message="Max retries exceeded",
    )


def fetch_multiple_urls(urls: list[str], max_workers: int = 5) -> list[FetchedContent]:
    """
    Fetch multiple URLs concurrently

    Args:
        urls: List of URLs to fetch
        max_workers: Maximum number of concurrent workers

    Returns:
        List of FetchedContent objects
    """
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(fetch_url_content, urls))

    return results
