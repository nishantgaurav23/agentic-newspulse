# 📧 Email Service Setup Guide for NewsPulse AI

This guide walks you through setting up Gmail SMTP for NewsPulse AI email delivery.

---

## Prerequisites

- A Gmail account
- NewsPulse AI project set up

---

## Step 1: Enable 2-Step Verification

Google requires 2-Step Verification to create app passwords.

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Click on **2-Step Verification**
3. Follow the prompts to enable it (you'll need your phone)

**Why?** Google blocks regular password SMTP login for security. App passwords are safer.

---

## Step 2: Generate Gmail App Password

Once 2-Step Verification is enabled:

1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select:
   - **App**: Mail
   - **Device**: Other (Custom name) → type "NewsPulse AI"
3. Click **Generate**
4. Copy the 16-character password (looks like: `abcd efgh ijkl mnop`)

**Important:** Save this password securely. You won't be able to see it again.

---

## Step 3: Configure Your `.env` File

Open `/Users/nishantgaurav/Project/agentic-newspulse/.env` and ensure these values are set:

```env
# Email Configuration (for dispatch)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-gmail@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  # Your 16-char app password (remove spaces)
```

**Example:**
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=primary.user@gmail.com
SMTP_PASSWORD=fhmighwscriqtqqf
```

---

## Step 4: Test Email Delivery

Generate a test report with email delivery:

```bash
cd /Users/nishantgaurav/Project/agentic-newspulse
source venv/bin/activate
python main.py generate nishantgaurav23
```

Check your inbox (or spam folder) for the NewsPulse AI report.

---

## Step 5: Multiple Email Recipients (Optional)

To send reports to multiple email addresses, see the **Multi-Email Setup** section below.

---

# 🔄 Multi-Email Setup

NewsPulse AI supports sending the same report to multiple recipients.

## Option 1: Add CC/BCC to User Profile

Edit your profile to include additional recipients:

```json
{
  "user_id": "nishantgaurav23",
  "delivery_email": "primary.user@gmail.com",
  "cc_emails": [
    "manager@turingglobal.com",
    "team-lead@turingglobal.com"
  ],
  "bcc_emails": [
    "archive@turingglobal.com"
  ]
}
```

## Option 2: Create Multiple Profiles (Recommended)

For different users with different interests:

```bash
# Create profile for team member 1
python create_profile_interactive.py

# Create profile for team member 2
python create_profile_interactive.py
```

Then schedule reports for each profile separately.

---

# ⚠️ Important Notes

## Gmail SMTP Limitations

- **Daily Limit**: 100-500 emails per day (varies by account age)
- **Rate Limiting**: ~100 emails per hour
- **Best for**: Personal use, small teams, testing

## For Production / High Volume

Consider professional email services:

- **SendGrid**: 100 emails/day free, then pay-as-you-go
- **Amazon SES**: $0.10 per 1,000 emails
- **Mailgun**: 5,000 emails/month free
- **Postmark**: Transactional email specialist

---

# 🔐 Security Best Practices

1. **Never commit `.env` to version control**
   - Already in `.gitignore` ✅

2. **Use app passwords, not your real Gmail password**
   - App passwords can be revoked without changing your main password

3. **For GCP deployment, use Secret Manager**
   - See `GCP_DEPLOYMENT_GUIDE.md` for details

4. **Rotate app passwords periodically**
   - Revoke old ones at [App Passwords](https://myaccount.google.com/apppasswords)

---

# 🐛 Troubleshooting

## "SMTP AUTH extension not supported"
- Make sure you're using the **app password**, not your regular Gmail password
- Check that 2-Step Verification is enabled

## "Username and Password not accepted"
- Remove spaces from the app password
- Regenerate a new app password if needed

## Email ends up in spam
- Recipients should add your email to contacts
- Use a professional "from" name in profile settings
- For production, configure SPF/DKIM records

## "SMTPAuthenticationError"
- Your app password may have been revoked
- Check at [App Passwords](https://myaccount.google.com/apppasswords)
- Generate a new one if needed

---

# 📚 Next Steps

1. ✅ Email service configured
2. Test report delivery
3. Set up automated scheduling (cron jobs)
4. Deploy to GCP for 24/7 operation → See `GCP_DEPLOYMENT_GUIDE.md`

---

**Need help?** Check the main README.md or file an issue.
