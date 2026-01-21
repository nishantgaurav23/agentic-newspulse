# API Setup Guide - NewsPulse AI

This guide provides detailed instructions for setting up all required API keys for NewsPulse AI.

## Prerequisites

- Google account
- Gmail account (for email delivery)
- Credit card (for Google Cloud APIs - free tier available)

## 1. Google Gemini API Key

The Google Gemini API is used for all AI agents in the system.

### Setup Steps:

1. **Visit Google AI Studio**
   - Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
   - Sign in with your Google account

2. **Create API Key**
   - Click "Get API key" or "Create API key"
   - Select an existing Google Cloud project or create a new one
   - Click "Create API key in existing project" or "Create API key in new project"

3. **Copy the API Key**
   - Copy the generated API key (starts with `AIza...`)
   - Add it to your `.env` file:
     ```
     GOOGLE_API_KEY=AIza...your_key_here
     ```

4. **Important Notes**
   - Keep your API key secure and never commit it to version control
   - The free tier includes generous usage limits
   - For production use, consider setting usage quotas

---

## 2. Google Custom Search API

Used for finding relevant news articles.

### Part A: Enable Custom Search API

1. **Go to Google Cloud Console**
   - Visit [https://console.cloud.google.com/](https://console.cloud.google.com/)
   - Select the same project you used for Gemini API

2. **Enable the API**
   - Navigate to "APIs & Services" > "Library"
   - Search for "Custom Search API"
   - Click "Enable"

3. **Create API Key**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the API key
   - Add to `.env`:
     ```
     GOOGLE_SEARCH_API_KEY=AIza...your_search_key_here
     ```

### Part B: Create Programmable Search Engine

1. **Visit Programmable Search Engine**
   - Go to [https://programmablesearchengine.google.com/](https://programmablesearchengine.google.com/)
   - Click "Get started" or "Add"

2. **Configure Search Engine**
   - **Sites to search**: Select "Search the entire web"
   - **Name**: NewsPulse Search (or any name)
   - Click "Create"

3. **Enable Image and Web Search**
   - In the control panel, go to "Setup"
   - Turn ON "Image search"
   - Turn ON "Search the entire web"
   - Click "Update"

4. **Get Search Engine ID**
   - In the "Setup" tab, you'll see "Search engine ID"
   - Copy this ID (looks like: `abc123...`)
   - Add to `.env`:
     ```
     GOOGLE_SEARCH_ENGINE_ID=abc123...your_engine_id
     ```

### Quotas and Pricing

- **Free tier**: 100 search queries per day
- **Paid**: $5 per 1000 queries (up to 10k queries/day)
- For most users, the free tier is sufficient

---

## 3. Email Configuration (Gmail)

NewsPulse uses SMTP to send news reports via email.

### Setup Steps:

1. **Enable 2-Factor Authentication**
   - Go to [https://myaccount.google.com/security](https://myaccount.google.com/security)
   - Under "Signing in to Google", click "2-Step Verification"
   - Follow the prompts to enable it

2. **Generate App Password**
   - Stay in Google Account Security settings
   - Under "2-Step Verification", scroll to "App passwords"
   - Click "App passwords"
   - Select:
     - App: Mail
     - Device: Other (Custom name) - enter "NewsPulse AI"
   - Click "Generate"

3. **Copy App Password**
   - Google will show a 16-character password
   - Copy this password (without spaces)
   - Add to `.env`:
     ```
     SMTP_USERNAME=your.email@gmail.com
     SMTP_PASSWORD=your_16_char_app_password
     ```

### Alternative: Other Email Providers

If not using Gmail, update your `.env`:

```env
SMTP_SERVER=smtp.your-provider.com
SMTP_PORT=587  # or 465 for SSL
SMTP_USERNAME=your_email@provider.com
SMTP_PASSWORD=your_email_password
```

Common SMTP servers:
- **Outlook**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **SendGrid**: `smtp.sendgrid.net:587`

---

## 4. Complete .env File Example

After completing all steps, your `.env` file should look like:

```env
# Google Gemini API
GOOGLE_API_KEY=AIzaSyABC123...your_gemini_key

# Google Custom Search
GOOGLE_SEARCH_API_KEY=AIzaSyDEF456...your_search_key
GOOGLE_SEARCH_ENGINE_ID=abc123def456...your_engine_id

# Email (Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=yourname@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  # 16-char app password

# Application Settings (optional - has defaults)
LOG_LEVEL=INFO
MAX_ARTICLES_PER_REPORT=10
VERIFICATION_MAX_RETRIES=3
GEMINI_MODEL=gemini-2.0-flash-exp
TEMPERATURE=0.7
```

---

## 5. Verify Setup

Test your configuration:

```bash
cd agentic-newspulse
python -c "from config import settings; settings.validate_api_keys(); print('✓ All API keys are configured!')"
```

If successful, you'll see: `✓ All API keys are configured!`

---

## Troubleshooting

### "Invalid API key" for Gemini
- Ensure there are no extra spaces in the key
- Check that the API key is enabled in Google Cloud Console
- Verify billing is enabled (even for free tier)

### "Custom Search API not enabled"
- Go to Google Cloud Console > APIs & Services > Library
- Search for "Custom Search API" and click "Enable"

### "Search Engine ID invalid"
- Make sure you copied the Search Engine ID, not the API key
- Check that "Search the entire web" is enabled
- Wait a few minutes after creating the search engine

### "SMTP Authentication failed"
- Ensure you're using an **App Password**, not your regular Gmail password
- Verify 2FA is enabled on your Google account
- Check for typos in the email address

### "Daily quota exceeded"
- Google Custom Search has 100 free queries/day
- Reduce `MAX_ARTICLES_PER_REPORT` in `.env`
- Or upgrade to paid tier

---

## Security Best Practices

1. **Never commit `.env` to version control**
   - It's already in `.gitignore`
   - Double-check before pushing code

2. **Rotate keys regularly**
   - Regenerate API keys every 3-6 months
   - Delete old keys after rotating

3. **Use environment-specific keys**
   - Different keys for development and production
   - Use separate Google Cloud projects

4. **Monitor usage**
   - Check Google Cloud Console for API usage
   - Set up billing alerts

---

## Need Help?

- **Google Gemini API**: [Documentation](https://ai.google.dev/docs)
- **Custom Search API**: [Documentation](https://developers.google.com/custom-search/v1/overview)
- **Gmail App Passwords**: [Support](https://support.google.com/accounts/answer/185833)

For NewsPulse-specific issues, check the main [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md).
