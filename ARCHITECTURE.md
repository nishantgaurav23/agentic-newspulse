# 🏗️ NewsPulse AI - System Architecture

Comprehensive technical documentation of the NewsPulse AI multi-agent system.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Multi-Agent Architecture](#multi-agent-architecture)
3. [5-Phase Workflow](#5-phase-workflow)
4. [Data Flow](#data-flow)
5. [Component Details](#component-details)
6. [Self-Correction Loop](#self-correction-loop)
7. [Deployment Architecture](#deployment-architecture)

---

## System Overview

NewsPulse AI is a **self-correcting multi-agent system** that delivers personalized, citation-backed news reports. The system combines 8 specialized AI agents with quality gates to prevent hallucinations and ensure factual accuracy.

### Design Principles

1. **Separation of Concerns** - Each agent has a single, well-defined responsibility
2. **Grounded Truth** - Fetch actual content, not just search snippets
3. **Quality Gates** - Verification loop ensures citations before delivery
4. **Personalization** - All decisions based on user context
5. **Continuous Learning** - Feedback loop improves future reports

---

## Multi-Agent Architecture

### High-Level Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        NEWSPULSE AI                             │
│                  Multi-Agent News Analyst                       │
└────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
         ┌────▼────┐                     ┌────▼────┐
         │ CLI/API │                     │ Agents  │
         │ Layer   │                     │  (8×)   │
         └────┬────┘                     └────┬────┘
              │                               │
              │        ┌──────────────────────┘
              │        │
         ┌────▼────────▼────┐
         │  Orchestrator    │
         │  (Coordinator)   │
         └────┬────────┬────┘
              │        │
    ┌─────────┴─┐   ┌─┴─────────┐
    │   Core    │   │  Tools    │
    │  Engine   │   │  (I/O)    │
    └─────┬─────┘   └─────┬─────┘
          │               │
    ┌─────▼─────┐   ┌─────▼─────┐
    │  Models   │   │  Config   │
    │ (Schemas) │   │(Settings) │
    └───────────┘   └───────────┘
```

### Component Layers

| Layer | Components | Responsibility |
|-------|------------|----------------|
| **Interface** | CLI, API | User interaction |
| **Orchestration** | Orchestrator | Coordinates agent execution |
| **Agents** | 8 AI Agents | Specialized intelligence |
| **Core** | Loop Agent, Utils | Verification loop, API wrapper |
| **Tools** | Search, Scraper, Email | External I/O operations |
| **Models** | Pydantic Schemas | Data validation |
| **Config** | Settings, Logger | Configuration management |

---

## 5-Phase Workflow

### Complete Flow Diagram

```
┌───────────────────────────────────────────────────────────────┐
│                     PHASE 1: Planning                         │
│                   Contextual Preparation                       │
└───────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
       ┌────▼──────┐    ┌────▼──────┐    ┌────▼──────┐
       │  Profile  │    │Historical │    │ Planning  │
       │   Agent   │    │Recommender│    │  Logic    │
       └────┬──────┘    └────┬──────┘    └────┬──────┘
            │                │                 │
            └────────────────┼─────────────────┘
                             │
                    ┌────────▼────────┐
                    │  User Context   │
                    │  & Constraints  │
                    └────────┬────────┘
                             │
┌───────────────────────────────────────────────────────────────┐
│                    PHASE 2: Research                          │
│                  Grounded Information Gathering                │
└───────────────────────────────────────────────────────────────┘
                             │
            ┌────────────────┼────────────────┐
            │                                 │
       ┌────▼──────┐                    ┌────▼──────┐
       │  Search   │                    │   Fetch   │
       │   Agent   │───────────────────▶│   Agent   │
       └────┬──────┘                    └────┬──────┘
            │                                 │
    ┌───────▼────────┐             ┌─────────▼────────┐
    │ Google Custom  │             │  Web Scraping    │
    │    Search      │             │ (BeautifulSoup)  │
    └───────┬────────┘             └─────────┬────────┘
            │                                 │
       Search Results              Full Article Content
            │                                 │
            └────────────────┬────────────────┘
                             │
                    ┌────────▼────────┐
                    │ Processed       │
                    │ Articles (10+)  │
                    └────────┬────────┘
                             │
┌───────────────────────────────────────────────────────────────┐
│                   PHASE 3: Verification                       │
│              Self-Correcting Quality Gate                     │
└───────────────────────────────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │ Verification    │
                    │     Loop        │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                                 │
       ┌────▼──────┐                    ┌────▼────────┐
       │  Writer   │◀───── Retry ───────│Verification │
       │   Agent   │                    │    Agent    │
       └────┬──────┘                    └────┬────────┘
            │                                 │
     Draft Report                       Audit Quality
            │                                 │
            │                            Approved?
            │                                 │
            │                        ┌────────┴────────┐
            │                        │                 │
            │                       Yes               No
            │                        │                 │
            └────────────────────────┘             Retry (2×)
                             │
                    ┌────────▼────────┐
                    │  Verified       │
                    │  Report         │
                    └────────┬────────┘
                             │
┌───────────────────────────────────────────────────────────────┐
│                    PHASE 4: Dispatch                          │
│                     Report Delivery                            │
└───────────────────────────────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   Dispatch      │
                    │    Agent        │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
       ┌────▼──────┐    ┌────▼──────┐   ┌────▼──────┐
       │   Email   │    │   Save    │   │   Log     │
       │ (To/CC/   │    │   to      │   │ Delivery  │
       │   BCC)    │    │ History   │   │  Status   │
       └───────────┘    └───────────┘   └───────────┘
                             │
┌───────────────────────────────────────────────────────────────┐
│                    PHASE 5: Feedback                          │
│                  Continuous Learning                           │
└───────────────────────────────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   Feedback      │
                    │    Agent        │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
       ┌────▼──────┐    ┌────▼──────┐   ┌────▼──────┐
       │  Collect  │    │  Analyze  │   │  Update   │
       │  Rating   │    │ Sentiment │   │  Profile  │
       └───────────┘    └───────────┘   └───────────┘
```

### Phase Details

#### Phase 1: Contextual Planning (5-10 seconds)

**Agents Involved:**
- Profile Agent
- Historical Recommender Agent

**Process:**
1. Load user profile (role, company, topics, preferences)
2. Check history to identify already-delivered URLs
3. Generate personalized search strategy
4. Build context for downstream agents

**Output:** User context dictionary with:
- Priority topics
- Excluded topics/sources
- Historical URLs to avoid
- Delivery preferences

#### Phase 2: Grounded Research (60-90 seconds)

**Agents Involved:**
- Search Agent
- Fetch Agent

**Process:**
1. **Search Agent**:
   - Constructs queries from user topics
   - Calls Google Custom Search API
   - Returns 10-20 article URLs

2. **Fetch Agent**:
   - Scrapes actual HTML from each URL
   - Parses content with BeautifulSoup
   - Uses AI to extract key facts and quotes
   - Validates content quality

**Output:** List of processed articles with:
- Full content
- Extracted facts
- Direct quotes
- Source metadata

#### Phase 3: Verification Loop (60-120 seconds)

**Agents Involved:**
- Writer Agent
- Verification Agent
- Loop Agent (coordinator)

**Process:**
1. **Writer Agent** drafts report with citations
2. **Verification Agent** audits:
   - Every claim has a citation
   - Quotes match sources
   - Sources are credible
   - No speculation or unsupported assertions
3. If rejected, retry with feedback (max 2-3 times)
4. If all retries fail, mark as unverified but deliver with warning

**Output:** Verified NewsReport or unverified report with warnings

#### Phase 4: Dispatch (2-5 seconds)

**Agents Involved:**
- Dispatch Agent

**Process:**
1. Format report as HTML email
2. Send to primary recipient (To)
3. Send to CC recipients (visible)
4. Send to BCC recipients (hidden)
5. Save to history for deduplication
6. Log delivery status

**Output:** Delivery confirmation with report ID

#### Phase 5: Feedback (when provided)

**Agents Involved:**
- Feedback Agent

**Process:**
1. Collect user rating (1-5 stars)
2. Analyze feedback comments
3. Update profile constraints
4. Adjust future report generation

**Output:** Updated user profile with learned preferences

---

## Data Flow

### Complete Data Flow Diagram

```
┌──────────────┐
│ User Profile │
│   (JSON)     │
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│  Profile     │────▶│  Historical  │
│   Agent      │     │ Recommender  │
└──────┬───────┘     └──────┬───────┘
       │                    │
       └────────┬───────────┘
                │
         ┌──────▼───────┐
         │ User Context │
         │   + History  │
         └──────┬───────┘
                │
                ▼
       ┌────────────────┐
       │ Search Agent   │
       │  (Topics →     │
       │   Queries)     │
       └────────┬───────┘
                │
                ▼
       ┌────────────────┐
       │ Google Custom  │
       │ Search API     │
       └────────┬───────┘
                │
         Search Results
                │
                ▼
       ┌────────────────┐
       │  Fetch Agent   │
       │ (URLs → HTML)  │
       └────────┬───────┘
                │
                ▼
       ┌────────────────┐
       │ Web Scraping   │
       │ (HTML → Text)  │
       └────────┬───────┘
                │
          Full Articles
                │
                ▼
       ┌────────────────┐
       │ Writer Agent   │
       │ (Articles →    │
       │  Draft Report) │
       └────────┬───────┘
                │
                ▼
       ┌────────────────────┐
       │ Verification Agent │
       │  (Audit Quality)   │
       └────────┬───────────┘
                │
           Approved?
                │
         ┌──────┴──────┐
         │             │
        Yes           No
         │             │
         │      ┌──────▼───────┐
         │      │ Retry Loop   │
         │      │  (Max 2-3×)  │
         │      └──────┬───────┘
         │             │
         └──────┬──────┘
                │
        Verified Report
                │
                ▼
       ┌────────────────┐
       │ Dispatch Agent │
       │ (Report →      │
       │  Email)        │
       └────────┬───────┘
                │
                ▼
       ┌────────────────┐     ┌────────────────┐
       │  SMTP Server   │     │  Save History  │
       │ (Gmail/Other)  │     │     (JSON)     │
       └────────┬───────┘     └────────┬───────┘
                │                      │
         Delivered Email        Updated History
                │                      │
                └──────────┬───────────┘
                           │
                    Report Complete
```

### Data Models

#### UserProfile
```python
{
  "user_id": "string",
  "name": "string",
  "role": "string",
  "company": "string",
  "industry": "string",
  "topics_of_interest": ["string"],
  "excluded_topics": ["string"],
  "preferred_sources": ["string"],
  "excluded_sources": ["string"],
  "delivery_email": "string",
  "cc_emails": ["string"],
  "bcc_emails": ["string"],
  "delivery_time": "HH:MM",
  "timezone": "string",
  "constraints": {}
}
```

#### NewsReport
```python
{
  "user_id": "string",
  "report_date": "datetime",
  "executive_summary": "string",
  "articles": [Article],
  "total_articles": int,
  "topics_covered": ["string"],
  "report_id": "uuid"
}
```

#### Article
```python
{
  "title": "string",
  "summary": "string",
  "key_insights": ["string"],
  "citations": [Citation],
  "priority": "critical|high|medium|low",
  "relevance_reason": "string",
  "url": "string",
  "source": "string"
}
```

#### Citation
```python
{
  "claim": "string",
  "source_url": "string",
  "source_title": "string",
  "quote": "string"
}
```

---

## Component Details

### 1. Orchestrator

**Location:** `core/orchestrator.py`

**Responsibilities:**
- Coordinates all agents
- Manages phase transitions
- Handles errors gracefully
- Provides unified API

**Key Methods:**
```python
async def generate_report(user_id: str, deliver: bool) -> NewsReport
def create_user_profile(...) -> UserProfile
def list_profiles() -> List[str]
```

### 2. Profile Agent

**Location:** `agents/profile_agent.py`

**Responsibilities:**
- Load user profile from disk
- Analyze user context
- Identify priority topics
- Build personalization strategy

**Input:** User ID
**Output:** User context dictionary

### 3. Historical Recommender Agent

**Location:** `agents/historical_recommender_agent.py`

**Responsibilities:**
- Load previous reports
- Extract delivered URLs
- Prevent duplicate content
- Suggest fresh topics

**Input:** User ID
**Output:** List of URLs to exclude

### 4. Search Agent

**Location:** `agents/search_agent.py`

**Responsibilities:**
- Build search queries from topics
- Call Google Custom Search API
- Rank results by relevance
- Return top 10-20 URLs

**Input:** User context, topics
**Output:** List of SearchResult objects

### 5. Fetch Agent

**Location:** `agents/fetch_agent.py`

**Responsibilities:**
- Scrape HTML from URLs
- Parse content with BeautifulSoup
- Extract text and metadata
- Use AI to identify key facts

**Input:** List of URLs
**Output:** List of processed articles

### 6. Writer Agent

**Location:** `agents/writer_agent.py`

**Responsibilities:**
- Draft executive summary
- Create article summaries
- Generate key insights
- **Mandatory:** Cite every claim

**Input:** Processed articles, user context
**Output:** Draft NewsReport

**Critical Requirement:** Every article must have at least 1 citation

### 7. Verification Agent

**Location:** `agents/verification_agent.py`

**Responsibilities:**
- Audit report quality
- Check all citations present
- Verify quotes match sources
- Assess source credibility
- Provide feedback for retries

**Input:** Draft NewsReport
**Output:** Approval decision + feedback

**Quality Standards:**
- Critical facts must have citations
- Quotes must be direct and accurate
- Sources must be credible
- No speculation without citations

### 8. Dispatch Agent

**Location:** `agents/dispatch_agent.py`

**Responsibilities:**
- Format report as HTML
- Send via SMTP
- Support To, CC, BCC
- Save to history
- Log delivery status

**Input:** Verified NewsReport, UserProfile
**Output:** Delivery status

### 9. Feedback Agent

**Location:** `agents/feedback_agent.py`

**Responsibilities:**
- Collect user ratings
- Analyze feedback comments
- Update profile constraints
- Improve future reports

**Input:** Report ID, rating, comments
**Output:** Updated profile

---

## Self-Correction Loop

### Detailed Loop Diagram

```
┌─────────────────────────────────────────────────────────────┐
│              VERIFICATION LOOP (LoopAgent)                  │
└─────────────────────────────────────────────────────────────┘
                           │
                  Attempt 1/3
                           │
                           ▼
              ┌────────────────────────┐
              │    Writer Agent        │
              │  • Draft Summary       │
              │  • Create Articles     │
              │  • Add Citations       │
              └───────────┬────────────┘
                          │
                   Draft Report
                          │
                          ▼
              ┌────────────────────────┐
              │  Verification Agent    │
              │  • Check Citations     │
              │  • Verify Quotes       │
              │  • Assess Sources      │
              └───────────┬────────────┘
                          │
                     Verdict?
                          │
         ┌────────────────┼────────────────┐
         │                │                │
        ✓               ✗               ✗
     Approved        Issues          Critical
         │            Found           Failure
         │                │                │
         │                ▼                │
         │    ┌───────────────────┐        │
         │    │  Generate         │        │
         │    │  Feedback:        │        │
         │    │  • Missing cites  │        │
         │    │  • Bad quotes     │        │
         │    │  • Weak sources   │        │
         │    └───────┬───────────┘        │
         │            │                    │
         │      Attempt 2/3                │
         │            │                    │
         │            ▼                    │
         │    ┌───────────────────┐        │
         │    │  Writer Agent     │        │
         │    │  (with feedback)  │        │
         │    └───────┬───────────┘        │
         │            │                    │
         │       Better Draft              │
         │            │                    │
         │            ▼                    │
         │    ┌───────────────────┐        │
         │    │ Verification      │        │
         │    │   Again           │        │
         │    └───────┬───────────┘        │
         │            │                    │
         │       Still Issues?             │
         │            │                    │
         │      ┌─────┴─────┐              │
         │      │           │              │
         │     Yes         No              │
         │      │           │              │
         │  Attempt 3/3    ✓               │
         │      │       Approved            │
         │      │           │              │
         │      ▼           │              │
         │ ┌───────────┐   │              │
         │ │Max Retries│   │              │
         │ │ Reached   │   │              │
         │ └─────┬─────┘   │              │
         │       │         │              │
         │  Unverified     │              │
         │   Warning       │              │
         │       │         │              │
         └───────┼─────────┴──────────────┘
                 │
            Deliver Report
          (Verified or with Warning)
```

### Loop Logic

**File:** `core/loop_agent.py`

```python
class VerificationLoop:
    max_retries: int = 2  # Configurable

    async def run(self):
        for attempt in range(1, self.max_retries + 1):
            # Draft report
            report = await writer_agent.run(...)

            # Verify quality
            verification = await verification_agent.run(report)

            if verification.approved:
                return report, True  # Verified

            # Generate feedback
            feedback = verification.feedback

            if attempt == self.max_retries:
                # Max retries reached
                return report, False  # Unverified

            # Retry with feedback
            writer_agent.apply_feedback(feedback)

        return report, False  # Failed verification
```

---

## Deployment Architecture

### Local Development

```
┌─────────────┐
│   Developer │
│    Machine  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Python    │
│    3.11+    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Virtual Env │
│   (venv)    │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐
│  NewsPulse  │────▶│ Google APIs │
│     AI      │     │ (Gemini +   │
└──────┬──────┘     │  Search)    │
       │            └─────────────┘
       ▼
┌─────────────┐
│    SMTP     │
│   Server    │
└─────────────┘
```

### Production (Google Cloud Run)

```
┌─────────────────────────────────────────────────────┐
│              Google Cloud Platform                   │
│                                                      │
│  ┌────────────────┐      ┌──────────────────┐      │
│  │ Cloud Scheduler│─────▶│   Cloud Run      │      │
│  │  (Cron Jobs)   │      │   (Container)    │      │
│  └────────────────┘      └─────────┬────────┘      │
│                                    │               │
│  ┌────────────────┐                │               │
│  │ Secret Manager │◀───────────────┘               │
│  │  (API Keys)    │                                │
│  └────────────────┘                                │
│                                                     │
│  ┌────────────────┐                                │
│  │  Artifact      │                                │
│  │  Registry      │                                │
│  │ (Docker Images)│                                │
│  └────────────────┘                                │
└─────────────────────────────────────────────────────┘
          │                        │
          │                        ▼
          │             ┌────────────────┐
          │             │ Google Gemini  │
          │             │      API       │
          │             └────────────────┘
          │
          ▼
┌────────────────┐
│  Gmail SMTP    │
│   (Delivery)   │
└────────────────┘
```

### Container Architecture

```
┌─────────────────────────────────────────┐
│         Docker Container                 │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │     Python 3.11 Base Image         │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │     Application Code               │ │
│  │  • agents/                         │ │
│  │  • core/                           │ │
│  │  • models/                         │ │
│  │  • tools/                          │ │
│  │  • config/                         │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │     Data Volumes                   │ │
│  │  • /app/data/user_profiles/        │ │
│  │  • /app/data/history/              │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │     Environment Variables          │ │
│  │  • GOOGLE_API_KEY (from Secrets)   │ │
│  │  • SMTP_PASSWORD (from Secrets)    │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

## Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Runtime** | Python 3.11+ | Main language |
| **AI Model** | Google Gemini 2.5 Flash | LLM for agents |
| **Data Validation** | Pydantic | Schema validation |
| **Web Scraping** | BeautifulSoup4 | HTML parsing |
| **HTTP** | httpx | Async HTTP client |
| **Search** | Google Custom Search API | News discovery |
| **Email** | smtplib | SMTP delivery |
| **Logging** | Python logging | Structured logs |
| **Config** | pydantic-settings | Environment config |

### Cloud Infrastructure

| Service | Purpose |
|---------|---------|
| **Cloud Run** | Serverless container hosting |
| **Artifact Registry** | Docker image storage |
| **Secret Manager** | API key management |
| **Cloud Scheduler** | Cron job automation |
| **Cloud Logging** | Centralized logging |

---

## Performance Characteristics

### Execution Time

| Phase | Time Range | Factors |
|-------|------------|---------|
| Phase 1 (Planning) | 5-10s | Profile loading, history check |
| Phase 2 (Research) | 60-90s | Number of articles, network speed |
| Phase 3 (Verification) | 60-120s | Retry count, citation quality |
| Phase 4 (Dispatch) | 2-5s | Email size, SMTP latency |
| Phase 5 (Feedback) | 1-3s | Profile update complexity |
| **Total** | **3-5 min** | End-to-end report generation |

### Resource Usage

| Resource | Local | Cloud Run |
|----------|-------|-----------|
| **Memory** | ~200-500 MB | 1 GB allocated |
| **CPU** | 1 core | 1 vCPU allocated |
| **Network** | ~10-50 MB/report | Same |
| **Storage** | ~1 MB/report (history) | Same |

### API Quotas

| Service | Free Tier | Rate Limit |
|---------|-----------|------------|
| **Gemini API** | 50 req/day | 10-15 req/min |
| **Custom Search** | 100 queries/day | 1 query/sec |
| **Gmail SMTP** | 100-500/day | ~100/hour |

---

## Security Considerations

### API Key Management

```
Production:
  └─ Google Secret Manager
      ├─ GOOGLE_API_KEY
      ├─ GOOGLE_SEARCH_API_KEY
      ├─ GOOGLE_SEARCH_ENGINE_ID
      └─ SMTP_PASSWORD

Development:
  └─ .env file (git-ignored)
      ├─ GOOGLE_API_KEY=...
      ├─ SMTP_PASSWORD=...
      └─ ...
```

### Data Privacy

- **User Profiles**: Stored locally or in Cloud Run volumes
- **Report History**: JSON files, not sent to external services
- **Email Content**: Encrypted in transit (TLS/STARTTLS)
- **API Keys**: Never logged or exposed

### Best Practices

1. ✅ Use Secret Manager for production
2. ✅ Rotate API keys periodically
3. ✅ Use service accounts (not user credentials)
4. ✅ Least privilege IAM permissions
5. ✅ Monitor for suspicious activity
6. ✅ Enable audit logging

---

## Monitoring and Observability

### Logging

**Structured Logging:**
```python
logger.info(
    "Phase completed",
    extra={
        "agent": "SearchAgent",
        "phase": "2",
        "user_id": "nishantgaurav23",
        "articles_found": 15
    }
)
```

**Log Levels:**
- `DEBUG`: Detailed execution traces
- `INFO`: Phase transitions, agent runs
- `WARNING`: Verification failures, retries
- `ERROR`: API errors, delivery failures

### Metrics

Key metrics to track:
- Report generation time
- Verification success rate
- Article fetch success rate
- Email delivery rate
- User satisfaction (feedback ratings)

---

## Future Enhancements

### Planned Improvements

1. **Web UI** - Profile management interface
2. **Multi-Language** - Support for non-English news
3. **Real-Time Alerts** - Breaking news notifications
4. **Audio Summaries** - Text-to-speech reports
5. **Mobile Apps** - iOS/Android clients
6. **Advanced Analytics** - Sentiment analysis, trend detection
7. **Team Collaboration** - Shared profiles, team digests
8. **Custom Integrations** - Slack, Teams, Discord bots

---

<div align="center">

**Built with ❤️ for intelligent news consumption**

[Back to README](README.md) | [GCP Deployment](GCP_DEPLOYMENT_GUIDE.md) | [Email Setup](EMAIL_SETUP_GUIDE.md)

</div>
