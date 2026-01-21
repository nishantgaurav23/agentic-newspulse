# QuickStart Guide - NewsPulse AI

Get up and running with NewsPulse AI in 5 minutes.

## Prerequisites Checklist

- [ ] Python 3.9 or higher installed
- [ ] Google Gemini API Key
- [ ] Google Custom Search API Key + Search Engine ID
- [ ] Gmail account with App Password

## Step-by-Step Setup

### 1. Install Dependencies (2 minutes)

```bash
cd agentic-newspulse
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys (1 minute)

```bash
cp .env.example .env
```

Edit `.env` with your keys:
```env
GOOGLE_API_KEY=AIza...
GOOGLE_SEARCH_API_KEY=AIza...
GOOGLE_SEARCH_ENGINE_ID=abc123...
SMTP_USERNAME=you@gmail.com
SMTP_PASSWORD=your_app_password
```

### 3. Create Your First Profile (1 minute)

```bash
python main.py create-profile
```

Example input:
```
User ID: demo_ceo
Full Name: Jane Doe
Role: CEO
Company: TechCorp
Industry: Technology
Email: jane@example.com

Topics of Interest:
  - Artificial Intelligence
  - Cloud Computing
  - Cybersecurity
  - [press Enter]
```

### 4. Generate Your First Report (1 minute)

```bash
python main.py generate demo_ceo
```

Watch the agents work:
- Profile Agent loads preferences
- Historical Recommender checks past reports
- Search Agent finds relevant news
- Fetch Agent retrieves content
- Writer Agent drafts summaries
- Verification Agent ensures citations
- Dispatch Agent sends email

### 5. Check Your Email!

You should receive a beautifully formatted HTML email with:
- Executive summary
- Prioritized articles
- Key insights
- Full citations for every claim

## What to Try Next

### Provide Feedback

```bash
python main.py feedback <report_id> demo_ceo 5
```

The system will learn from your preferences!

### Create Multiple Profiles

```bash
python main.py create-profile
```

Create profiles for different roles (CTO, CFO, etc.) with different interests.

### Test Without Email

```bash
python main.py generate demo_ceo --no-deliver
```

## Troubleshooting

### "No search results found"

**Cause**: Google Custom Search API not configured or quota exceeded

**Fix**:
1. Verify `GOOGLE_SEARCH_API_KEY` and `GOOGLE_SEARCH_ENGINE_ID` in `.env`
2. Check your API quota in Google Cloud Console
3. Ensure your Programmable Search Engine searches the "entire web"

### "Failed to fetch URL"

**Cause**: Website blocking or network issues

**Fix**: The system has built-in retry logic. If persistent:
1. Check your internet connection
2. Some sites block scrapers (this is normal)
3. The system will skip failed URLs and continue

### "Verification failed after max retries"

**Cause**: Writer Agent struggling to include proper citations

**Fix**: This is rare but can happen with complex topics. The system will:
1. Still generate the report
2. Flag it as unverified
3. Continue to deliver (with warning in logs)

### Email not sending

**Cause**: SMTP authentication or configuration issue

**Fix**:
1. Ensure you're using an **App Password**, not your regular password
2. Enable "Less secure app access" if not using 2FA
3. Check SMTP server and port settings

## API Key Setup Guides

### Google Gemini API

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API Key"
3. Create or select a project
4. Copy the key → paste in `.env`

### Google Custom Search API

1. Visit [Programmable Search Engine](https://programmablesearchengine.google.com/)
2. Click "Add" → Create new search engine
3. Choose "Search the entire web"
4. Copy the **Search Engine ID**
5. Visit [Google Cloud Console](https://console.cloud.google.com/)
6. Enable "Custom Search API"
7. Create API Key → paste in `.env`

### Gmail App Password

1. Enable 2FA on your Google Account
2. Visit [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate password for "Mail"
4. Copy 16-character password → paste in `.env`

## Next Steps

Read the full [README.md](README.md) for:
- Architecture deep dive
- How the verification loop works
- Customization options
- Contributing guidelines

## Need Help?

- Check logs in console (colorized by agent)
- Review generated reports in `data/history/`
- Inspect user profiles in `data/user_profiles/`

---

**You're all set! Enjoy NewsPulse AI. 🚀**
