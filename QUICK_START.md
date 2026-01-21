# ⚡ NewsPulse AI - Quick Start Guide

**Get from zero to production in 3 commands**

---

## 🎯 For the Impatient

```bash
# 1. Test locally with Docker
./test_docker.sh

# 2. Deploy to Google Cloud
./deploy_gcp.sh

# 3. Automate daily reports
./setup_scheduler.sh
```

**Total time:** ~60-90 minutes

---

## 📋 Prerequisites Checklist

Before running the commands above:

- [ ] Docker Desktop installed and running
- [ ] Google Cloud account with billing enabled
- [ ] gcloud CLI installed (`gcloud --version`)
- [ ] Authenticated to GCP (`gcloud auth login`)
- [ ] API Keys ready:
  - [ ] GOOGLE_API_KEY (from AI Studio)
  - [ ] GOOGLE_SEARCH_API_KEY
  - [ ] GOOGLE_SEARCH_ENGINE_ID
  - [ ] Gmail App Password
- [ ] Profile created (`python create_profile_interactive.py`)

---

## 🚀 Deployment Commands

### Local Testing

```bash
# Start Docker Desktop first!

# Quick test
./test_docker.sh

# Or manual
docker build -t newspulse-ai:latest .
docker run --rm --env-file .env -v $(pwd)/data:/app/data \
    newspulse-ai python main.py generate nishantgaurav23 --no-deliver
```

### GCP Deployment

```bash
# One command deployment
./deploy_gcp.sh

# Or manual (see GCP_DEPLOYMENT_GUIDE.md)
gcloud run jobs create newspulse-job ...
```

### Automation Setup

```bash
# Set up daily 8 AM reports
./setup_scheduler.sh

# Manual trigger test
gcloud scheduler jobs run newspulse-daily-report --location=us-central1
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `README.md` | Main documentation |
| `DEPLOYMENT_CHECKLIST.md` | Step-by-step deployment |
| `test_docker.sh` | Docker testing script |
| `deploy_gcp.sh` | GCP deployment script |
| `setup_scheduler.sh` | Scheduler automation |
| `docker-compose.yml` | Docker Compose config |

---

## 🔑 Environment Variables

Required in `.env`:

```env
GOOGLE_API_KEY=your_key_here
GOOGLE_SEARCH_API_KEY=your_key_here
GOOGLE_SEARCH_ENGINE_ID=your_id_here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your_app_password
MAX_ARTICLES_PER_REPORT=5
VERIFICATION_MAX_RETRIES=2
GEMINI_MODEL=models/gemini-2.5-flash
```

---

## 💡 Common Commands

### Local

```bash
# List profiles
python main.py list

# Generate test report
python main.py generate nishantgaurav23 --no-deliver

# Generate and send
python main.py generate nishantgaurav23

# Create profile
python create_profile_interactive.py
```

### Docker

```bash
# Build
docker build -t newspulse-ai:latest .

# Run
docker-compose run --rm newspulse-ai python main.py list

# Test
./test_docker.sh
```

### GCP

```bash
# Execute job
gcloud run jobs execute newspulse-job --region us-central1

# View logs
gcloud run jobs logs read newspulse-job --region us-central1

# List executions
gcloud run jobs executions list --job=newspulse-job --region=us-central1

# Trigger scheduler
gcloud scheduler jobs run newspulse-daily-report --location=us-central1
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Docker not running | Start Docker Desktop |
| gcloud not found | Install gcloud CLI |
| Permission denied | `gcloud auth login` |
| Secret Manager error | Check IAM permissions |
| Rate limit (429) | Wait 60s, or use gemini-2.5-flash |
| Email not sent | Check Gmail App Password |

---

## 📊 What to Expect

### Processing Time
- Local: 3-5 minutes per report
- GCP Cloud Run: 3-5 minutes per report

### Cost
- GCP: ~$0.60-$1.50/month for daily reports

### Email Delivery
- Gmail SMTP: 100-500 emails/day limit
- For production: Consider SendGrid/Mailgun

---

## ✅ Success Indicators

You'll know it's working when:

1. ✅ `./test_docker.sh` completes without errors
2. ✅ You receive test email locally
3. ✅ GCP job executes successfully
4. ✅ Cloud Scheduler triggers at scheduled time
5. ✅ Daily reports arrive in your inbox

---

## 📚 Full Documentation

| Document | Lines | Purpose |
|----------|-------|---------|
| README.md | 540 | Overview & usage |
| ARCHITECTURE.md | 968 | Technical deep-dive |
| EMAIL_SETUP_GUIDE.md | 187 | Email configuration |
| GCP_DEPLOYMENT_GUIDE.md | 336 | Cloud deployment |
| DEPLOYMENT_CHECKLIST.md | 600+ | Step-by-step guide |

**Total:** 2,600+ lines of documentation!

---

## 🎯 Next Steps

1. ✅ Run `./test_docker.sh`
2. ✅ Run `./deploy_gcp.sh`
3. ✅ Run `./setup_scheduler.sh`
4. ✅ Wait for tomorrow's 8 AM report
5. ✅ Provide feedback to improve

---

<div align="center">

**Questions?** Check `DEPLOYMENT_CHECKLIST.md`

**Issues?** See troubleshooting in `README.md`

**Ready?** Start with `./test_docker.sh`

</div>
