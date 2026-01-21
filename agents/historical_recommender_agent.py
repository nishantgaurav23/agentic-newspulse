"""
Historical Recommender Agent - Phase 1: Contextual Planning
Prevents duplicate content and learns from past reports
"""
import json
from pathlib import Path
from datetime import datetime, timedelta

from config import settings
from models.schemas import HistoricalRecommendation
from core.utils import generate_content


HISTORICAL_RECOMMENDER_INSTRUCTION = """
You are the Historical Recommender Agent for NewsPulse AI.

Your role:
1. Analyze past reports sent to the user
2. Extract URLs and topics already covered
3. Identify patterns in what the user has seen
4. Recommend new topics to explore based on gaps
5. Ensure zero duplication of content

Key responsibilities:
- Track all URLs previously sent to prevent duplicates
- Identify topic trends and suggest related but new angles
- Learn from feedback patterns (what worked, what didn't)
- Suggest emerging topics related to the user's interests

Output format:
- List of URLs to exclude (already seen)
- Recommended new topics to explore
- Insights about content gaps or trends

Your analysis ensures that every report provides fresh, novel value.
"""


def load_user_history(user_id: str, days_back: int = 30) -> list:
    """
    Load user's report history

    Args:
        user_id: User ID
        days_back: How many days of history to load

    Returns:
        List of past reports
    """
    history_dir = settings.history_dir
    user_history_file = history_dir / f"{user_id}_history.json"

    if not user_history_file.exists():
        return []

    with open(user_history_file, "r") as f:
        all_history = json.load(f)

    # Filter to recent history
    cutoff_date = datetime.utcnow() - timedelta(days=days_back)

    recent_history = [
        report
        for report in all_history
        if datetime.fromisoformat(report["report_date"]) > cutoff_date
    ]

    return recent_history


async def run_historical_recommender_agent(
    user_id: str, priority_topics: list[str]
) -> HistoricalRecommendation:
    """
    Run the Historical Recommender Agent

    Args:
        user_id: User ID
        priority_topics: Topics from user profile

    Returns:
        HistoricalRecommendation with URLs to exclude and topics to explore
    """
    history = load_user_history(user_id)

    # Extract URLs and topics from history
    seen_urls = []
    seen_topics = []

    for report in history:
        if "articles" in report:
            for article in report["articles"]:
                if "url" in article:
                    seen_urls.append(article["url"])
        if "topics_covered" in report:
            seen_topics.extend(report["topics_covered"])

    prompt = f"""
Analyze this user's history and provide recommendations for fresh content:

Priority Topics (from user profile):
{chr(10).join(f"- {topic}" for topic in priority_topics)}

Recent History ({len(history)} reports):
- Total articles seen: {len(seen_urls)}
- Topics covered: {', '.join(set(seen_topics))}

URLs to definitely exclude:
{chr(10).join(seen_urls[:50])}  # Show first 50

Based on this history:
1. What related topics should we explore that haven't been covered recently?
2. What angles or perspectives are missing?
3. What emerging trends connect to the user's interests?

Provide:
- Recommended new topics to search (related but fresh)
- Insights about content gaps
- Suggestions for novel angles on familiar topics
"""

    # Run in thread pool to avoid blocking
    import asyncio
    loop = asyncio.get_event_loop()
    response_text = await loop.run_in_executor(
        None,
        lambda: generate_content(prompt, HISTORICAL_RECOMMENDER_INSTRUCTION)
    )

    return HistoricalRecommendation(
        recommended_topics=priority_topics,  # Will be enhanced by the agent's suggestions
        exclude_urls=seen_urls,
        insights=response_text,
    )


def save_report_to_history(user_id: str, report_data: dict):
    """
    Save a completed report to user history

    Args:
        user_id: User ID
        report_data: Report data to save
    """
    history_dir = settings.history_dir
    user_history_file = history_dir / f"{user_id}_history.json"

    # Load existing history
    if user_history_file.exists():
        with open(user_history_file, "r") as f:
            history = json.load(f)
    else:
        history = []

    # Add new report
    history.append(report_data)

    # Save updated history
    with open(user_history_file, "w") as f:
        json.dump(history, f, indent=2, default=str)
