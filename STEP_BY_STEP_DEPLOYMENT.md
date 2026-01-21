# 🚀 NewsPulse AI - Complete GCP Deployment Guide
## Step-by-Step Instructions

**Time Required:** ~90 minutes
**Cost:** ~$1-2/month for daily reports

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [ ] Google account (Gmail)
- [ ] Credit/debit card for GCP billing (free trial available)
- [ ] Terminal/command line access
- [ ] Internet connection

---

## STEP 1: Open Terminal and Set Up gcloud

### 1.1 Open Terminal

**On macOS:**
- Press `Cmd + Space`
- Type "Terminal"
- Press Enter

### 1.2 Set Up gcloud Environment

Copy and paste this **entire block** into your terminal and press Enter:

```bash
export CLOUDSDK_CONFIG=$HOME/gcloud-config
export PATH=$HOME/google-cloud-sdk/google-cloud-sdk/bin:$PATH
```

**What this does:** Sets up Google Cloud SDK to use the correct paths.

**Expected output:** None (command runs silently)

### 1.3 Verify gcloud is Installed

```bash
gcloud --version
```

**Expected output:**
```
Google Cloud SDK 552.0.0
core 2026.01.09
```

✅ **Success indicator:** You see a version number

❌ **If you see "command not found":** Run the commands from Step 1.2 again

---

## STEP 2: Authenticate to Google Cloud

### 2.1 Login to Google Cloud

```bash
gcloud auth login
```

**What happens:**
1. Your web browser will open automatically
2. You'll see a Google sign-in page

**Expected output in terminal:**
```
Your browser has been opened to visit:
https://accounts.google.com/o/oauth2/auth?...

Waiting for authentication...
```

### 2.2 In Your Web Browser

1. **Select your Google account** (the one you want to use for GCP)
2. Click **"Allow"** when asked to grant permissions
3. You'll see: **"You are now authenticated with the gcloud CLI!"**
4. **Close the browser tab**

### 2.3 Back in Terminal

**Expected output:**
```
You are now logged in as [your-email@gmail.com].
Your current project is [None].
```

✅ **Success indicator:** Message says "You are now logged in"

### 2.4 Set Application Default Credentials

```bash
gcloud auth application-default login
```

**What happens:** Browser opens again

**In browser:**
1. Click **"Allow"**
2. You'll see: **"Authentication successful"**
3. Close the browser tab

**Expected output in terminal:**
```
Credentials saved to file: [/Users/your-name/gcloud-config/application_default_credentials.json]
```

✅ **Success indicator:** Message says "Credentials saved"

---

## STEP 3: Create GCP Project

### 3.1 Generate a Unique Project ID

```bash
PROJECT_ID="newspulse-ai-$(date +%s)"
echo "Your project ID will be: $PROJECT_ID"
```

**Expected output:**
```
Your project ID will be: newspulse-ai-1737416742
```

📝 **IMPORTANT:** Copy this project ID somewhere - you'll need it later!

**Alternative:** Choose your own project ID:
```bash
PROJECT_ID="my-custom-project-name"
```

**Rules for project ID:**
- Must be unique across all of GCP
- Only lowercase letters, numbers, and hyphens
- Must start with a letter
- 6-30 characters

### 3.2 Create the Project

```bash
gcloud projects create $PROJECT_ID --name="NewsPulse AI"
```

**Expected output:**
```
Create in progress for [https://cloudresourcemanager.googleapis.com/v1/projects/newspulse-ai-1737416742].
Waiting for [operations/cp.12345...] to finish...done.
```

✅ **Success indicator:** Message says "Create in progress" and then "done"

❌ **If you see "already exists":** The project ID is taken. Run Step 3.1 again to generate a new ID.

### 3.3 Set as Default Project

```bash
gcloud config set project $PROJECT_ID
```

**Expected output:**
```
Updated property [core/project].
```

### 3.4 Set Default Region

```bash
gcloud config set compute/region us-central1
```

**Expected output:**
```
Updated property [compute/region].
```

**Other region options:**
- `us-east1` (South Carolina)
- `us-west1` (Oregon)
- `europe-west1` (Belgium)
- `asia-south1` (Mumbai)

### 3.5 Verify Configuration

```bash
gcloud config list
```

**Expected output:**
```
[compute]
region = us-central1
[core]
account = your-email@gmail.com
disable_usage_reporting = False
project = newspulse-ai-1737416742
```

✅ **Success indicator:** You see your project ID and email

---

## STEP 4: Enable Billing (REQUIRED)

**Cost:** Free trial gives $300 credit. NewsPulse AI costs ~$1-2/month.

### 4.1 Open Billing Page

**Option A - From Terminal:**
```bash
echo "https://console.cloud.google.com/billing/linkedaccount?project=$PROJECT_ID"
```

Copy the URL and open it in your browser.

**Option B - Direct Link:**
Open: https://console.cloud.google.com/billing

### 4.2 In Your Browser (Google Cloud Console)

1. **If you're new to GCP:**
   - Click **"Activate Free Trial"** or **"Get Started for Free"**
   - Enter credit/debit card information
   - Click **"Start my free trial"**

2. **If you have an existing billing account:**
   - Click **"Link a billing account"**
   - Select your billing account
   - Click **"Set account"**

3. **Verify billing is enabled:**
   - Go to: https://console.cloud.google.com/billing
   - You should see your project listed with "Billing enabled" ✅

✅ **Success indicator:** Project shows "Billing enabled"

❌ **If stuck:** Google Cloud requires billing for Cloud Run, but you won't be charged during free trial ($300 credit)

---

## STEP 5: Navigate to Project Directory

```bash
cd /Users/nishantgaurav/Project/agentic-newspulse
```

**Expected output:** None (changes directory silently)

**Verify you're in the right place:**
```bash
ls -la deploy_gcp.sh
```

**Expected output:**
```
-rwxr-xr-x  1 nishantgaurav  staff  XXXX Jan 20 XX:XX deploy_gcp.sh
```

---

## STEP 6: Prepare Your API Keys

You'll need these API keys. Let me show you how to get each one.

### 6.1 Get Google AI Studio API Key

**Open:** https://aistudio.google.com/

**Steps:**
1. Click **"Get API Key"** (top right)
2. Select your project (newspulse-ai-XXXXX) or create new
3. Click **"Create API Key"**
4. **Copy the key** (looks like: `AIzaSy...`)

📝 **SAVE THIS:** Paste it somewhere safe (Notes app, text file)

### 6.2 Get Google Custom Search API Key

**Open:** https://console.cloud.google.com/apis/credentials

**Steps:**
1. Select your project (newspulse-ai-XXXXX)
2. Click **"+ CREATE CREDENTIALS"**
3. Select **"API key"**
4. **Copy the key** (looks like: `AIzaSy...`)
5. Click **"RESTRICT KEY"** (optional but recommended)
   - Under "API restrictions", select "Restrict key"
   - Search for "Custom Search API"
   - Click "Save"

📝 **SAVE THIS:** Paste it somewhere safe

### 6.3 Get Google Search Engine ID

**Open:** https://programmablesearchengine.google.com/

**Steps:**
1. Click **"Add"** or **"Get Started"**
2. **What to search:** Enter `*` (asterisk - means search entire web)
3. **Name of search engine:** Enter "NewsPulse Search"
4. Click **"Create"**
5. Click **"Customize"** next to your new search engine
6. In "Basic" tab, find **"Search engine ID"** (looks like: `e0123456789abcdef`)
7. **Copy the ID**

📝 **SAVE THIS:** Paste it somewhere safe

### 6.4 Enable Custom Search API

**Open:** https://console.cloud.google.com/apis/library/customsearch.googleapis.com

**Steps:**
1. Select your project
2. Click **"ENABLE"**
3. Wait for confirmation (takes ~30 seconds)

### 6.5 Get Gmail App Password

**Open:** https://myaccount.google.com/apppasswords

**Steps:**
1. **If you don't have 2-Step Verification:**
   - Click "Get Started" for 2-Step Verification
   - Follow the setup wizard (takes 5 minutes)
   - Then return to App Passwords page

2. **Create App Password:**
   - Enter app name: **"NewsPulse AI"**
   - Click **"Create"**
   - You'll see a 16-character password (like: `abcd efgh ijkl mnop`)
   - **Copy this password** (remove spaces: `abcdefghijklmnop`)

📝 **SAVE THIS:** Paste it somewhere safe

**⚠️ IMPORTANT:** This is NOT your regular Gmail password. It's a special password for apps.

---

## STEP 7: Update Your .env File

### 7.1 Open .env File

```bash
nano .env
```

**If file doesn't exist:**
```bash
cp .env.example .env
nano .env
```

### 7.2 Update the File

You'll see something like this:

```
GOOGLE_API_KEY=your-google-api-key-here
GOOGLE_SEARCH_API_KEY=your-google-search-api-key-here
GOOGLE_SEARCH_ENGINE_ID=your-search-engine-id-here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password-here
```

**Replace with YOUR values:**

```
GOOGLE_API_KEY=AIzaSy[paste your AI Studio API key here]
GOOGLE_SEARCH_API_KEY=AIzaSy[paste your Custom Search API key here]
GOOGLE_SEARCH_ENGINE_ID=[paste your Search Engine ID here]
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=[YOUR actual Gmail address]
SMTP_PASSWORD=[paste your 16-char Gmail app password]
```

**Example (with fake values):**
```
GOOGLE_API_KEY=AIzaSyABC123XYZ789
GOOGLE_SEARCH_API_KEY=AIzaSyDEF456UVW012
GOOGLE_SEARCH_ENGINE_ID=a1b2c3d4e5f6g7h8i
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=myemail@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
```

### 7.3 Save the File

**In nano editor:**
1. Press `Ctrl + X` to exit
2. Press `Y` to save
3. Press `Enter` to confirm filename

### 7.4 Verify .env File

```bash
cat .env | grep -E "GOOGLE_API_KEY|SMTP_USERNAME"
```

**Expected output:**
```
GOOGLE_API_KEY=AIzaSy...
SMTP_USERNAME=your-email@gmail.com
```

✅ **Success indicator:** You see your actual values (not "your-xxx-here")

---

## STEP 8: Update Your Profile Email Addresses

### 8.1 Open Profile File

```bash
nano data/user_profiles/nishantgaurav23.json
```

### 8.2 Update Email Addresses

**Find these lines:**
```json
  "delivery_email": "primary.user@gmail.com",
  "cc_emails": [
    "team.member1@gmail.com",
    "team.member2@gmail.com"
  ],
  "bcc_emails": [
    "archive@company.com"
  ],
```

**Replace with YOUR actual email addresses:**

```json
  "delivery_email": "your-primary-email@gmail.com",
  "cc_emails": [
    "second-recipient@gmail.com",
    "third-recipient@gmail.com"
  ],
  "bcc_emails": [
    "fourth-recipient@company.com"
  ],
```

**Example:**
```json
  "delivery_email": "myemail@gmail.com",
  "cc_emails": [
    "friend@gmail.com",
    "colleague@gmail.com"
  ],
  "bcc_emails": [
    "work@company.com"
  ],
```

**Notes:**
- `delivery_email` = Primary recipient (TO)
- `cc_emails` = Recipients who can see each other
- `bcc_emails` = Hidden recipients (good for archiving)
- You can have 1-10 recipients in each category
- Remove entries if you don't want CC or BCC

### 8.3 Save the File

1. Press `Ctrl + X`
2. Press `Y`
3. Press `Enter`

---

## STEP 9: Run GCP Deployment Script

### 9.1 Make Sure Environment is Set

```bash
export CLOUDSDK_CONFIG=$HOME/gcloud-config
export PATH=$HOME/google-cloud-sdk/google-cloud-sdk/bin:$PATH
```

### 9.2 Make Script Executable

```bash
chmod +x deploy_gcp.sh
```

### 9.3 Run Deployment

```bash
./deploy_gcp.sh
```

### 9.4 Follow the Prompts

The script will ask you questions. Here's what to enter:

**Prompt 1: GCP Project ID**
```
Enter your GCP project ID: 
```
**Enter:** Your project ID from Step 3.1 (e.g., `newspulse-ai-1737416742`)

**Prompt 2: Region**
```
Enter GCP region [us-central1]: 
```
**Enter:** Press `Enter` to use default (us-central1) or type different region

**Prompt 3: Confirmation**
```
Deploy NewsPulse AI to GCP? (yes/no): 
```
**Enter:** `yes`

**Prompt 4-9: API Keys and Credentials**

The script will ask for each secret. **Paste the values you saved in Step 6:**

```
Enter GOOGLE_API_KEY: 
```
**Paste:** Your AI Studio API key

```
Enter GOOGLE_SEARCH_API_KEY: 
```
**Paste:** Your Custom Search API key

```
Enter GOOGLE_SEARCH_ENGINE_ID: 
```
**Paste:** Your Search Engine ID

```
Enter SMTP_USERNAME: 
```
**Type:** Your Gmail address

```
Enter SMTP_PASSWORD: 
```
**Paste:** Your 16-character Gmail app password

### 9.5 Wait for Deployment

**Expected duration:** 20-30 minutes

**What you'll see:**
```
☁️  NewsPulse AI - GCP Deployment Script
========================================

Configuration:
  Project ID: newspulse-ai-1737416742
  Region: us-central1

🔧 Step 1: Configure gcloud
✅ gcloud configured

🔧 Step 2: Enable required APIs
Operation "operations/..." finished successfully.
✅ APIs enabled

🔧 Step 3: Create Artifact Registry
Created repository [newspulse-repo].
✅ Artifact Registry created

🔧 Step 4: Configure Docker authentication
✅ Docker configured for Artifact Registry

🔧 Step 5: Create secrets in Secret Manager
Created version [1] of the secret [google-api-key].
Created version [1] of the secret [google-search-api-key].
Created version [1] of the secret [google-search-engine-id].
Created version [1] of the secret [smtp-username].
Created version [1] of the secret [smtp-password].
✅ Secrets created

🔧 Step 6: Grant IAM permissions
✅ IAM permissions granted

🔧 Step 7: Build Docker image
... [many lines of build output] ...
✅ Docker image built

🔧 Step 8: Push image to Artifact Registry
The push refers to repository [us-central1-docker.pkg.dev/...]
✅ Image pushed to registry

🔧 Step 9: Create Cloud Run Job
✅ Cloud Run Job created: newspulse-job

🎉 Deployment Complete!
```

✅ **Success indicator:** Final message says "🎉 Deployment Complete!"

---

## STEP 10: Test the Deployment

### 10.1 Manually Execute the Job

```bash
gcloud run jobs execute newspulse-job --region us-central1
```

**Expected output:**
```
✓ Executing job [newspulse-job]...
  ✓ Creating execution [newspulse-job-xxxxx]...
  . Running...
```

**Wait time:** 3-5 minutes

### 10.2 Check Execution Status

```bash
gcloud run jobs executions list --job=newspulse-job --region=us-central1 --limit=1
```

**Expected output:**
```
EXECUTION              STATUS      STARTED                 COMPLETED
newspulse-job-xxxxx    Succeeded   2026-01-21 10:00:00     2026-01-21 10:04:30
```

✅ **Success indicator:** STATUS shows "Succeeded"

### 10.3 Check Your Email

**Wait 5 minutes, then check:**
- [ ] Primary email inbox (delivery_email)
- [ ] CC email inboxes
- [ ] BCC email inbox

**Look for:** Email with subject "NewsPulse AI Report - [Date]"

✅ **Success indicator:** All recipients received the email

---

## STEP 11: Set Up Daily Automation

### 11.1 Run Scheduler Setup Script

```bash
chmod +x setup_scheduler.sh
./setup_scheduler.sh
```

### 11.2 Follow Prompts

**Prompt 1: Project ID**
```
Enter your GCP project ID:
```
**Enter:** Same project ID as before

**Prompt 2: Region**
```
Enter GCP region [us-central1]:
```
**Enter:** Press `Enter` for default

**Prompt 3: Schedule Time**
```
Enter schedule time (HH:MM) [08:00]:
```
**Enter:** `08:00` (or your preferred time in 24-hour format)

**Prompt 4: Timezone**
```
Enter timezone [Asia/Kolkata]:
```
**Enter:** Press `Enter` for Asia/Kolkata or type your timezone
- `America/New_York` (EST)
- `America/Los_Angeles` (PST)
- `Europe/London` (GMT)
- Full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

**Prompt 5: Confirmation**
```
Set up Cloud Scheduler? (yes/no):
```
**Enter:** `yes`

### 11.3 Verify Scheduler

```bash
gcloud scheduler jobs describe newspulse-daily-report --location=us-central1
```

**Expected output:**
```
name: projects/.../locations/us-central1/jobs/newspulse-daily-report
schedule: 0 8 * * *
state: ENABLED
timeZone: Asia/Kolkata
```

✅ **Success indicator:** Shows your schedule and state is "ENABLED"

---

## STEP 12: Set Up GitHub Actions (Optional)

This enables automatic deployment when you push code to GitHub.

### 12.1 Create Service Account for GitHub

```bash
export PROJECT_ID=$(gcloud config get-value project)
SA_NAME="github-actions-deployer"

gcloud iam service-accounts create ${SA_NAME} \
    --display-name="GitHub Actions Deployer" \
    --project=${PROJECT_ID}
```

### 12.2 Grant Permissions

```bash
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

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
```

### 12.3 Create and Download Key

```bash
gcloud iam service-accounts keys create github-actions-key.json \
    --iam-account=${SA_EMAIL}

echo "✅ Service account key created!"
echo "📁 File: github-actions-key.json"
```

### 12.4 View the Key

```bash
cat github-actions-key.json
```

**Copy the ENTIRE output** (including the curly braces `{}`)

### 12.5 Add to GitHub Secrets

**Open:** https://github.com/nishantgaurav23/agentic-newspulse/settings/secrets/actions

**Add 3 secrets:**

**Secret 1: GCP_PROJECT_ID**
- Click **"New repository secret"**
- Name: `GCP_PROJECT_ID`
- Value: Your project ID (e.g., `newspulse-ai-1737416742`)
- Click **"Add secret"**

**Secret 2: GCP_REGION**
- Click **"New repository secret"**
- Name: `GCP_REGION`
- Value: `us-central1` (or your region)
- Click **"Add secret"**

**Secret 3: GCP_SA_KEY**
- Click **"New repository secret"**
- Name: `GCP_SA_KEY`
- Value: **Paste the ENTIRE contents** of github-actions-key.json
- Click **"Add secret"**

### 12.6 Delete the Key File (Security)

```bash
rm github-actions-key.json
echo "✅ Key file deleted for security"
```

### 12.7 Test GitHub Actions

```bash
cd /Users/nishantgaurav/Project/agentic-newspulse
echo "# Test deployment" >> README.md
git add README.md
git commit -m "Test: GitHub Actions deployment"
git push origin main
```

**Check deployment:**
Open: https://github.com/nishantgaurav23/agentic-newspulse/actions

You should see a workflow running!

---

## ✅ Success! You're Done!

### What Happens Now

1. **Daily Reports:** Every day at 8:00 AM (your timezone), NewsPulse AI will:
   - Generate a personalized news report
   - Send it to all your configured email addresses
   - Save the report to history

2. **Auto-Deployment:** When you push code to GitHub:
   - GitHub Actions automatically builds new Docker image
   - Deploys to Cloud Run
   - Your changes are live in ~5 minutes

3. **Manual Execution:** Run anytime with:
   ```bash
   gcloud run jobs execute newspulse-job --region us-central1
   ```

### Cost

- **Daily reports:** ~$0.02-$0.05 per day
- **Monthly:** ~$1-2/month
- **Your free trial:** $300 credit lasts ~10-15 years at this rate!

### Monitoring

**View logs:**
```bash
gcloud run jobs logs read newspulse-job --region us-central1 --limit 100
```

**View executions:**
```bash
gcloud run jobs executions list --job=newspulse-job --region us-central1
```

**View in browser:**
https://console.cloud.google.com/run/jobs

---

## 🎉 Congratulations!

Your NewsPulse AI system is now:
- ✅ Deployed to Google Cloud Platform
- ✅ Running automatically every day
- ✅ Sending reports to multiple recipients
- ✅ Auto-deploying on code changes

Enjoy your personalized news reports! 🚀

---

## 📞 Need Help?

**Common Issues:**

**Billing error?**
- Verify billing at: https://console.cloud.google.com/billing

**Job fails?**
- Check logs: `gcloud run jobs logs read newspulse-job --region us-central1`

**No email received?**
- Verify SMTP credentials in Secret Manager
- Check spam folder
- Verify profile email addresses

**GitHub Actions fails?**
- Check secrets are set correctly
- Verify service account has permissions

**Documentation:**
- Full guide: `README.md`
- Architecture: `ARCHITECTURE.md`
- Troubleshooting: `DEPLOYMENT_CHECKLIST.md`

