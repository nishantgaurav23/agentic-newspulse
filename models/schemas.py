"""
Pydantic models for strict I/O schemas between agents
Prevents "telephone game" errors where context is lost between agents
"""
from pydantic import BaseModel, Field, HttpUrl, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class Priority(str, Enum):
    """Priority levels for news topics"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class UserProfile(BaseModel):
    """User profile with personalized preferences"""

    user_id: str
    name: str
    role: str  # e.g., "CEO", "CTO", "VP of Marketing"
    company: str
    industry: str

    # Interests and preferences
    topics_of_interest: List[str] = Field(
        description="List of topics the user wants to track"
    )
    excluded_topics: List[str] = Field(
        default=[], description="Topics to exclude from reports"
    )
    preferred_sources: List[str] = Field(
        default=[], description="Preferred news sources"
    )
    excluded_sources: List[str] = Field(
        default=[], description="Sources to exclude"
    )

    # Delivery preferences
    delivery_email: str
    cc_emails: List[str] = Field(
        default=[], description="Additional recipients (CC)"
    )
    bcc_emails: List[str] = Field(
        default=[], description="Hidden recipients (BCC)"
    )
    delivery_time: str = "08:00"  # Time in HH:MM format
    timezone: str = "America/New_York"

    # Constraints learned from feedback
    constraints: Dict[str, Any] = Field(
        default={}, description="Learned constraints from user feedback"
    )

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SearchResult(BaseModel):
    """Result from search agent"""

    query: str
    url: str
    title: str
    snippet: str
    source: str
    published_date: Optional[str] = None
    relevance_score: Optional[float] = None


class FetchedContent(BaseModel):
    """Content fetched from a URL"""

    url: str
    title: str
    content: str  # Full HTML or extracted text
    author: Optional[str] = None
    published_date: Optional[str] = None
    source: str
    fetch_timestamp: datetime = Field(default_factory=datetime.utcnow)
    success: bool = True
    error_message: Optional[str] = None


class Citation(BaseModel):
    """Citation for a claim in the report"""

    claim: str
    source_url: str
    source_title: str
    quote: str  # Direct quote from source


class Article(BaseModel):
    """A single news article in the report"""

    title: str
    summary: str
    key_insights: List[str]
    citations: List[Citation] = Field(
        description="All citations must be included for verification"
    )
    priority: Priority
    relevance_reason: str  # Why this is relevant to the user
    url: str
    source: str
    published_date: Optional[str] = None

    @validator("citations")
    def validate_citations(cls, v):
        """Ensure at least one citation exists"""
        if not v or len(v) == 0:
            raise ValueError("Article must have at least one citation")
        return v


class NewsReport(BaseModel):
    """Complete news report for a user"""

    user_id: str
    report_date: datetime = Field(default_factory=datetime.utcnow)
    executive_summary: str  # High-level overview
    articles: List[Article]
    total_articles: int
    topics_covered: List[str]

    # Metadata
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    report_id: str

    @validator("articles")
    def validate_articles_not_empty(cls, v):
        """Ensure report has articles"""
        if not v or len(v) == 0:
            raise ValueError("Report must contain at least one article")
        return v


class VerificationResult(BaseModel):
    """Result from verification agent"""

    article_title: str
    is_verified: bool
    issues_found: List[str] = Field(
        default=[], description="List of verification issues"
    )
    missing_citations: List[str] = Field(
        default=[], description="Claims without citations"
    )
    feedback: str  # Feedback for the writer agent
    retry_suggested: bool = False


class FeedbackData(BaseModel):
    """User feedback on a report"""

    report_id: str
    user_id: str
    rating: int = Field(ge=1, le=5, description="1-5 star rating")
    feedback_text: Optional[str] = None
    liked_topics: List[str] = Field(default=[])
    disliked_topics: List[str] = Field(default=[])
    too_long: bool = False
    too_short: bool = False
    missing_topics: List[str] = Field(default=[])
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HistoricalRecommendation(BaseModel):
    """Recommendation from historical analysis"""

    recommended_topics: List[str]
    exclude_urls: List[str] = Field(
        description="URLs already seen by the user"
    )
    insights: str  # What we learned from history
