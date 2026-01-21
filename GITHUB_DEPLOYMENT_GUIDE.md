# GitHub to GCP Automated Deployment Guide

**NewsPulse AI - Continuous Deployment Setup**

This guide explains how to set up automated deployment from GitHub to Google Cloud Platform (GCP) using GitHub Actions.

---

## 📋 Overview

When you push code to the `main` branch on GitHub, the following happens automatically:

1. ✅ GitHub Actions workflow triggered
2. 🏗️ Docker image built
3. 📦 Image pushed to GCP Artifact Registry
4. 🚀 Cloud Run Job updated with new image
5. ✉️ Ready to execute (via scheduler or manual trigger)

**Repository:** https://github.com/nishantgaurav23/agentic-newspulse

---

## 🔧 Prerequisites

Before setting up automated deployment, you need:

### 1. GCP Project Setup
- [ ] GCP project created
- [ ] Billing enabled
- [ ] Required APIs enabled:
  - Cloud Run API
  - Artifact Registry API
  - Secret Manager API
  - Cloud Scheduler API

### 2. Service Account Created
- [ ] Service account with appropriate permissions
- [ ] JSON key file downloaded

### 3. Secrets Created in GCP Secret Manager
- [ ] `google-api-key`
- [ ] `google-search-api-key`
- [ ] `google-search-engine-id`
- [ ] `smtp-username`
- [ ] `smtp-password`

---

## 🚀 Step 1: Initial GCP Setup

### Run the Setup Script

```bash
# This only needs to be done ONCE
./deploy_gcp.sh
```

This script will:
- ✅ Configure GCP project
- ✅ Enable required APIs
- ✅ Create Artifact Registry
- ✅ Create Secret Manager secrets
- ✅ Create initial Cloud Run Job

**Important:** You only run this script once for initial setup. After that, GitHub Actions handles all deployments.

---

## 🔑 Step 2: Create GCP Service Account

### Create Service Account with Required Permissions

```bash
# Set your project ID
PROJECT_ID="your-project-id"
SA_NAME="github-actions-deployer"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# Create service account
gcloud iam service-accounts create ${SA_NAME} \
    --display-name="GitHub Actions Deployer" \
    --project=${PROJECT_ID}

# Grant required permissions
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/secretmanager.secretAccessor"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/iam.serviceAccountUser"

# Create and download key
gcloud iam service-accounts keys create github-actions-key.json \
    --iam-account=${SA_EMAIL} \
    --project=${PROJECT_ID}

echo "✅ Service account created: ${SA_EMAIL}"
echo "🔑 Key file: github-actions-key.json"
echo ""
echo "⚠️  IMPORTANT: Keep this key file secure!"
echo "   You'll add it to GitHub Secrets in the next step."
```

---

## 🔒 Step 3: Configure GitHub Secrets

### Add Secrets to GitHub Repository

1. Go to your GitHub repository: https://github.com/nishantgaurav23/agentic-newspulse

2. Click **Settings** → **Secrets and variables** → **Actions**

3. Click **New repository secret**

4. Add the following secrets:

| Secret Name | Value | How to Get |
|-------------|-------|------------|
| `GCP_PROJECT_ID` | Your GCP project ID | From GCP Console or `gcloud config get-value project` |
| `GCP_REGION` | `us-central1` (or your region) | Your chosen GCP region |
| `GCP_SA_KEY` | Contents of `github-actions-key.json` | Copy entire JSON file content |

### Adding GCP_SA_KEY Secret

```bash
# Display the service account key (copy this output)
cat github-actions-key.json
```

Copy the **entire JSON output** and paste it into the `GCP_SA_KEY` secret in GitHub.

**Example of what to copy:**
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "github-actions-deployer@your-project-id.iam.gserviceaccount.com",
  ...
}
```

### Security Note

⚠️ **NEVER commit the service account key file to GitHub!**

```bash
# Delete the key file after adding to GitHub Secrets
rm github-actions-key.json

# Verify .gitignore excludes key files
grep -E "\.json|key" .gitignore
```

---

## ✅ Step 4: Verify GitHub Actions Workflow

The workflow file is already created at: `.github/workflows/deploy-gcp.yml`

### Workflow Trigger

The deployment runs automatically when:
- ✅ Code is pushed to `main` branch
- ✅ Manual trigger via GitHub Actions UI

### Workflow Steps

1. **Checkout code** - Gets latest code from repository
2. **Authenticate to GCP** - Uses service account key
3. **Setup gcloud** - Configures GCP CLI
4. **Configure Docker** - Sets up Artifact Registry authentication
5. **Build image** - Builds Docker image with commit SHA tag
6. **Push image** - Pushes to GCP Artifact Registry
7. **Deploy Job** - Updates Cloud Run Job with new image

---

## 🧪 Step 5: Test the Deployment

### Option 1: Push a Test Commit

```bash
# Make a small change
echo "# Test deployment" >> README.md

# Commit and push
git add README.md
git commit -m "Test: Trigger GitHub Actions deployment"
git push origin main
```

### Option 2: Manual Trigger

1. Go to: https://github.com/nishantgaurav23/agentic-newspulse/actions
2. Click on **Deploy to GCP Cloud Run** workflow
3. Click **Run workflow** → **Run workflow**

### Monitor Deployment

1. Watch the workflow run in GitHub Actions tab
2. Expected duration: 5-10 minutes
3. Check for green checkmarks ✅ on each step

---

## 📊 Step 6: Verify Deployment in GCP

After GitHub Actions completes:

```bash
# Check Cloud Run Job status
gcloud run jobs describe newspulse-job --region=us-central1

# View latest image in Artifact Registry
gcloud artifacts docker images list \
    us-central1-docker.pkg.dev/YOUR_PROJECT_ID/newspulse-repo/newspulse-ai \
    --sort-by=~CREATE_TIME \
    --limit=5

# Test the deployment by executing the job
gcloud run jobs execute newspulse-job --region=us-central1
```

---

## 🔄 Continuous Deployment Workflow

### Development Workflow

```bash
# 1. Make changes locally
vim agents/writer_agent.py

# 2. Test locally (optional but recommended)
python main.py generate nishantgaurav23 --no-deliver

# 3. Commit changes
git add .
git commit -m "Fix: Improve citation extraction logic"

# 4. Push to GitHub
git push origin main

# 5. GitHub Actions automatically:
#    - Builds new Docker image
#    - Pushes to Artifact Registry
#    - Updates Cloud Run Job

# 6. No manual deployment needed!
```

### After Each Push

1. ✅ GitHub Actions builds and deploys (5-10 min)
2. ✅ New code is live in GCP
3. ✅ Next scheduled run (or manual trigger) uses new code
4. ✅ No manual intervention required

---

## ⏰ Cloud Scheduler Setup

After GitHub Actions deployment is working:

```bash
# Set up daily automated reports
./setup_scheduler.sh
```

This creates a Cloud Scheduler job that:
- Runs daily at 8:00 AM (Asia/Kolkata)
- Executes the Cloud Run Job
- Generates and emails reports to all 4 recipients

---

## 🐛 Troubleshooting

### GitHub Actions Fails

**Error:** "Authentication failed"
```bash
# Solution: Verify GCP_SA_KEY secret is correct
# Re-create service account key if needed
gcloud iam service-accounts keys create new-key.json \
    --iam-account=github-actions-deployer@PROJECT_ID.iam.gserviceaccount.com
# Update GitHub secret with new key content
```

**Error:** "Permission denied"
```bash
# Solution: Grant missing IAM roles
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:SA_EMAIL" \
    --role="roles/run.admin"
```

**Error:** "Secret not found"
```bash
# Solution: Create missing secrets in Secret Manager
echo -n "YOUR_VALUE" | gcloud secrets create SECRET_NAME --data-file=-
```

### Cloud Run Job Update Fails

**Error:** "Job not found"
```bash
# Solution: Run initial setup script first
./deploy_gcp.sh
```

This creates the initial Cloud Run Job. GitHub Actions then updates it.

### Docker Build Fails

**Error:** "Build timeout"
```bash
# Solution: Increase timeout in workflow
# Edit .github/workflows/deploy-gcp.yml
# Add: timeout-minutes: 30
```

---

## 📈 Monitoring and Logs

### View GitHub Actions Logs

https://github.com/nishantgaurav23/agentic-newspulse/actions

### View GCP Logs

```bash
# Cloud Run Job logs
gcloud run jobs logs read newspulse-job --region=us-central1 --limit=100

# GitHub Actions deployment logs
gcloud logging read 'resource.type=cloud_run_job AND resource.labels.job_name=newspulse-job' \
    --limit=50 \
    --format=json
```

---

## 🔐 Security Best Practices

### ✅ Do

- ✅ Store all secrets in GitHub Secrets (encrypted)
- ✅ Store API keys in GCP Secret Manager (not environment variables)
- ✅ Use service accounts with minimal required permissions
- ✅ Rotate service account keys regularly
- ✅ Keep `.env` file in `.gitignore`
- ✅ Review GitHub Actions logs for sensitive data leaks

### ❌ Don't

- ❌ Commit `.env` files
- ❌ Commit service account key files
- ❌ Give service accounts excessive permissions
- ❌ Share service account keys
- ❌ Commit API keys or passwords
- ❌ Expose secrets in GitHub Actions logs

---

## 🎯 Summary

### Initial Setup (One-Time)

1. ✅ Run `./deploy_gcp.sh` for initial GCP setup
2. ✅ Create service account with deployment permissions
3. ✅ Add GitHub Secrets (GCP_PROJECT_ID, GCP_REGION, GCP_SA_KEY)
4. ✅ Test deployment with a push to main

### Ongoing Development

1. ✅ Make code changes locally
2. ✅ Test locally (optional)
3. ✅ Commit and push to GitHub
4. ✅ GitHub Actions deploys automatically
5. ✅ Verify deployment in GCP

### Automation

1. ✅ Run `./setup_scheduler.sh` for daily automation
2. ✅ Reports generated daily at 8 AM
3. ✅ Sent to all 4 email recipients
4. ✅ No manual intervention needed

---

## 📞 Support

### Common Issues

**Issue:** GitHub Actions not triggering

**Solution:** Check `.github/workflows/deploy-gcp.yml` is in `main` branch

**Issue:** Deployment succeeds but job doesn't run

**Solution:** Execute manually:
```bash
gcloud run jobs execute newspulse-job --region=us-central1
```

**Issue:** Email not sending to all recipients

**Solution:** Verify profile configuration:
```bash
cat data/user_profiles/nishantgaurav23.json
```

---

## 🎉 Success!

When everything is working:

- ✅ Push to GitHub → Automatic deployment
- ✅ Cloud Run Job always has latest code
- ✅ Daily 8 AM reports to 4 recipients
- ✅ Zero manual deployment steps

**Repository:** https://github.com/nishantgaurav23/agentic-newspulse

**Next:** Make your first code change and watch it deploy automatically! 🚀
