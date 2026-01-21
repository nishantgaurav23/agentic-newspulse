#!/bin/bash
# GCP Cloud Run Deployment Script for NewsPulse AI

set -e  # Exit on error

echo "☁️  NewsPulse AI - GCP Deployment Script"
echo "========================================"
echo ""

# Configuration
read -p "Enter your GCP Project ID: " PROJECT_ID
read -p "Enter region (default: us-central1): " REGION
REGION=${REGION:-us-central1}

echo ""
echo "Configuration:"
echo "  Project ID: $PROJECT_ID"
echo "  Region: $REGION"
echo ""

# Confirm
read -p "Continue with deployment? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "❌ Deployment cancelled"
    exit 0
fi

echo ""
echo "🔧 Step 1: Configure gcloud"
gcloud config set project $PROJECT_ID
gcloud config set run/region $REGION

echo ""
echo "🔧 Step 2: Enable required APIs"
gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    secretmanager.googleapis.com \
    cloudscheduler.googleapis.com

echo ""
echo "🔧 Step 3: Create Artifact Registry repository"
gcloud artifacts repositories create newspulse-repo \
    --repository-format=docker \
    --location=$REGION \
    --description="NewsPulse AI container repository" \
    || echo "  (Repository may already exist)"

echo ""
echo "🔧 Step 4: Configure Docker authentication"
gcloud auth configure-docker ${REGION}-docker.pkg.dev

echo ""
echo "🔧 Step 5: Create secrets in Secret Manager"
echo "   You'll need to provide your API keys..."
echo ""

read -p "Enter GOOGLE_API_KEY: " -s GOOGLE_API_KEY
echo ""
read -p "Enter GOOGLE_SEARCH_API_KEY: " -s GOOGLE_SEARCH_API_KEY
echo ""
read -p "Enter GOOGLE_SEARCH_ENGINE_ID: " GOOGLE_SEARCH_ENGINE_ID
echo ""
read -p "Enter SMTP_PASSWORD (Gmail App Password): " -s SMTP_PASSWORD
echo ""

# Create secrets
echo -n "$GOOGLE_API_KEY" | gcloud secrets create google-api-key --data-file=- || \
    echo -n "$GOOGLE_API_KEY" | gcloud secrets versions add google-api-key --data-file=-

echo -n "$GOOGLE_SEARCH_API_KEY" | gcloud secrets create google-search-api-key --data-file=- || \
    echo -n "$GOOGLE_SEARCH_API_KEY" | gcloud secrets versions add google-search-api-key --data-file=-

echo -n "$GOOGLE_SEARCH_ENGINE_ID" | gcloud secrets create google-search-engine-id --data-file=- || \
    echo -n "$GOOGLE_SEARCH_ENGINE_ID" | gcloud secrets versions add google-search-engine-id --data-file=-

echo -n "$SMTP_PASSWORD" | gcloud secrets create smtp-password --data-file=- || \
    echo -n "$SMTP_PASSWORD" | gcloud secrets versions add smtp-password --data-file=-

echo "✅ Secrets created"

echo ""
echo "🔧 Step 6: Grant Secret Manager access"
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')

for SECRET in google-api-key google-search-api-key google-search-engine-id smtp-password; do
    gcloud secrets add-iam-policy-binding $SECRET \
        --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
        --role="roles/secretmanager.secretAccessor" \
        || echo "  (IAM binding may already exist)"
done

echo ""
echo "📦 Step 7: Build and push Docker image"
IMAGE_NAME="${REGION}-docker.pkg.dev/${PROJECT_ID}/newspulse-repo/newspulse-ai:latest"

docker build -t newspulse-ai:latest .
docker tag newspulse-ai:latest $IMAGE_NAME
docker push $IMAGE_NAME

echo "✅ Image pushed: $IMAGE_NAME"

echo ""
echo "🚀 Step 8: Deploy to Cloud Run (Job - recommended for CLI tools)"

read -p "Enter SMTP username (your Gmail): " SMTP_USERNAME

gcloud run jobs create newspulse-job \
    --image $IMAGE_NAME \
    --region $REGION \
    --set-env-vars SMTP_SERVER=smtp.gmail.com \
    --set-env-vars SMTP_PORT=587 \
    --set-env-vars SMTP_USERNAME=$SMTP_USERNAME \
    --set-env-vars MAX_ARTICLES_PER_REPORT=5 \
    --set-env-vars VERIFICATION_MAX_RETRIES=2 \
    --set-env-vars GEMINI_MODEL=models/gemini-2.5-flash \
    --set-secrets GOOGLE_API_KEY=google-api-key:latest \
    --set-secrets GOOGLE_SEARCH_API_KEY=google-search-api-key:latest \
    --set-secrets GOOGLE_SEARCH_ENGINE_ID=google-search-engine-id:latest \
    --set-secrets SMTP_PASSWORD=smtp-password:latest \
    --memory 1Gi \
    --cpu 1 \
    --max-retries 2 \
    --task-timeout 10m \
    --args="python","main.py","generate","nishantgaurav23" \
    || echo "  (Job may already exist - updating...)" && \
    gcloud run jobs update newspulse-job \
        --image $IMAGE_NAME \
        --region $REGION

echo ""
echo "🎉 Deployment Complete!"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Test the Cloud Run Job manually:"
echo "   gcloud run jobs execute newspulse-job --region $REGION"
echo ""
echo "2. Set up automated scheduling (see setup_scheduler.sh)"
echo ""
echo "3. View job executions:"
echo "   gcloud run jobs executions list --job=newspulse-job --region=$REGION"
echo ""
echo "4. View logs:"
echo "   gcloud run jobs logs read newspulse-job --region=$REGION"
echo ""
