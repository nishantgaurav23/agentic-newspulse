# ✈️ NewsPulse AI - Pre-Flight Checklist

**Complete this checklist before running deployment scripts**

---

## ✅ Step 1: Verify Installation

### Docker Desktop
```bash
docker --version
# Expected: Docker version 20.x or higher
```
- [ ] Docker Desktop installed
- [ ] Docker Desktop running (check system tray/menu bar)

### Google Cloud CLI
```bash
gcloud --version
# Expected: Google Cloud SDK version with gcloud, gsutil, etc.
```
- [ ] gcloud CLI installed
- [ ] gcloud version 400.0.0 or higher

### Python Environment
```bash
source venv/bin/activate
python --version
# Expected: Python 3.11 or higher
```
- [ ] Virtual environment exists
- [ ] Python 3.11+ installed

---

## ✅ Step 2: Verify Authentication

### Google Cloud
```bash
# Login to GCP
gcloud auth login

# Set application default credentials
gcloud auth application-default login

# Verify authentication
gcloud auth list
# Should show your account with * indicator
```
- [ ] Authenticated to GCP
- [ ] Application default credentials set

---

## ✅ Step 3: Verify API Keys

### Check .env File
```bash
cat .env | grep -E "GOOGLE_API_KEY|GOOGLE_SEARCH|SMTP"
```

Required variables:
- [ ] GOOGLE_API_KEY (from AI Studio)
- [ ] GOOGLE_SEARCH_API_KEY (from Custom Search)
- [ ] GOOGLE_SEARCH_ENGINE_ID (from Custom Search)
- [ ] SMTP_SERVER=smtp.gmail.com
- [ ] SMTP_PORT=587
- [ ] SMTP_USERNAME (your Gmail)
- [ ] SMTP_PASSWORD (Gmail App Password - 16 chars)

### Get Missing Keys

**GOOGLE_API_KEY:**
1. Go to: https://aistudio.google.com/
2. Click "Get API Key"
3. Create or select project
4. Copy API key

**GOOGLE_SEARCH_API_KEY & ENGINE_ID:**
1. Go to: https://developers.google.com/custom-search
2. Create custom search engine
3. Get API key and Engine ID

**SMTP_PASSWORD:**
1. Go to: https://myaccount.google.com/apppasswords
2. Enable 2-Step Verification first
3. Create app password for "Mail"
4. Copy 16-character password

---

## ✅ Step 4: Verify Profile Configuration

```bash
# View your profile
cat data/user_profiles/nishantgaurav23.json

# Verify multi-email recipients
python -c "
from models.user_profile import UserProfileManager
profile = UserProfileManager().load_profile('nishantgaurav23')
print(f'To: {profile.delivery_email}')
print(f'CC: {profile.cc_emails}')
print(f'BCC: {profile.bcc_emails}')
print(f'Total: {1 + len(profile.cc_emails) + len(profile.bcc_emails)} recipients')
"
```

Expected output:
```
To: primary.user@gmail.com
CC: ['team.member1@gmail.com', 'team.member2@gmail.com']
BCC: ['archive@company.com']
Total: 4 recipients
```

- [ ] Profile exists
- [ ] All 4 email addresses configured
- [ ] Topics configured (7 topics)

---

## ✅ Step 5: Verify GCP Project

### Create or Select Project
```bash
# List existing projects
gcloud projects list

# Create new project (if needed)
gcloud projects create my-newspulse-project

# Set project
gcloud config set project my-newspulse-project
```

- [ ] GCP project created or selected
- [ ] Project ID noted: ____________________

### Enable Billing
1. Go to: https://console.cloud.google.com/billing
2. Link billing account to project
3. Verify billing is enabled

- [ ] Billing enabled on project

---

## ✅ Step 6: Test Local Generation (Optional but Recommended)

```bash
# Activate environment
source venv/bin/activate

# Generate test report (no email)
python main.py generate nishantgaurav23 --no-deliver
```

This will:
- Take 3-5 minutes
- Generate a report
- NOT send email
- Verify system works before Docker/GCP deployment

- [ ] Local generation works
- [ ] Report generated successfully

---

## ✅ Step 7: Verify Script Permissions

```bash
# Make scripts executable
chmod +x test_docker.sh deploy_gcp.sh setup_scheduler.sh

# Verify permissions
ls -l *.sh
# Should show: -rwxr-xr-x for all .sh files
```

- [ ] All scripts are executable

---

## 📋 Final Checklist

Before running deployment scripts, verify ALL items:

### Software Installation
- [ ] Docker Desktop installed and running
- [ ] gcloud CLI installed (version 400+)
- [ ] Python 3.11+ with virtual environment

### Authentication
- [ ] gcloud auth login completed
- [ ] gcloud auth application-default login completed
- [ ] Authenticated user shown in `gcloud auth list`

### API Keys & Configuration
- [ ] .env file exists
- [ ] All 7 environment variables configured
- [ ] Gmail App Password obtained (16 chars)
- [ ] API keys tested (no 401/403 errors)

### Profile Configuration
- [ ] Profile nishantgaurav23 exists
- [ ] 4 email recipients configured
- [ ] 7 topics configured
- [ ] Profile loads successfully

### GCP Setup
- [ ] GCP project created/selected
- [ ] Project ID noted
- [ ] Billing enabled
- [ ] Region decided (default: us-central1)

### Scripts Ready
- [ ] test_docker.sh executable
- [ ] deploy_gcp.sh executable
- [ ] setup_scheduler.sh executable

### Optional but Recommended
- [ ] Local test generation successful
- [ ] README.md reviewed
- [ ] EXECUTE_NOW.md opened

---

## 🚀 Ready to Deploy!

If ALL checkboxes are checked, you're ready to run:

```bash
./test_docker.sh
```

If any checkbox is NOT checked, complete that step first.

---

## 🐛 Common Issues

**Docker not running**
```bash
# macOS
open -a Docker

# Then wait for Docker to start (~30 seconds)
docker info
```

**gcloud not found**
```bash
# Install from:
# https://cloud.google.com/sdk/docs/install

# After installation, restart terminal
gcloud --version
```

**Authentication expired**
```bash
# Re-authenticate
gcloud auth login
gcloud auth application-default login
```

**Missing .env file**
```bash
# Copy from example
cp .env.example .env

# Then edit with your keys
nano .env
```

---

## 📞 Need Help?

- **Quick Start:** QUICK_START.md
- **Detailed Guide:** EXECUTE_NOW.md
- **Full Documentation:** README.md
- **Troubleshooting:** DEPLOYMENT_CHECKLIST.md

---

<div align="center">

**All checked? Start deployment!**

```bash
./test_docker.sh
```

</div>
