# GitHub Actions Workflows

## 🚀 Automated Deployment to GCP

### deploy-gcp.yml

**Purpose:** Automatically deploy NewsPulse AI to Google Cloud Platform when code is pushed to `main` branch.

**Triggers:**
- Push to `main` branch
- Manual workflow dispatch

**Required Secrets:**

Add these secrets in: **Settings → Secrets and variables → Actions**

| Secret Name | Description |
|-------------|-------------|
| `GCP_PROJECT_ID` | Your GCP project ID |
| `GCP_REGION` | GCP region (e.g., `us-central1`) |
| `GCP_SA_KEY` | Service account JSON key with deployment permissions |

**Workflow Steps:**

1. Checkout code
2. Authenticate to GCP
3. Configure Docker for Artifact Registry
4. Build Docker image
5. Push to Artifact Registry
6. Deploy/Update Cloud Run Job

**Duration:** ~5-10 minutes

**View Runs:** https://github.com/nishantgaurav23/agentic-newspulse/actions

---

## 📋 Setup Guide

See: [GITHUB_DEPLOYMENT_GUIDE.md](../../GITHUB_DEPLOYMENT_GUIDE.md)

**Quick Setup:**

1. Run initial GCP setup: `./deploy_gcp.sh`
2. Create service account with deployment permissions
3. Add GitHub Secrets (GCP_PROJECT_ID, GCP_REGION, GCP_SA_KEY)
4. Push to `main` → Automatic deployment!

---

## 🔧 Manual Trigger

To deploy without pushing code:

1. Go to: https://github.com/nishantgaurav23/agentic-newspulse/actions
2. Click **Deploy to GCP Cloud Run**
3. Click **Run workflow** → **Run workflow**

---

## 🐛 Troubleshooting

**Workflow fails with "Authentication failed"**
- Verify `GCP_SA_KEY` secret is correctly set
- Check service account has required permissions

**Job not found error**
- Run `./deploy_gcp.sh` first to create initial Cloud Run Job
- GitHub Actions updates existing jobs, doesn't create them

**Build timeout**
- Workflow has 60-minute timeout by default
- Check Docker build steps for issues

---

## 📊 Monitoring

**View logs in GitHub:**
- https://github.com/nishantgaurav23/agentic-newspulse/actions

**View logs in GCP:**
```bash
gcloud run jobs logs read newspulse-job --region=us-central1
```

---

## ✅ Success Indicators

Deployment succeeded when:
- ✅ All workflow steps have green checkmarks
- ✅ "Deployment completed successfully!" message shown
- ✅ New image appears in Artifact Registry
- ✅ Cloud Run Job updated timestamp is recent

**Verify:**
```bash
gcloud run jobs describe newspulse-job --region=us-central1
```
