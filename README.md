# 📰 NewsPulse AI

<div align="center">

**Self-Correcting Multi-Agent News Analyst**

*Personalized, Citation-Backed News Reports Powered by Google Gemini*

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4)](https://ai.google.dev/)

</div>

---

## 🌟 What is NewsPulse AI?

NewsPulse AI is an **intelligent news analyst** that automatically finds, verifies, and delivers personalized news reports tailored to your professional interests. Unlike simple news aggregators, NewsPulse AI:

✅ **Prevents Hallucinations** - Scrapes actual article content, not just search snippets

✅ **Quality Gates** - Self-correcting verification loop ensures citations

✅ **Personalization** - Tailored to your role, industry, and topics

✅ **Continuous Learning** - Improves from your feedback

✅ **Transparency** - Shows sources and handles verification failures gracefully

✅ **Deduplication** - Never sends the same news twice

---

## 🎯 Key Features

### 🤖 Multi-Agent Architecture
8 specialized AI agents working together:
- **Profile Agent** - Loads user context and preferences
- **Historical Recommender** - Prevents duplicate content
- **Search Agent** - Finds relevant news articles
- **Fetch Agent** - Scrapes full article content
- **Writer Agent** - Drafts reports with citations
- **Verification Agent** - Audits quality and citations
- **Dispatch Agent** - Delivers via email
- **Feedback Agent** - Learns from your ratings

### 🔄 5-Phase Workflow
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Phase 1   │───▶│   Phase 2   │───▶│   Phase 3   │
│  Planning   │    │  Research   │    │Verification │
│   Context   │    │  Grounded   │    │    Loop     │
└─────────────┘    └─────────────┘    └──────┬──────┘
                                              │
┌─────────────┐    ┌─────────────┐           │
│   Phase 5   │◀───│   Phase 4   │◀──────────┘
│  Feedback   │    │  Dispatch   │
│   Learning  │    │   Delivery  │
└─────────────┘    └─────────────┘
```

### 📊 Self-Correction Loop
```
     ┌──────────────┐
     │ Writer Agent │
     │  Drafts      │
     │  Report      │
     └──────┬───────┘
            │
            ▼
  ┌────────────────────┐
  │ Verification Agent │     ✗ Issues Found
  │   Audits Quality   │────────────┐
  └────────┬───────────┘            │
           │ ✓ Approved             │
           │                        │
           ▼                        ▼
    ┌──────────┐            ┌──────────────┐
    │ Deliver  │            │   Retry      │
    │  Report  │            │ (Max 2-3×)   │
    └──────────┘            └──────┬───────┘
                                   │
                                   └──────┐
                                          │
                          Better Draft ───┘
```

---

## 📸 Example Report

### Executive Summary
```
The evolving landscape of Artificial Intelligence and Data Science
continues to drive demand for highly skilled professionals and robust
strategic frameworks. Recent developments highlight:

• Educational institutions offering advanced programs
• Industry methodologies for AI project validation
• Growing emphasis on responsible AI implementation
```

### Sample Article
```
┌──────────────────────────────────────────────────────────┐
│ 🔴 HIGH PRIORITY                                         │
│                                                          │
│ MIT IDSS Program Addresses Practical and Responsible    │
│ AI Skills for Business Impact                           │
│                                                          │
│ Why this matters: Critical professional development     │
│ opportunities in responsible AI directly aligning with   │
│ your role as a Data Scientist.                          │
│                                                          │
│ Key Insights:                                           │
│ • Investigate programs offering practical AI skills     │
│ • Prioritize learning with official certifications      │
│ • Focus on ethical AI implementation                    │
│ • Explore Generative AI masterclasses                   │
│                                                          │
│ Sources (4 citations):                                  │
│ [1] "The 12-week program covers deep learning..."       │
│     - MIT IDSS Curriculum Guide                         │
│                                                          │
│ [2] "Participants receive an MIT IDSS Certificate..."   │
│     - Great Learning                                    │
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-newspulse.git
cd agentic-newspulse

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file:

```env
# Google Gemini API
GOOGLE_API_KEY=your_google_api_key

# Google Custom Search API
GOOGLE_SEARCH_API_KEY=your_search_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your_app_password

# Application Settings
MAX_ARTICLES_PER_REPORT=5
VERIFICATION_MAX_RETRIES=2
GEMINI_MODEL=models/gemini-2.5-flash
```

**Get API Keys:**
- [Google AI Studio](https://aistudio.google.com/) - Get GOOGLE_API_KEY
- [Google Custom Search](https://developers.google.com/custom-search) - Get Search API
- [Gmail App Password](https://myaccount.google.com/apppasswords) - Get SMTP password

See [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md) for detailed email configuration.

### 3. Create Your Profile

```bash
# Interactive profile creation
python create_profile_interactive.py

# Or use the template
python create_my_profile.py
```

### 4. Generate Your First Report

```bash
# Test without email delivery
python main.py generate your_user_id --no-deliver

# Generate and send via email
python main.py generate your_user_id
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture and flow diagrams |
| [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md) | Email service setup and multi-recipient support |
| [GCP_DEPLOYMENT_GUIDE.md](GCP_DEPLOYMENT_GUIDE.md) | Deploy to Google Cloud Platform |
| [SETUP_COMPLETE.md](SETUP_COMPLETE.md) | Initial setup completion guide |

---

## 🎮 Usage

### Generate Reports

```bash
# Generate test report (no email)
python main.py generate nishantgaurav23 --no-deliver

# Generate and deliver via email
python main.py generate nishantgaurav23

# List all profiles
python main.py list

# Submit feedback
python main.py feedback <report_id> <user_id> <rating>
```

### Manage Profiles

```bash
# Create new profile (interactive)
python create_profile_interactive.py

# Create from template
python create_my_profile.py

# View profile
cat data/user_profiles/nishantgaurav23.json
```

### Multi-Email Support

Edit your profile to add CC and BCC recipients:

```json
{
  "user_id": "nishantgaurav23",
  "delivery_email": "primary.user@gmail.com",
  "cc_emails": [
    "manager@company.com",
    "team-lead@company.com"
  ],
  "bcc_emails": [
    "archive@company.com"
  ]
}
```

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    NEWSPULSE AI                         │
└─────────────────────────────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    ┌────▼────┐     ┌────▼────┐     ┌────▼────┐
    │ Agents  │     │  Core   │     │  Tools  │
    │ (8×AI)  │     │ Engine  │     │ (I/O)   │
    └────┬────┘     └────┬────┘     └────┬────┘
         │               │                │
         └───────────────┼────────────────┘
                         │
            ┌────────────▼────────────┐
            │                         │
       ┌────▼────┐            ┌──────▼──────┐
       │ Models  │            │   Config    │
       │(Schemas)│            │ (Settings)  │
       └─────────┘            └─────────────┘
```

For detailed architecture diagrams, see [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🔧 Configuration

### Model Configuration

```python
# config/settings.py
gemini_model: str = "models/gemini-2.5-flash"  # Stable, good rate limits
temperature: float = 0.7                        # Creativity level
max_tokens: int = 8192                          # Response length
```

### Verification Settings

```python
# .env
VERIFICATION_MAX_RETRIES=2  # Number of retry attempts
MAX_ARTICLES_PER_REPORT=5   # Articles per report (5-15)
```

### Email Settings

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
```

---

## 🐳 Docker Deployment

### Build and Run Locally

```bash
# Build image
docker build -t newspulse-ai:latest .

# Run container
docker run -it --rm \
    --env-file .env \
    -v $(pwd)/data:/app/data \
    newspulse-ai:latest \
    python main.py generate nishantgaurav23
```

### Deploy to Google Cloud Run

See [GCP_DEPLOYMENT_GUIDE.md](GCP_DEPLOYMENT_GUIDE.md) for complete instructions.

```bash
# Quick deploy
gcloud run deploy newspulse-service \
    --image gcr.io/your-project/newspulse-ai:latest \
    --region us-central1 \
    --set-secrets=GOOGLE_API_KEY=google-api-key:latest
```

---

## 📊 Project Structure

```
agentic-newspulse/
├── agents/                    # 8 AI agents
│   ├── profile_agent.py       # Phase 1: User context
│   ├── historical_recommender_agent.py  # Deduplication
│   ├── search_agent.py        # Phase 2: Find news
│   ├── fetch_agent.py         # Scrape content
│   ├── writer_agent.py        # Phase 3: Draft reports
│   ├── verification_agent.py  # Quality gate
│   ├── dispatch_agent.py      # Phase 4: Deliver
│   └── feedback_agent.py      # Phase 5: Learn
│
├── config/                    # Configuration
│   ├── settings.py            # Application settings
│   └── logger_config.py       # Structured logging
│
├── core/                      # Core engine
│   ├── orchestrator.py        # Main coordinator
│   ├── loop_agent.py          # Verification loop
│   └── utils.py               # Gemini API wrapper
│
├── models/                    # Data schemas
│   ├── schemas.py             # Pydantic models
│   └── user_profile.py        # Profile manager
│
├── tools/                     # I/O tools
│   ├── search_tool.py         # Google Custom Search
│   ├── scraper_tool.py        # Web scraping
│   └── email_tool.py          # SMTP delivery
│
├── data/                      # User data
│   ├── user_profiles/         # Profiles (JSON)
│   └── history/               # Report history
│
├── main.py                    # CLI entry point
├── create_profile_interactive.py  # Profile creator
├── Dockerfile                 # Container image
├── requirements.txt           # Python dependencies
└── .env                       # Environment variables
```

---

## ⚙️ System Capabilities

### ✅ What NewsPulse AI Does Well

1. **Prevents Hallucinations** - Forces real content scraping, not search snippets
2. **Quality Gates** - Verification loop ensures citations
3. **Personalization** - Tailored to your role, industry, topics
4. **Continuous Learning** - Improves from feedback
5. **Transparency** - Shows when verification fails
6. **Deduplication** - Never sends same news twice
7. **Multi-Recipient** - Supports To, CC, and BCC emails

### ⚠️ Current Limitations

1. **Rate Limits** - Gemini API has quotas (10-15 req/min for free tier)
2. **Processing Time** - Takes 3-5 minutes per report
3. **Source Availability** - Some websites block scrapers
4. **Verification Strictness** - May reject "good enough" reports

---

## 🛠️ Advanced Features

### Multi-Email Support

Send reports to multiple recipients:

```json
{
  "delivery_email": "primary@example.com",
  "cc_emails": ["manager@example.com", "team@example.com"],
  "bcc_emails": ["archive@example.com"]
}
```

### Automated Scheduling

Use cron jobs or Cloud Scheduler:

```bash
# crontab entry (daily at 8 AM)
0 8 * * * cd /path/to/agentic-newspulse && ./venv/bin/python main.py generate nishantgaurav23
```

### Custom Topics

Edit your profile to track specific topics:

```json
{
  "topics_of_interest": [
    "Artificial Intelligence",
    "Machine Learning",
    "Cloud Computing",
    "Python",
    "React"
  ],
  "excluded_topics": [
    "Celebrity News",
    "Sports"
  ]
}
```

---

## 🧪 Testing

```bash
# Validate configuration
python test_setup.py

# Generate test report (no email)
python main.py generate your_user_id --no-deliver

# Check logs
tail -f logs/newspulse.log
```

---

## 📈 Roadmap

### Short Term
- [ ] Web UI for profile management
- [ ] Multiple language support
- [ ] Slack/Teams integration
- [ ] RSS feed support

### Long Term
- [ ] Audio/podcast summaries
- [ ] Interactive feedback widgets
- [ ] Mobile app (iOS/Android)
- [ ] Real-time alerts for breaking news
- [ ] Multi-tenant SaaS platform

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **Google Gemini** for powerful LLM capabilities
- **Google Custom Search** for news discovery
- **BeautifulSoup** for web scraping
- **Pydantic** for data validation

---

## 📞 Support

- **Documentation**: See docs in this repository
- **Issues**: File an issue on GitHub
- **Email**: Check SETUP_COMPLETE.md for contact info

---

<div align="center">

**Built with ❤️ using Google Gemini 2.5 Flash**

Made by Nishant Gaurav

</div>
