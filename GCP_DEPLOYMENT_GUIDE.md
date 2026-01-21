# 🚀 GCP Cloud Run Deployment Guide

Deploy NewsPulse AI to Google Cloud Platform for 24/7 automated news report generation.

---

## Prerequisites

- Google Cloud Platform account
- [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed
- Docker installed locally
- NewsPulse AI project set up

---

## Architecture Overview

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Cloud     │──────│  Container   │──────│   Secret    │
│   Run       │      │  Registry    │      │   Manager   │
│  (Compute)  │      │  (Artifact)  │      │  (API Keys) │
└─────────────┘      └──────────────┘      └─────────────┘
       │                                            │
       │                                            │
       ▼                                            ▼
┌─────────────────────────────────────────────────────────┐
│              Cloud Scheduler (Cron Jobs)                 │
│           Triggers report generation daily                │
└─────────────────────────────────────────────────────────┘
```

---

## Step 1: Configure GCP Project

```bash
# Set your project ID
export PROJECT_ID="your-project-id"

# Configure gcloud
gcloud config set project $PROJECT_ID
gcloud config set run/region us-central1

# Enable required APIs
gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    secretmanager.googleapis.com \
    cloudscheduler.googleapis.com
```

---

## Step 2: Create Artifact Registry

```bash
# Create a Docker repository
gcloud artifacts repositories create newspulse-repo \
    --repository-format=docker \
    --location=us-central1 \
    --description="NewsPulse AI container repository"

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev
```

---

## Step 3: Store Secrets in Secret Manager

```bash
# Create secrets for sensitive data
echo -n "YOUR_GOOGLE_API_KEY" | gcloud secrets create google-api-key --data-file=-
echo -n "YOUR_GOOGLE_SEARCH_API_KEY" | gcloud secrets create google-search-api-key --data-file=-
echo -n "YOUR_SEARCH_ENGINE_ID" | gcloud secrets create google-search-engine-id --data-file=-
echo -n "YOUR_SMTP_PASSWORD" | gcloud secrets create smtp-password --data-file=-

# Grant Cloud Run access to secrets
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')

for SECRET in google-api-key google-search-api-key google-search-engine-id smtp-password; do
    gcloud secrets add-iam-policy-binding $SECRET \
        --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
        --role="roles/secretmanager.secretAccessor"
done
```

---

## Step 4: Build and Push Docker Image

```bash
# Build the Docker image locally
docker build -t newspulse-ai:latest .

# Tag for Artifact Registry
docker tag newspulse-ai:latest \
    us-central1-docker.pkg.dev/$PROJECT_ID/newspulse-repo/newspulse-ai:latest

# Push to Artifact Registry
docker push us-central1-docker.pkg.dev/$PROJECT_ID/newspulse-repo/newspulse-ai:latest
```

---

## Step 5: Deploy to Cloud Run

```bash
# Deploy with secrets
gcloud run deploy newspulse-service \
    --image us-central1-docker.pkg.dev/$PROJECT_ID/newspulse-repo/newspulse-ai:latest \
    --region us-central1 \
    --platform managed \
    --no-allow-unauthenticated \
    --set-env-vars SMTP_SERVER=smtp.gmail.com \
    --set-env-vars SMTP_PORT=587 \
    --set-env-vars SMTP_USERNAME=your-email@gmail.com \
    --set-env-vars MAX_ARTICLES_PER_REPORT=5 \
    --set-env-vars VERIFICATION_MAX_RETRIES=2 \
    --set-env-vars GEMINI_MODEL=models/gemini-2.5-flash \
    --set-secrets GOOGLE_API_KEY=google-api-key:latest \
    --set-secrets GOOGLE_SEARCH_API_KEY=google-search-api-key:latest \
    --set-secrets GOOGLE_SEARCH_ENGINE_ID=google-search-engine-id:latest \
    --set-secrets SMTP_PASSWORD=smtp-password:latest \
    --memory 1Gi \
    --cpu 1 \
    --timeout 10m \
    --max-instances 5
```

---

## Step 6: Set Up Cloud Scheduler (Automated Daily Reports)

```bash
# Get the Cloud Run service URL
SERVICE_URL=$(gcloud run services describe newspulse-service \
    --region us-central1 \
    --format='value(status.url)')

# Create a service account for Cloud Scheduler
gcloud iam service-accounts create newspulse-scheduler \
    --display-name="NewsPulse Scheduler"

# Grant the service account permission to invoke Cloud Run
gcloud run services add-iam-policy-binding newspulse-service \
    --region=us-central1 \
    --member="serviceAccount:newspulse-scheduler@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/run.invoker"

# Create Cloud Scheduler job (runs daily at 8 AM)
gcloud scheduler jobs create http newspulse-daily-report \
    --location=us-central1 \
    --schedule="0 8 * * *" \
    --time-zone="America/New_York" \
    --uri="${SERVICE_URL}/generate" \
    --http-method=POST \
    --oidc-service-account-email="newspulse-scheduler@${PROJECT_ID}.iam.gserviceaccount.com" \
    --message-body='{"user_id":"nishantgaurav23"}' \
    --headers="Content-Type=application/json"
```

**Note:** If you don't have a web interface yet, you can trigger reports manually via Cloud Run jobs or HTTP endpoints.

---

## Step 7: Verify Deployment

```bash
# Check deployment status
gcloud run services describe newspulse-service \
    --region us-central1

# View logs
gcloud run services logs read newspulse-service \
    --region us-central1 \
    --limit 50

# Test manual run (if you have an endpoint)
curl -X POST "${SERVICE_URL}/generate" \
    -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
    -H "Content-Type: application/json" \
    -d '{"user_id":"nishantgaurav23"}'
```

---

## Alternative: Run as Cloud Run Job (Simpler for CLI tools)

If you don't need a web interface, use Cloud Run Jobs:

```bash
# Create a Cloud Run Job
gcloud run jobs create newspulse-job \
    --image us-central1-docker.pkg.dev/$PROJECT_ID/newspulse-repo/newspulse-ai:latest \
    --region us-central1 \
    --set-env-vars SMTP_SERVER=smtp.gmail.com \
    --set-env-vars SMTP_PORT=587 \
    --set-env-vars SMTP_USERNAME=your-email@gmail.com \
    --set-secrets GOOGLE_API_KEY=google-api-key:latest \
    --set-secrets GOOGLE_SEARCH_API_KEY=google-search-api-key:latest \
    --set-secrets GOOGLE_SEARCH_ENGINE_ID=google-search-engine-id:latest \
    --set-secrets SMTP_PASSWORD=smtp-password:latest \
    --memory 1Gi \
    --cpu 1 \
    --max-retries 2 \
    --task-timeout 10m \
    --args="python","main.py","generate","nishantgaurav23"

# Execute the job manually
gcloud run jobs execute newspulse-job --region us-central1

# Schedule with Cloud Scheduler
gcloud scheduler jobs create http newspulse-daily-job \
    --location=us-central1 \
    --schedule="0 8 * * *" \
    --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT_ID}/jobs/newspulse-job:run" \
    --http-method=POST \
    --oauth-service-account-email="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
```

---

## Cost Estimation

### Cloud Run (Recommended for CLI tools - Jobs)
- **Pricing**: Pay only when job runs
- **Estimate**: $0.01-$0.05 per report (5-10 minutes runtime)
- **Monthly (daily reports)**: ~$0.30-$1.50/month

### Artifact Registry
- **Storage**: $0.10/GB/month
- **Estimate**: <$0.10/month (images are small)

### Secret Manager
- **Secrets**: $0.06/secret/month
- **Estimate**: ~$0.24/month (4 secrets)

### Cloud Scheduler
- **Jobs**: First 3 jobs free, then $0.10/job/month
- **Estimate**: $0 (only 1 job)

**Total Monthly Cost**: ~$0.50-$2.00/month

---

## Monitoring and Logging

```bash
# View Cloud Run logs
gcloud run services logs read newspulse-service --region us-central1

# Or for Jobs
gcloud run jobs logs read newspulse-job --region us-central1

# Stream logs in real-time
gcloud run services logs tail newspulse-service --region us-central1

# View specific execution
gcloud run jobs executions list --job=newspulse-job --region=us-central1
```

---

## Troubleshooting

### Issue: "Permission denied" errors
**Solution**: Ensure service account has Secret Manager accessor role

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

### Issue: "Container failed to start"
**Solution**: Check environment variables and secrets

```bash
gcloud run services describe newspulse-service --region us-central1
```

### Issue: "Timeout exceeded"
**Solution**: Increase timeout in Cloud Run

```bash
gcloud run services update newspulse-service \
    --region us-central1 \
    --timeout 15m
```

---

## Updating the Deployment

```bash
# Rebuild and push new image
docker build -t newspulse-ai:latest .
docker tag newspulse-ai:latest \
    us-central1-docker.pkg.dev/$PROJECT_ID/newspulse-repo/newspulse-ai:latest
docker push us-central1-docker.pkg.dev/$PROJECT_ID/newspulse-repo/newspulse-ai:latest

# Update the service
gcloud run services update newspulse-service \
    --image us-central1-docker.pkg.dev/$PROJECT_ID/newspulse-repo/newspulse-ai:latest \
    --region us-central1
```

---

## Security Best Practices

1. ✅ **Use Secret Manager** for all sensitive data (API keys, passwords)
2. ✅ **Restrict IAM permissions** to least privilege
3. ✅ **Use service accounts** instead of user credentials
4. ✅ **Enable Cloud Armor** for DDoS protection (if using web interface)
5. ✅ **Rotate secrets** periodically
6. ✅ **Monitor logs** for suspicious activity
7. ✅ **Use VPC** if connecting to internal resources

---

## Next Steps

1. ✅ Deployment complete
2. Test automated report generation
3. Set up monitoring alerts
4. Configure backup and disaster recovery
5. Add more user profiles
6. Scale to multiple users/teams

---

**Need help?** Check [Cloud Run documentation](https://cloud.google.com/run/docs) or file an issue.
