# Google Cloud SDK Installation Guide

**Platform:** macOS (detected)

---

## Option 1: Install via Homebrew (Recommended)

```bash
# Install Google Cloud SDK
brew install google-cloud-sdk

# Add gcloud to your PATH (if needed)
echo 'source "$(brew --prefix)/share/google-cloud-sdk/path.bash.inc"' >> ~/.zshrc
echo 'source "$(brew --prefix)/share/google-cloud-sdk/completion.bash.inc"' >> ~/.zshrc

# Reload shell
source ~/.zshrc

# Verify installation
gcloud --version
```

---

## Option 2: Download and Install Manually

```bash
# Download the SDK
curl https://sdk.cloud.google.com | bash

# Restart your shell
exec -l $SHELL

# Initialize gcloud
gcloud init
```

---

## After Installation

### 1. Initialize gcloud
```bash
gcloud init
```

This will:
- Prompt you to log in to your Google account
- Let you select or create a GCP project
- Set default region/zone

### 2. Authenticate
```bash
# Login to GCP
gcloud auth login

# Set application default credentials
gcloud auth application-default login

# Verify authentication
gcloud auth list
```

### 3. Create or Select Project
```bash
# List existing projects
gcloud projects list

# Create new project (if needed)
gcloud projects create YOUR-PROJECT-ID --name="NewsPulse AI"

# Set as default project
gcloud config set project YOUR-PROJECT-ID

# Enable billing (required for Cloud Run)
# Go to: https://console.cloud.google.com/billing
```

---

## Quick Install (All Steps)

```bash
# 1. Install via Homebrew
brew install google-cloud-sdk

# 2. Add to PATH
echo 'source "$(brew --prefix)/share/google-cloud-sdk/path.bash.inc"' >> ~/.zshrc
source ~/.zshrc

# 3. Initialize and authenticate
gcloud init

# 4. Verify
gcloud --version
gcloud auth list
```

---

## Verification

Run these commands to verify installation:

```bash
# Check version
gcloud --version

# Check authentication
gcloud auth list

# Check current project
gcloud config get-value project

# Check current region
gcloud config get-value compute/region
```

---

## Next Steps

After installation and authentication:

```bash
# Run NewsPulse AI deployment
cd /Users/nishantgaurav/Project/agentic-newspulse
./deploy_gcp.sh
```

