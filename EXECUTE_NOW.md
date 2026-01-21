# ⚡ NewsPulse AI - Execute Deployment NOW

**Ready-to-run commands for complete deployment**

---

## 🎯 Your Profile Configuration

✅ **Profile:** nishantgaurav23
✅ **Primary Email:** primary.user@gmail.com
✅ **CC Recipients:**
   - team.member1@gmail.com
   - team.member2@gmail.com
✅ **BCC Recipients:**
   - archive@company.com
✅ **Total Recipients:** 4 people per report
✅ **Topics:** AI, ML, Software Dev, Cloud, Python, React, DevOps
✅ **Schedule:** Daily at 08:00 AM (Asia/Kolkata)

---

## 🚀 Execute All 5 Steps

### Prerequisites Check

Before starting, verify:

```bash
# Check Docker
docker --version
# If not found: Install Docker Desktop from docker.com

# Check gcloud
gcloud --version
# If not found: Install from cloud.google.com/sdk

# Check Python environment
source venv/bin/activate
python main.py list
# Should show: nishantgaurav23 profile
```

---

## Step 1: ✅ Documentation (COMPLETE)

**Status:** Already reviewed

**What we have:**
- ✅ README.md (540 lines)
- ✅ ARCHITECTURE.md (968 lines)
- ✅ EMAIL_SETUP_GUIDE.md (187 lines)
- ✅ GCP_DEPLOYMENT_GUIDE.md (336 lines)
- ✅ DEPLOYMENT_CHECKLIST.md (600+ lines)
- ✅ QUICK_START.md (180 lines)

**Total:** 2,600+ lines of documentation

---

## Step 2: ✅ Multi-Email Support (COMPLETE)

**Status:** Configured and tested

**Your configuration:**
```json
{
  "delivery_email": "primary.user@gmail.com",
  "cc_emails": [
    "team.member1@gmail.com",
    "team.member2@gmail.com"
  ],
  "bcc_emails": [
    "archive@company.com"
  ]
}
```

**Test it:**
```bash
# Generate test report (local, no email yet)
source venv/bin/activate
python main.py generate nishantgaurav23 --no-deliver

# Generate and send to all 4 recipients
python main.py generate nishantgaurav23
```

---

## Step 3: 🏃 Docker Testing (EXECUTE NOW)

### Option A: Automated (Recommended)

```bash
# Make sure Docker Desktop is running!
./test_docker.sh
```

**What it does:**
1. ✅ Checks Docker is running
2. 📦 Builds Docker image (~5 min)
3. 🧪 Tests profile listing
4. 🧪 Generates test report (~3-5 min)
5. 📊 Shows image size

**Expected output:**
```
✅ Docker is running
📦 Building Docker image...
✅ Docker image built successfully
🧪 Test 1: List user profiles
✅ Profile listing works
🧪 Test 2: Generate test report
✅ Test report generation works
```

### Option B: Manual Testing

```bash
# Start Docker Desktop first!

# Build image
docker build -t newspulse-ai:latest .

# Test listing
docker run --rm --env-file .env \
    newspulse-ai:latest \
    python main.py list

# Generate test report
docker run --rm \
    --env-file .env \
    -v $(pwd)/data:/app/data \
    newspulse-ai:latest \
    python main.py generate nishantgaurav23 --no-deliver

# Generate and send to all 4 recipients
docker run --rm \
    --env-file .env \
    -v $(pwd)/data:/app/data \
    newspulse-ai:latest \
    python main.py generate nishantgaurav23
```

### Option C: Docker Compose

```bash
# Test
docker-compose run --rm newspulse-ai \
    python main.py generate nishantgaurav23 --no-deliver

# Send to all 4 recipients
docker-compose run --rm newspulse-ai \
    python main.py generate nishantgaurav23
```

**Time:** 15-20 minutes

---

## Step 4: 🏃 GCP Deployment (EXECUTE NOW)

### Prerequisites

```bash
# Authenticate to GCP
gcloud auth login
gcloud auth application-default login

# Verify authentication
gcloud auth list
```

### Execute Deployment

```bash
./deploy_gcp.sh
```

**What it will ask you:**

1. **GCP Project ID** (e.g., `my-newspulse-project`)
2. **Region** (press Enter for default: us-central1)
3. **Confirm deployment** (type: yes)
4. **GOOGLE_API_KEY** (from AI Studio)
5. **GOOGLE_SEARCH_API_KEY** (from Custom Search)
6. **GOOGLE_SEARCH_ENGINE_ID** (from Custom Search)
7. **SMTP_PASSWORD** (Gmail App Password - 16 chars)
8. **SMTP_USERNAME** (your Gmail: primary.user@gmail.com)

**What it does:**

1. ✅ Configures GCP project
2. ✅ Enables APIs (Run, Secrets, Scheduler, etc.)
3. ✅ Creates Artifact Registry
4. ✅ Stores secrets in Secret Manager
5. ✅ Builds Docker image
6. ✅ Pushes to Artifact Registry
7. ✅ Creates Cloud Run Job
8. ✅ Grants IAM permissions

**Expected output:**
```
☁️  NewsPulse AI - GCP Deployment Script
========================================

Configuration:
  Project ID: my-newspulse-project
  Region: us-central1

🔧 Step 1: Configure gcloud
✅ gcloud configured

🔧 Step 2: Enable required APIs
✅ APIs enabled

...

🎉 Deployment Complete!
```

**Time:** 20-30 minutes

### Verify Deployment

```bash
# Test the Cloud Run Job
gcloud run jobs execute newspulse-job --region us-central1

# View execution status
gcloud run jobs executions list \
    --job=newspulse-job \
    --region=us-central1

# View logs
gcloud run jobs logs read newspulse-job \
    --region=us-central1 \
    --limit=100

# Check if email was sent to all 4 recipients
```

---

## Step 5: 🏃 Cloud Scheduler (EXECUTE NOW)

### Execute Scheduler Setup

```bash
./setup_scheduler.sh
```

**What it will ask you:**

1. **GCP Project ID** (same as Step 4)
2. **Region** (press Enter for default: us-central1)
3. **Schedule time** (press Enter for default: 08:00)
4. **Timezone** (press Enter for default: Asia/Kolkata)
5. **Confirm setup** (type: yes)

**What it does:**

1. ✅ Grants Cloud Run invoker permission
2. ✅ Creates Cloud Scheduler job
3. ✅ Sets daily 8 AM schedule
4. ✅ Configures timezone

**Expected output:**
```
⏰ NewsPulse AI - Cloud Scheduler Setup
=======================================

Configuration:
  Project ID: my-newspulse-project
  Region: us-central1
  Schedule: 08:00 AM (Asia/Kolkata)
  Cron: 0 8 * * *

✅ Cloud Scheduler configured!
```

**Time:** 5-10 minutes

### Test Scheduler Immediately

```bash
# Manually trigger the scheduler (don't wait for 8 AM)
gcloud scheduler jobs run newspulse-daily-report \
    --location=us-central1

# Check execution
gcloud run jobs executions list \
    --job=newspulse-job \
    --region=us-central1 \
    --limit=1

# View logs
gcloud run jobs logs read newspulse-job \
    --region=us-central1 \
    --limit=50
```

---

## 🎯 Complete Execution Script

Run all steps in sequence:

```bash
#!/bin/bash
# Complete NewsPulse AI Deployment

echo "🚀 Starting Complete Deployment..."
echo ""

# Step 3: Docker Testing
echo "Step 3/3: Docker Testing..."
./test_docker.sh
echo ""

# Step 4: GCP Deployment
echo "Step 4/3: GCP Deployment..."
./deploy_gcp.sh
echo ""

# Step 5: Cloud Scheduler
echo "Step 5/3: Cloud Scheduler..."
./setup_scheduler.sh
echo ""

echo "🎉 Complete Deployment Finished!"
echo ""
echo "✅ Check your email (all 4 recipients) for the first report"
echo "✅ Tomorrow at 8 AM, automated reports will start"
```

Save as `deploy_all.sh` and run:

```bash
chmod +x deploy_all.sh
./deploy_all.sh
```

---

## 📊 What to Expect

### During Deployment

**Step 3 (Docker):**
- Build time: ~5 minutes
- Test report: ~3-5 minutes
- Total: ~15-20 minutes

**Step 4 (GCP):**
- Setup: ~10 minutes
- Docker push: ~5-10 minutes
- Deployment: ~5 minutes
- Total: ~20-30 minutes

**Step 5 (Scheduler):**
- Configuration: ~2 minutes
- Testing: ~3-5 minutes
- Total: ~5-10 minutes

**Grand Total:** 60-90 minutes

### After Deployment

**Immediate:**
- ✅ Cloud Run Job deployed
- ✅ Scheduler configured
- ✅ Secrets stored securely

**First Manual Test:**
```bash
gcloud scheduler jobs run newspulse-daily-report --location=us-central1
```
- ⏱️ Wait 3-5 minutes
- ✅ Check email: All 4 recipients get report

**Tomorrow at 8 AM:**
- ✅ Automated execution
- ✅ Report generated
- ✅ Sent to all 4 recipients
- ✅ Saved to history

**Every Day at 8 AM:**
- ✅ Same automated process
- ✅ Fresh news articles
- ✅ No duplicates (deduplication active)

---

## ✅ Success Checklist

After running all steps, verify:

- [ ] Docker image builds without errors
- [ ] `./test_docker.sh` completes successfully
- [ ] Test report generated locally
- [ ] GCP Cloud Run Job created
- [ ] `gcloud run jobs execute` works
- [ ] Email received by all 4 recipients
- [ ] Cloud Scheduler job created
- [ ] Manual trigger sends email
- [ ] Logs show successful execution

---

## 📧 Email Recipients Verification

Your reports will be sent to:

1. **Primary (To):** primary.user@gmail.com
   - Full report with priority badge
   - All articles and citations

2. **CC #1:** team.member1@gmail.com
   - Visible to all recipients
   - Full report access

3. **CC #2:** team.member2@gmail.com
   - Visible to all recipients
   - Full report access

4. **BCC:** archive@company.com
   - Hidden from other recipients
   - Full report access
   - Good for archiving

**Total:** 4 people receive each report

---

## 💰 Cost Summary

### GCP Monthly Costs

| Service | Cost |
|---------|------|
| Cloud Run Jobs (30/month) | $0.30-$1.00 |
| Artifact Registry | $0.05-$0.10 |
| Secret Manager (4 secrets) | $0.24 |
| Cloud Scheduler | $0.00 (free) |
| **TOTAL** | **$0.60-$1.50** |

**Per day:** ~$0.02-$0.05
**Per report:** ~$0.02-$0.05

---

## 🐛 Troubleshooting

### Docker Issues

**Error:** "Docker daemon not running"
```bash
# Start Docker Desktop
open -a Docker  # macOS
# Or start Docker Desktop app
```

**Error:** "Build failed"
```bash
# Clear cache and rebuild
docker system prune -a
docker build --no-cache -t newspulse-ai:latest .
```

### GCP Issues

**Error:** "Project not found"
```bash
# Create new project
gcloud projects create my-newspulse-project
gcloud config set project my-newspulse-project
```

**Error:** "Permission denied"
```bash
# Re-authenticate
gcloud auth login
gcloud auth application-default login
```

**Error:** "Billing not enabled"
```bash
# Enable billing in GCP Console
# https://console.cloud.google.com/billing
```

### Email Issues

**Error:** "SMTP authentication failed"
```bash
# Generate new Gmail App Password
# Go to: https://myaccount.google.com/apppasswords
# Delete old password, create new one
# Update .env file with new password
```

**Issue:** "Only primary recipient gets email, not CC/BCC"
```bash
# Verify profile configuration
python -c "
from models.user_profile import UserProfileManager
profile = UserProfileManager().load_profile('nishantgaurav23')
print('CC:', profile.cc_emails)
print('BCC:', profile.bcc_emails)
"
```

---

## 📞 Need Help?

**Documentation:**
- Quick reference: `QUICK_START.md`
- Full guide: `DEPLOYMENT_CHECKLIST.md`
- Architecture: `ARCHITECTURE.md`
- Email setup: `EMAIL_SETUP_GUIDE.md`

**Logs:**
```bash
# Local logs
tail -f logs/newspulse.log

# GCP logs
gcloud run jobs logs read newspulse-job --region=us-central1

# Scheduler logs
gcloud logging read 'resource.type=cloud_scheduler_job' --limit=50
```

---

## 🎉 Ready to Execute!

### Quick Start (3 Commands)

```bash
# 1. Test locally
./test_docker.sh

# 2. Deploy to cloud
./deploy_gcp.sh

# 3. Automate daily reports
./setup_scheduler.sh
```

### Or All at Once

```bash
./test_docker.sh && ./deploy_gcp.sh && ./setup_scheduler.sh
```

---

<div align="center">

## ⚡ START NOW!

**First command to run:**

```bash
./test_docker.sh
```

**Then follow the prompts for Steps 4 and 5**

Good luck! 🚀

</div>
