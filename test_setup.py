#!/usr/bin/env python3
"""
Test setup script for NewsPulse AI
Creates a demo profile and validates configuration
"""
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

def test_configuration():
    """Test that configuration is loaded correctly"""
    print("🔍 Testing configuration...")

    try:
        from config import settings

        if not settings:
            print("❌ Settings could not be loaded")
            return False

        print(f"✓ Settings loaded successfully")
        print(f"  - Model: {settings.gemini_model}")
        print(f"  - Max articles: {settings.max_articles_per_report}")

        # Validate API keys
        try:
            settings.validate_api_keys()
            print("✓ All API keys are configured")
            return True
        except ValueError as e:
            print(f"❌ API key validation failed: {e}")
            return False

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_demo_profile():
    """Create a demo user profile"""
    print("\n📝 Creating demo user profile...")

    try:
        from core.orchestrator import NewsPulseOrchestrator

        orchestrator = NewsPulseOrchestrator()

        # Create a demo profile
        profile = orchestrator.create_user_profile(
            user_id="demo_user",
            name="Demo User",
            role="Technology Executive",
            company="Demo Corporation",
            industry="Technology",
            topics_of_interest=[
                "Artificial Intelligence",
                "Machine Learning",
                "Cloud Computing",
                "Cybersecurity",
                "Digital Transformation"
            ],
            delivery_email="demo@example.com"
        )

        print(f"✓ Profile created successfully!")
        print(f"  - User ID: {profile.user_id}")
        print(f"  - Name: {profile.name}")
        print(f"  - Role: {profile.role}")
        print(f"  - Topics: {len(profile.topics_of_interest)}")

        return True

    except Exception as e:
        print(f"❌ Profile creation error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    print("=" * 60)
    print("NewsPulse AI - Setup Test")
    print("=" * 60)
    print()

    # Test 1: Configuration
    config_ok = test_configuration()

    if not config_ok:
        print("\n❌ Setup test failed: Configuration issues")
        print("\nPlease check your .env file and ensure all API keys are set.")
        return 1

    # Test 2: Create demo profile
    profile_ok = create_demo_profile()

    if not profile_ok:
        print("\n❌ Setup test failed: Could not create profile")
        return 1

    # Success!
    print("\n" + "=" * 60)
    print("✅ Setup test completed successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Generate a report: python main.py generate demo_user --no-deliver")
    print("  2. Create your own profile: python main.py create-profile")
    print("  3. View all profiles: python main.py list")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
