#!/bin/bash
# Docker Testing Script for NewsPulse AI

set -e  # Exit on error

echo "🐳 NewsPulse AI - Docker Testing Script"
echo "========================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running!"
    echo "   Please start Docker Desktop and try again."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Build the image
echo "📦 Building Docker image..."
docker build -t newspulse-ai:latest .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Docker build failed"
    exit 1
fi
echo ""

# Test 1: List profiles
echo "🧪 Test 1: List user profiles"
docker run --rm --env-file .env newspulse-ai:latest python main.py list

if [ $? -eq 0 ]; then
    echo "✅ Profile listing works"
else
    echo "❌ Profile listing failed"
fi
echo ""

# Test 2: Generate test report (no delivery)
echo "🧪 Test 2: Generate test report (no email delivery)"
echo "   This will take 3-5 minutes..."
docker run --rm \
    --env-file .env \
    -v $(pwd)/data:/app/data \
    newspulse-ai:latest \
    python main.py generate nishantgaurav23 --no-deliver

if [ $? -eq 0 ]; then
    echo "✅ Test report generation works"
else
    echo "❌ Test report generation failed"
fi
echo ""

# Test 3: Check image size
echo "📊 Docker Image Info:"
docker images newspulse-ai:latest --format "Size: {{.Size}}"
echo ""

echo "🎉 Docker testing complete!"
echo ""
echo "Next steps:"
echo "  1. Review the test report output above"
echo "  2. Generate and send a real report:"
echo "     docker run --rm --env-file .env -v \$(pwd)/data:/app/data newspulse-ai python main.py generate nishantgaurav23"
echo "  3. Deploy to GCP (see GCP_DEPLOYMENT_GUIDE.md)"
