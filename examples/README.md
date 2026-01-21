# Examples - NewsPulse AI

This folder contains example files to help you get started with NewsPulse AI.

## Files

### `example_profile.json`
Sample user profile showing the structure and fields. Use this as a reference when creating your own profiles.

**Key fields:**
- `user_id`: Unique identifier
- `topics_of_interest`: What news topics to track
- `role`, `company`, `industry`: For personalization
- `delivery_email`: Where to send reports
- `preferred_sources`: Trusted news outlets

## Usage Examples

### Example 1: Create a Profile and Generate Report

```python
from core.orchestrator import NewsPulseOrchestrator
import asyncio

async def main():
    orchestrator = NewsPulseOrchestrator()

    # Create profile
    profile = orchestrator.create_user_profile(
        user_id="tech_ceo",
        name="Jane Smith",
        role="CEO",
        company="TechStartup Inc",
        industry="Technology",
        topics_of_interest=["AI", "Cloud Computing", "Cybersecurity"],
        delivery_email="jane@techstartup.com"
    )

    # Generate report
    report = await orchestrator.generate_report("tech_ceo")
    print(f"Generated report with {report.total_articles} articles")

asyncio.run(main())
```

### Example 2: Generate Report Without Email

```python
from core.orchestrator import NewsPulseOrchestrator
import asyncio

async def main():
    orchestrator = NewsPulseOrchestrator()

    # Generate but don't send
    report = await orchestrator.generate_report(
        user_id="tech_ceo",
        deliver=False  # Don't send email
    )

    # Print to console instead
    print(f"\\n=== {report.executive_summary} ===\\n")

    for article in report.articles:
        print(f"- {article.title}")
        print(f"  {article.url}\\n")

asyncio.run(main())
```

### Example 3: Submit Feedback

```python
from core.orchestrator import NewsPulseOrchestrator
from agents.feedback_agent import collect_feedback
import asyncio

async def main():
    orchestrator = NewsPulseOrchestrator()

    # Collect feedback
    feedback = collect_feedback(
        report_id="report_123",
        user_id="tech_ceo",
        rating=5,
        feedback_text="Great report, very insightful!",
        liked_topics=["AI", "Cloud Computing"],
        missing_topics=["Quantum Computing"]
    )

    # Process feedback
    result = await orchestrator.process_feedback(feedback)
    print(f"Feedback processed: {result['summary']}")

asyncio.run(main())
```

### Example 4: Batch Generate for Multiple Users

```python
from core.orchestrator import NewsPulseOrchestrator
import asyncio

async def generate_for_user(orchestrator, user_id):
    try:
        report = await orchestrator.generate_report(user_id)
        return f"✓ {user_id}: {report.total_articles} articles"
    except Exception as e:
        return f"✗ {user_id}: {str(e)}"

async def main():
    orchestrator = NewsPulseOrchestrator()

    users = ["ceo_user", "cto_user", "cfo_user"]

    # Generate reports for all users
    tasks = [generate_for_user(orchestrator, uid) for uid in users]
    results = await asyncio.gather(*tasks)

    for result in results:
        print(result)

asyncio.run(main())
```

### Example 5: Custom Personalization

```python
from core.orchestrator import NewsPulseOrchestrator

orchestrator = NewsPulseOrchestrator()

# Create highly customized profile
profile = orchestrator.create_user_profile(
    user_id="finance_vp",
    name="John Doe",
    role="VP of Finance",
    company="Global Corp",
    industry="Financial Services",
    topics_of_interest=[
        "Fintech",
        "Cryptocurrency",
        "Banking Regulations",
        "Market Trends"
    ],
    excluded_topics=[
        "Celebrity News",
        "Sports"
    ],
    preferred_sources=[
        "bloomberg.com",
        "wsj.com",
        "ft.com"
    ],
    excluded_sources=[
        "tabloid-site.com"
    ],
    delivery_email="john.doe@globalcorp.com",
    delivery_time="07:00",  # 7 AM delivery
    timezone="America/New_York"
)

print(f"Profile created for {profile.name}")
```

## CLI Usage

### Create Profile
```bash
python main.py create-profile
```

### Generate Report
```bash
# With email delivery
python main.py generate tech_ceo

# Without email delivery
python main.py generate tech_ceo --no-deliver
```

### Submit Feedback
```bash
python main.py feedback report_123 tech_ceo 5
```

### List Profiles
```bash
python main.py list
```

## Tips

1. **Start Simple**: Create a basic profile first, then refine based on feedback
2. **Test Without Email**: Use `--no-deliver` to test report generation
3. **Iterate**: Use feedback to improve future reports
4. **Monitor Quotas**: Check Google API usage if running many reports

## Need More Help?

- [README.md](../README.md) - Full documentation
- [QUICKSTART.md](../QUICKSTART.md) - 5-minute setup guide
- [API_SETUP_GUIDE.md](../API_SETUP_GUIDE.md) - Detailed API configuration
