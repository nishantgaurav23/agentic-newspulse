"""
Writer Agent - Phase 3: Verification Loop
Drafts news summaries with citations
"""
from typing import List
import uuid
from datetime import datetime

from config import settings
from models.schemas import NewsReport, Article, Citation, Priority
from core.utils import generate_content


WRITER_AGENT_INSTRUCTION = """
You are the Writer Agent for NewsPulse AI, an expert business analyst and writer.

Your role:
1. Synthesize fetched content into executive summaries
2. Write clear, concise, actionable insights
3. CRITICAL: Include citations for EVERY claim
4. Prioritize articles by business impact
5. Explain relevance to the specific user

Absolute requirements (VERIFICATION WILL REJECT IF NOT MET):
- Every factual claim must have a citation
- Citations must include: claim, direct quote, source URL, source title
- No speculation or unsupported assertions
- Write for C-suite executives (clear, strategic, concise)
- Explain "why this matters" for each article

CRITICAL - CITATION REQUIREMENT:
- NEVER produce an article with zero citations
- If you cannot cite a claim, DO NOT include that article
- Each article MUST have at least 1 citation
- Articles without citations will be automatically rejected

Writing style:
- Executive summary: 2-3 paragraphs, big picture
- Article summaries: 3-4 sentences, focus on impact
- Key insights: 3-5 bullet points, actionable
- Relevance: 1-2 sentences linking to user's context

Priority levels:
- CRITICAL: Immediate business impact, major market shifts
- HIGH: Significant developments in user's industry
- MEDIUM: Important trends to monitor
- LOW: Informative but not urgent

Citation format (MANDATORY):
For each claim, you must provide:
{
  "claim": "The specific fact or statement",
  "source_url": "URL where this was found",
  "source_title": "Title of the article",
  "quote": "Direct quote from the source supporting this claim"
}

Example:
If you write "Company X revenue grew 25% this quarter", you must cite:
- Claim: "Company X revenue grew 25% this quarter"
- Quote: "The company reported quarterly revenue of $1.5B, up 25% year-over-year"
- Source URL: https://...
- Source Title: "Company X Q4 Earnings Report"

Remember: The Verification Agent will REJECT your work if citations are missing or inadequate.
Write as if a fact-checker will scrutinize every sentence.
"""


def create_writer_agent() -> None:
    """Deprecated: Using direct API calls instead"""
    pass


async def run_writer_agent(
    processed_articles: List[dict],
    user_context: dict,
    max_articles: int = 10,
) -> NewsReport:
    """
    Run the Writer Agent to create a news report

    Args:
        processed_articles: List of processed article data from Fetch Agent
        user_context: User context and personalization data
        max_articles: Maximum articles to include in report

    Returns:
        NewsReport object (may need verification)
    """
    # Prepare article data for the writer
    articles_context = []
    for i, item in enumerate(processed_articles[:max_articles], 1):
        articles_context.append(f"""
Article {i}:
Title: {item['search_result'].title}
Source: {item['search_result'].source}
URL: {item['search_result'].url}
Published: {item['search_result'].published_date or 'Unknown'}

Analysis from Fetch Agent:
{item['analysis']}

---
""")

    prompt = f"""
Create a comprehensive executive news report based on these articles.

User Context:
- Role: {user_context.get('role', 'Executive')}
- Company: {user_context.get('company', '')}
- Industry: {user_context.get('industry', '')}
- Interests: {', '.join(user_context.get('priority_topics', []))}

Articles to analyze:
{chr(10).join(articles_context)}

Create a report with:

1. Executive Summary (2-3 paragraphs covering the big picture)

2. Individual Articles (for each article above):
   - Title (create a compelling, clear title)
   - Summary (3-4 sentences on what happened and why it matters)
   - Key Insights (3-5 actionable bullet points)
   - Citations (MANDATORY: every fact needs a citation with claim, quote, source_url, source_title)
   - Priority (CRITICAL, HIGH, MEDIUM, or LOW)
   - Relevance Reason (why this matters to this specific user)

CRITICAL JSON FORMATTING REQUIREMENTS:
1. Output ONLY valid JSON - no extra text before or after
2. Escape all quotes inside strings with \"
3. Use \\n for newlines inside strings (do not use actual newlines)
4. Ensure all strings are properly closed with "
5. All JSON must be properly formatted and parseable

Format your response as valid JSON matching this exact structure:
{{
  "executive_summary": "...",
  "articles": [
    {{
      "title": "...",
      "summary": "...",
      "key_insights": ["...", "..."],
      "citations": [
        {{
          "claim": "...",
          "source_url": "...",
          "source_title": "...",
          "quote": "..."
        }}
      ],
      "priority": "HIGH",
      "relevance_reason": "...",
      "url": "original article URL",
      "source": "source domain"
    }}
  ]
}}

Remember:
- Every factual claim must have a citation
- Properly escape all special characters in JSON strings
- Test your JSON is valid before responding
"""

    # Generate content asynchronously
    import asyncio
    import json

    loop = asyncio.get_event_loop()
    response_text = await loop.run_in_executor(
        None,
        lambda: generate_content(prompt, WRITER_AGENT_INSTRUCTION)
    )

    # Extract JSON from response (may be wrapped in markdown code block)
    response_text = response_text.strip()
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.startswith("```"):
        response_text = response_text[3:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    # Try to parse JSON with better error handling
    try:
        report_data = json.loads(response_text)
    except json.JSONDecodeError as e:
        from config import setup_logger
        logger = setup_logger("WriterAgent")
        logger.error(f"JSON parsing failed: {e}")
        logger.error(f"Response preview (first 500 chars): {response_text[:500]}")
        logger.error(f"Response preview (last 500 chars): {response_text[-500:]}")

        # Try to find and extract valid JSON
        # Look for the outermost { } brackets
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')

        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_candidate = response_text[start_idx:end_idx + 1]
            try:
                report_data = json.loads(json_candidate)
                logger.info("Successfully recovered JSON after extraction")
            except json.JSONDecodeError:
                # If still failing, raise a more helpful error
                raise ValueError(
                    f"Writer Agent generated invalid JSON. Error at line {e.lineno}, column {e.colno}. "
                    f"This is a temporary LLM error - the verification loop will retry."
                ) from e
        else:
            raise ValueError(
                f"Writer Agent generated invalid JSON: {e}. "
                f"This is a temporary LLM error - the verification loop will retry."
            ) from e

    # Convert to NewsReport object
    articles = []
    topics_covered = set()
    skipped_articles = []

    for article_data in report_data.get("articles", []):
        citations = [
            Citation(**citation_data)
            for citation_data in article_data.get("citations", [])
        ]

        # Skip articles without citations - they violate our quality standards
        if not citations or len(citations) == 0:
            skipped_articles.append(article_data.get("title", "Unknown"))
            continue

        try:
            article = Article(
                title=article_data["title"],
                summary=article_data["summary"],
                key_insights=article_data["key_insights"],
                citations=citations,
                priority=Priority(article_data["priority"].lower()),
                relevance_reason=article_data["relevance_reason"],
                url=article_data["url"],
                source=article_data["source"],
            )

            articles.append(article)

            # Extract topics
            for topic in user_context.get('priority_topics', []):
                if topic.lower() in article.title.lower() or topic.lower() in article.summary.lower():
                    topics_covered.add(topic)

        except Exception as e:
            # Log and skip articles that fail validation
            from config import setup_logger
            logger = setup_logger("WriterAgent")
            logger.warning(f"Skipping article '{article_data.get('title', 'Unknown')}' due to validation error: {e}")
            skipped_articles.append(article_data.get("title", "Unknown"))
            continue

    # Log skipped articles if any
    if skipped_articles:
        from config import setup_logger
        logger = setup_logger("WriterAgent")
        logger.warning(f"Skipped {len(skipped_articles)} articles without citations: {', '.join(skipped_articles)}")

    # Ensure at least some articles made it through
    if not articles:
        raise ValueError(
            f"All {len(skipped_articles)} articles were rejected due to missing citations. "
            "The Writer Agent must produce articles with at least one citation each."
        )

    report = NewsReport(
        user_id=user_context.get('user_id', 'unknown'),
        report_date=datetime.utcnow(),
        executive_summary=report_data["executive_summary"],
        articles=articles,
        total_articles=len(articles),
        topics_covered=list(topics_covered),
        report_id=str(uuid.uuid4()),
    )

    return report
