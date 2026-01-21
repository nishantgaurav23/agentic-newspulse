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

### 2. Get API Keys

#### **Step 2a: Google Gemini API Key**

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API key" → "Create API key in new project"
3. Copy the API key (starts with `AIza...`)

#### **Step 2b: Google Custom Search API**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable "Custom Search API" in APIs & Services → Library
3. Create credentials → API Key
4. Visit [Programmable Search Engine](https://programmablesearchengine.google.com/)
5. Create a new search engine → Select "Search the entire web"
6. Copy the Search Engine ID

#### **Step 2c: Gmail App Password**

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**
3. Go to **App passwords**
4. Select Mail → Other (Custom name) → "NewsPulse AI"
5. Copy the 16-character password

See [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md) for detailed email configuration.

### 3. Configure Environment

Create a `.env` file:

```env
# Google Gemini API
GOOGLE_API_KEY=your_google_api_key_here

# Google Custom Search API
GOOGLE_SEARCH_API_KEY=your_search_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here

# Email Configuration (Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your_16_char_app_password_here

# Application Settings
MAX_ARTICLES_PER_REPORT=5
VERIFICATION_MAX_RETRIES=2
GEMINI_MODEL=models/gemini-2.5-flash
```

**Security Note:** Never commit your `.env` file to version control!

### 4. Create Your Profile

```bash
# Interactive profile creation
python create_profile_interactive.py

# Or use the template
python create_my_profile.py
```

### 5. Generate Your First Report

```bash
# Test without email delivery
python main.py generate your_user_id --no-deliver

# Generate and send via email
python main.py generate your_user_id
```

---

## ☁️ Deploy to Google Cloud Platform

### Prerequisites

- Google account
- Credit/debit card for GCP billing (free tier available)
- Time required: ~60 minutes
- Cost: ~$1-2/month for daily reports

### Quick Deploy

See [GCP_INSTALLATION_GUIDE.md](GCP_INSTALLATION_GUIDE.md) for installing Google Cloud SDK.

```bash
# 1. Set up environment
export CLOUDSDK_CONFIG=$HOME/gcloud-config
export PATH=$HOME/google-cloud-sdk/google-cloud-sdk/bin:$PATH

# 2. Authenticate
gcloud auth login
gcloud auth application-default login

# 3. Create project
export PROJECT_ID=newspulse-$(date +%s)
gcloud projects create $PROJECT_ID
gcloud config set project $PROJECT_ID

# 4. Enable billing (manual step in browser)
echo "Enable billing at: https://console.cloud.google.com/billing/linkedaccount?project=$PROJECT_ID"

# 5. Run deployment script
chmod +x deploy_gcp.sh
./deploy_gcp.sh
```

The deployment script will:
- Enable required APIs
- Create Artifact Registry repository
- Build and push Docker image
- Create Secret Manager secrets
- Deploy Cloud Run Job
- Set up Cloud Scheduler for daily execution

### Manual Deployment Steps

If you prefer manual deployment or need to troubleshoot:

#### 1. Build Docker Image

```bash
docker build --platform linux/amd64 -t newspulse-ai:latest .
```

#### 2. Push to Artifact Registry

```bash
# Create repository
gcloud artifacts repositories create newspulse-repo \
    --repository-format=docker \
    --location=us-central1

# Tag and push
docker tag newspulse-ai:latest \
    us-central1-docker.pkg.dev/$PROJECT_ID/newspulse-repo/newspulse-ai:latest

docker push us-central1-docker.pkg.dev/$PROJECT_ID/newspulse-repo/newspulse-ai:latest
```

#### 3. Create Secrets

```bash
# Store API keys in Secret Manager
echo -n "YOUR_API_KEY" | gcloud secrets create google-api-key --data-file=-
echo -n "YOUR_SEARCH_KEY" | gcloud secrets create google-search-api-key --data-file=-
echo -n "YOUR_SEARCH_ID" | gcloud secrets create google-search-engine-id --data-file=-
echo -n "YOUR_EMAIL" | gcloud secrets create smtp-username --data-file=-
echo -n "YOUR_APP_PASSWORD" | gcloud secrets create smtp-password --data-file=-
```

#### 4. Deploy Cloud Run Job

```bash
gcloud run jobs create newspulse-job \
    --image=us-central1-docker.pkg.dev/$PROJECT_ID/newspulse-repo/newspulse-ai:latest \
    --region=us-central1 \
    --set-env-vars=SMTP_SERVER=smtp.gmail.com,SMTP_PORT=587 \
    --set-secrets=GOOGLE_API_KEY=google-api-key:latest,GOOGLE_SEARCH_API_KEY=google-search-api-key:latest,GOOGLE_SEARCH_ENGINE_ID=google-search-engine-id:latest,SMTP_USERNAME=smtp-username:latest,SMTP_PASSWORD=smtp-password:latest \
    --max-retries=0 \
    --task-timeout=20m \
    --memory=2Gi \
    --cpu=2 \
    --args="python","main.py","generate","your_user_id"
```

#### 5. Set Up Cloud Scheduler (Daily at 8 AM)

```bash
gcloud scheduler jobs create http newspulse-daily \
    --location=us-central1 \
    --schedule="0 8 * * *" \
    --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/$PROJECT_ID/jobs/newspulse-job:run" \
    --http-method=POST \
    --oauth-service-account-email=$PROJECT_ID@appspot.gserviceaccount.com
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture and flow diagrams |
| [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md) | Email configuration and multi-recipient support |
| [GCP_INSTALLATION_GUIDE.md](GCP_INSTALLATION_GUIDE.md) | Install Google Cloud SDK |

---

## 🎮 Usage

### Generate Reports

```bash
# Generate test report (no email)
python main.py generate your_user_id --no-deliver

# Generate and deliver via email
python main.py generate your_user_id

# List all profiles
python main.py list

# Submit feedback
python main.py feedback <report_id> <user_id> <rating>
```

### Manage Profiles

```bash
# Create new profile (interactive)
python create_profile_interactive.py

# View profile
cat data/user_profiles/your_user_id.json
```

### Multi-Email Support

Edit your profile to add CC and BCC recipients:

```json
{
  "user_id": "your_user_id",
  "delivery_email": "primary@example.com",
  "cc_emails": [
    "manager@example.com",
    "team@example.com"
  ],
  "bcc_emails": [
    "archive@example.com"
  ]
}
```

---

## 🐳 Docker Deployment

### Local Docker

```bash
# Build image
docker build -t newspulse-ai:latest .

# Run container
docker run -it --rm \
    --env-file .env \
    -v $(pwd)/data:/app/data \
    newspulse-ai:latest \
    python main.py generate your_user_id
```

### Docker Compose

```bash
docker-compose up
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
│   ├── fetch_tool.py          # Web scraping
│   └── email_tool.py          # SMTP delivery
│
├── data/                      # User data
│   ├── user_profiles/         # Profiles (JSON)
│   └── history/               # Report history
│
├── main.py                    # CLI entry point
├── create_profile_interactive.py  # Profile creator
├── deploy_gcp.sh              # GCP deployment script
├── Dockerfile                 # Container image
├── requirements.txt           # Python dependencies
└── .env                       # Environment variables (local)
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

### Automated Scheduling

**Local (cron):**
```bash
# crontab entry (daily at 8 AM)
0 8 * * * cd /path/to/agentic-newspulse && ./venv/bin/python main.py generate your_user_id
```

**Google Cloud (Cloud Scheduler):**
See GCP deployment section above.

### Custom Topics

Edit your profile to track specific topics:

```json
{
  "topics_of_interest": [
    "Artificial Intelligence",
    "Machine Learning",
    "Cloud Computing"
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

# Test with Docker
./test_docker.sh
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` to version control**
   - Already in `.gitignore` - double-check before pushing

2. **Rotate API keys regularly**
   - Regenerate every 3-6 months
   - Delete old keys immediately

3. **Use Secret Manager in production**
   - Store credentials in GCP Secret Manager
   - Never hardcode secrets in code

4. **Monitor API usage**
   - Set up billing alerts
   - Track quota consumption

5. **Private repositories recommended**
   - Keep your deployment private
   - Review code before sharing

---

## 📈 Roadmap

### Short Term
- [ ] Web UI for profile management
- [ ] Multiple language support
- [ ] Slack/Teams integration

### Long Term
- [ ] Audio/podcast summaries
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

<div align="center">

**Built with ❤️ using Google Gemini 2.5 Flash**

Made by Nishant Gaurav

</div>
