#!/bin/bash
# Cloud Scheduler Setup Script for NewsPulse AI
# Automates daily report generation

set -e  # Exit on error

echo "⏰ NewsPulse AI - Cloud Scheduler Setup"
echo "======================================="
echo ""

# Configuration
read -p "Enter your GCP Project ID: " PROJECT_ID
read -p "Enter region (default: us-central1): " REGION
REGION=${REGION:-us-central1}

echo ""
read -p "Enter schedule time (HH:MM in 24-hour format, default: 08:00): " SCHEDULE_TIME
SCHEDULE_TIME=${SCHEDULE_TIME:-08:00}

read -p "Enter timezone (default: Asia/Kolkata): " TIMEZONE
TIMEZONE=${TIMEZONE:-Asia/Kolkata}

# Convert time to cron format
HOUR=$(echo $SCHEDULE_TIME | cut -d: -f1)
MINUTE=$(echo $SCHEDULE_TIME | cut -d: -f2)
CRON_SCHEDULE="$MINUTE $HOUR * * *"

echo ""
echo "Configuration:"
echo "  Project ID: $PROJECT_ID"
echo "  Region: $REGION"
echo "  Schedule: $SCHEDULE_TIME ($TIMEZONE)"
echo "  Cron: $CRON_SCHEDULE"
echo ""

read -p "Continue? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "❌ Setup cancelled"
    exit 0
fi

echo ""
echo "🔧 Setting up Cloud Scheduler..."

gcloud config set project $PROJECT_ID

# Get project number for service account
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

echo ""
echo "🔧 Grant Cloud Run invoker permission..."
gcloud run jobs add-iam-policy-binding newspulse-job \
    --region=$REGION \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/run.invoker" \
    || echo "  (Permission may already exist)"

echo ""
echo "🔧 Creating Cloud Scheduler job..."

# Create the scheduler job
gcloud scheduler jobs create http newspulse-daily-report \
    --location=$REGION \
    --schedule="$CRON_SCHEDULE" \
    --time-zone="$TIMEZONE" \
    --uri="https://${REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT_ID}/jobs/newspulse-job:run" \
    --http-method=POST \
    --oauth-service-account-email="$SERVICE_ACCOUNT" \
    --description="Daily NewsPulse AI report generation" \
    || gcloud scheduler jobs update http newspulse-daily-report \
        --location=$REGION \
        --schedule="$CRON_SCHEDULE" \
        --time-zone="$TIMEZONE"

echo ""
echo "✅ Cloud Scheduler configured!"
echo ""
echo "📋 Scheduler Details:"
echo "  Job Name: newspulse-daily-report"
echo "  Schedule: Every day at $SCHEDULE_TIME ($TIMEZONE)"
echo "  Next Run: Check with command below"
echo ""
echo "📋 Useful Commands:"
echo ""
echo "1. View scheduler job:"
echo "   gcloud scheduler jobs describe newspulse-daily-report --location=$REGION"
echo ""
echo "2. Manually trigger the job:"
echo "   gcloud scheduler jobs run newspulse-daily-report --location=$REGION"
echo ""
echo "3. View scheduler logs:"
echo "   gcloud logging read 'resource.type=cloud_scheduler_job AND resource.labels.job_id=newspulse-daily-report' --limit 50"
echo ""
echo "4. Pause scheduler:"
echo "   gcloud scheduler jobs pause newspulse-daily-report --location=$REGION"
echo ""
echo "5. Resume scheduler:"
echo "   gcloud scheduler jobs resume newspulse-daily-report --location=$REGION"
echo ""
echo "6. Delete scheduler:"
echo "   gcloud scheduler jobs delete newspulse-daily-report --location=$REGION"
echo ""
echo "🎉 Setup complete! Your reports will be generated daily at $SCHEDULE_TIME."
