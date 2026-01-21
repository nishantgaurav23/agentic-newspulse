# 📋 NewsPulse AI - Deployment Checklist

Complete guide to deploy NewsPulse AI from local testing to production.

---

## ✅ Step 1: Review Documentation

**Status:** ✅ Complete

**Files to Review:**
- [x] `README.md` (540 lines) - Main documentation
- [x] `ARCHITECTURE.md` (968 lines) - Technical architecture
- [x] `EMAIL_SETUP_GUIDE.md` (187 lines) - Email configuration
- [x] `GCP_DEPLOYMENT_GUIDE.md` (336 lines) - Cloud deployment

**Documentation Stats:**
- Total: 2,030 lines of comprehensive documentation
- 4 major guides covering all aspects
- ASCII diagrams for visual understanding

**Action:** ✅ Documentation reviewed and complete

---

## ✅ Step 2: Test Multi-Email Support

**Status:** ✅ Complete

### What Was Done

1. **Updated Profile Schema:**
   - Added `cc_emails` field for visible recipients
   - Added `bcc_emails` field for hidden recipients
   - Updated `nishantgaurav23.json` profile

2. **Updated Code:**
   - `models/schemas.py` - New fields in UserProfile
   - `tools/email_tool.py` - CC/BCC support in send_email_report()
   - `agents/dispatch_agent.py` - Passes CC/BCC to email tool
   - `create_profile_interactive.py` - Interactive CC/BCC input

### How to Use

Edit your profile:
```json
{
  "delivery_email": "primary.user@gmail.com",
  "cc_emails": ["team.member1@gmail.com", "team.member2@gmail.com"],
  "bcc_emails": ["archive@company.com"]
}
```

Or use interactive profile creator:
```bash
python create_profile_interactive.py
```

### Verification

```bash
# Verify profile loads correctly
python main.py list
```

**Result:** ✅ Profile loading works with new fields

---

## ⏳ Step 3: Test Docker Build

**Status:** Ready to execute

### Prerequisites

1. **Install Docker Desktop**
   - Download: https://www.docker.com/products/docker-desktop
   - Start Docker Desktop application

2. **Verify Docker is running:**
   ```bash
   docker info
   ```

### Automated Testing

We've created an automated test script:

```bash
./test_docker.sh
```

This script will:
1. ✅ Check if Docker is running
2. 📦 Build the Docker image
3. 🧪 Test profile listing
4. 🧪 Generate a test report (3-5 minutes)
5. 📊 Show image size and stats

### Manual Testing

If you prefer manual testing:

```bash
# 1. Build the image
docker build -t newspulse-ai:latest .

# 2. Test profile listing
docker run --rm --env-file .env newspulse-ai:latest python main.py list

# 3. Generate test report (no email)
docker run --rm \
    --env-file .env \
    -v $(pwd)/data:/app/data \
    newspulse-ai:latest \
    python main.py generate nishantgaurav23 --no-deliver

# 4. Generate and send email
docker run --rm \
    --env-file .env \
    -v $(pwd)/data:/app/data \
    newspulse-ai:latest \
    python main.py generate nishantgaurav23
```

### Using Docker Compose

We've also created `docker-compose.yml` for easier management:

```bash
# List profiles
docker-compose up

# Generate test report
docker-compose run --rm newspulse-ai python main.py generate nishantgaurav23 --no-deliver

# Generate and send
docker-compose run --rm newspulse-ai python main.py generate nishantgaurav23
```

---

## ⏳ Step 4: Deploy to GCP Cloud Run

**Status:** Ready to execute

### Prerequisites

1. **Google Cloud Account**
   - Sign up: https://cloud.google.com/
   - Create a new project or use existing

2. **Install gcloud CLI**
   - Download: https://cloud.google.com/sdk/docs/install
   - Verify: `gcloud --version`

3. **Authenticate:**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

4. **Enable Billing**
   - Required for Cloud Run, Secret Manager, etc.
   - Estimated cost: ~$0.50-$2.00/month

### Automated Deployment

We've created an automated deployment script:

```bash
./deploy_gcp.sh
```

This script will:
1. 🔧 Configure gcloud project and region
2. 🔧 Enable required APIs
3. 🔧 Create Artifact Registry repository
4. 🔧 Configure Docker authentication
5. 🔧 Create secrets in Secret Manager
6. 🔧 Grant IAM permissions
7. 📦 Build and push Docker image
8. 🚀 Deploy as Cloud Run Job

**What you'll need:**
- GCP Project ID
- Region (default: us-central1)
- API Keys:
  - GOOGLE_API_KEY
  - GOOGLE_SEARCH_API_KEY
  - GOOGLE_SEARCH_ENGINE_ID
  - SMTP_PASSWORD (Gmail App Password)
- SMTP_USERNAME (your Gmail)

### Manual Deployment

If you prefer manual steps, see `GCP_DEPLOYMENT_GUIDE.md` for detailed instructions.

### Verify Deployment

```bash
# Test the Cloud Run Job
gcloud run jobs execute newspulse-job --region us-central1

# View executions
gcloud run jobs executions list --job=newspulse-job --region=us-central1

# View logs
gcloud run jobs logs read newspulse-job --region=us-central1 --limit 100

# Check job details
gcloud run jobs describe newspulse-job --region=us-central1
```

---

## ⏳ Step 5: Set Up Cloud Scheduler Automation

**Status:** Ready to execute

### Purpose

Automate daily report generation at a specific time (e.g., 8 AM daily).

### Automated Setup

We've created an automated scheduler setup script:

```bash
./setup_scheduler.sh
```

This script will:
1. ⏰ Configure Cloud Scheduler
2. 🔐 Grant necessary IAM permissions
3. 📅 Set up daily cron job
4. ✅ Verify configuration

**What you'll need:**
- GCP Project ID
- Region (default: us-central1)
- Schedule time (default: 08:00)
- Timezone (default: Asia/Kolkata)

### Scheduler Configuration

The script creates a scheduler job that:
- Runs daily at your specified time
- Triggers the Cloud Run Job
- Generates and emails the report automatically

### Manual Trigger

Test the scheduler immediately:
```bash
gcloud scheduler jobs run newspulse-daily-report --location=us-central1
```

### Manage Scheduler

```bash
# View scheduler details
gcloud scheduler jobs describe newspulse-daily-report --location=us-central1

# Pause scheduler
gcloud scheduler jobs pause newspulse-daily-report --location=us-central1

# Resume scheduler
gcloud scheduler jobs resume newspulse-daily-report --location=us-central1

# Update schedule
gcloud scheduler jobs update http newspulse-daily-report \
    --location=us-central1 \
    --schedule="0 9 * * *"  # Change to 9 AM

# View logs
gcloud logging read \
    'resource.type=cloud_scheduler_job AND resource.labels.job_id=newspulse-daily-report' \
    --limit 50
```

---

## 📊 Deployment Summary

### Files Created

**Scripts:**
- ✅ `test_docker.sh` - Docker testing automation
- ✅ `deploy_gcp.sh` - GCP deployment automation
- ✅ `setup_scheduler.sh` - Cloud Scheduler setup
- ✅ `docker-compose.yml` - Docker Compose configuration

**Documentation:**
- ✅ `README.md` - Main documentation (540 lines)
- ✅ `ARCHITECTURE.md` - Technical details (968 lines)
- ✅ `EMAIL_SETUP_GUIDE.md` - Email setup (187 lines)
- ✅ `GCP_DEPLOYMENT_GUIDE.md` - Deployment guide (336 lines)
- ✅ `DEPLOYMENT_CHECKLIST.md` - This file

**Configuration:**
- ✅ `Dockerfile` - Production container
- ✅ `.dockerignore` - Build optimization

### Code Updates

**Multi-Email Support:**
- ✅ `models/schemas.py` - Added cc_emails, bcc_emails
- ✅ `tools/email_tool.py` - CC/BCC implementation
- ✅ `agents/dispatch_agent.py` - Multi-recipient delivery
- ✅ `create_profile_interactive.py` - Interactive CC/BCC input

---

## 🎯 Execution Order

### Recommended Flow

```
1. ✅ Review Documentation
   └─> Understand the system

2. ✅ Test Multi-Email
   └─> Verify code works locally

3. ⏳ Test Docker Build
   └─> ./test_docker.sh
   └─> Verify containerization

4. ⏳ Deploy to GCP
   └─> ./deploy_gcp.sh
   └─> Get cloud infrastructure

5. ⏳ Set Up Scheduler
   └─> ./setup_scheduler.sh
   └─> Automate daily reports
```

### Time Estimates

| Step | Time Required | Notes |
|------|---------------|-------|
| Step 1 | 15-30 min | Reading documentation |
| Step 2 | 5 min | Profile update |
| Step 3 | 15-20 min | Docker build + test report |
| Step 4 | 20-30 min | GCP deployment |
| Step 5 | 5-10 min | Scheduler setup |
| **Total** | **60-95 min** | Full deployment |

---

## 💰 Cost Estimation

### GCP Monthly Costs (Daily Reports)

| Service | Usage | Cost |
|---------|-------|------|
| **Cloud Run Jobs** | ~30 executions/month (5 min each) | $0.30-$1.00 |
| **Artifact Registry** | 1 image (~500MB) | $0.05-$0.10 |
| **Secret Manager** | 4 secrets | $0.24 |
| **Cloud Scheduler** | 1 job (free tier) | $0.00 |
| **Cloud Logging** | ~1GB logs | $0.00 (free tier) |
| **Networking** | Minimal egress | $0.00-$0.10 |
| **TOTAL** | | **~$0.60-$1.50/month** |

### Free Tier Benefits

- Cloud Scheduler: First 3 jobs free
- Cloud Logging: 50GB/month free
- Cloud Run: 2M requests free (we use ~30/month)

---

## 🔒 Security Checklist

- [x] API keys stored in Secret Manager (not .env)
- [x] Service account with least privilege
- [x] Docker images in private Artifact Registry
- [x] SMTP using app password (not real password)
- [x] .env file in .gitignore
- [x] No secrets in code or logs

---

## 🐛 Troubleshooting

### Docker Build Issues

**Problem:** Docker daemon not running
```bash
# Solution: Start Docker Desktop
open -a Docker  # macOS
```

**Problem:** Build fails with dependency errors
```bash
# Solution: Clear Docker cache
docker system prune -a
docker build --no-cache -t newspulse-ai:latest .
```

### GCP Deployment Issues

**Problem:** Permission denied
```bash
# Solution: Re-authenticate
gcloud auth login
gcloud auth application-default login
```

**Problem:** API not enabled
```bash
# Solution: Enable manually
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

**Problem:** Secret Manager access denied
```bash
# Solution: Grant IAM permission
PROJECT_NUMBER=$(gcloud projects describe PROJECT_ID --format='value(projectNumber)')
gcloud secrets add-iam-policy-binding google-api-key \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

### Cloud Scheduler Issues

**Problem:** Job not triggering
```bash
# Solution: Check IAM permissions
gcloud run jobs add-iam-policy-binding newspulse-job \
    --region=us-central1 \
    --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
    --role="roles/run.invoker"
```

**Problem:** Wrong timezone
```bash
# Solution: Update scheduler
gcloud scheduler jobs update http newspulse-daily-report \
    --location=us-central1 \
    --time-zone="America/New_York"
```

---

## 📞 Support

If you encounter issues:

1. Check logs:
   ```bash
   # Local
   tail -f logs/newspulse.log

   # Cloud Run
   gcloud run jobs logs read newspulse-job --region=us-central1

   # Scheduler
   gcloud logging read 'resource.type=cloud_scheduler_job' --limit 50
   ```

2. Review documentation:
   - README.md
   - ARCHITECTURE.md
   - GCP_DEPLOYMENT_GUIDE.md

3. Check GitHub Issues (if available)

---

## ✅ Success Criteria

You'll know deployment is successful when:

- [ ] Docker image builds without errors
- [ ] Local Docker test generates a report
- [ ] GCP Cloud Run Job executes successfully
- [ ] Email is received in your inbox
- [ ] Cloud Scheduler triggers at the scheduled time
- [ ] Daily reports arrive automatically

---

## 🎉 Next Steps After Deployment

1. **Monitor Performance:**
   - Check Cloud Run logs daily for errors
   - Review email delivery rates
   - Monitor API quota usage

2. **Optimize:**
   - Adjust MAX_ARTICLES_PER_REPORT based on quality
   - Fine-tune verification settings
   - Add more topics to your profile

3. **Scale:**
   - Create profiles for team members
   - Set up different schedules for different users
   - Add Slack/Teams integration (future)

4. **Provide Feedback:**
   - Use `python main.py feedback` command
   - Help the system learn your preferences
   - Improve future reports

---

<div align="center">

**🚀 Ready to Deploy!**

Start with: `./test_docker.sh`

Then: `./deploy_gcp.sh`

Finally: `./setup_scheduler.sh`

</div>
