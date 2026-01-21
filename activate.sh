#!/bin/bash
# Activation script for NewsPulse AI

echo "🚀 Setting up NewsPulse AI..."
echo ""

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

echo "✓ Virtual environment activated!"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "You can now run:"
echo "  python main.py create-profile    # Create a user profile"
echo "  python main.py generate <user_id>  # Generate a news report"
echo ""
echo "To deactivate the virtual environment later, run: deactivate"
