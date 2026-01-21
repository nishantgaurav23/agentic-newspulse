#!/usr/bin/env python3
"""
Create a custom profile - Edit this file with your preferences
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from core.orchestrator import NewsPulseOrchestrator


def create_custom_profile():
    """Create a profile - EDIT THE VALUES BELOW"""

    # ============= EDIT YOUR DETAILS HERE =============

    USER_ID = "nishantgaurav23"  # Your username
    NAME = "Nishant Gaurav"
    ROLE = "Data Scientist"  # Your role
    COMPANY = "Turing Global India Private Limited"
    INDUSTRY = "Technology"
    EMAIL = "primary.user@gmail.com"  # Your email from .env

    # Topics you want to track
    TOPICS = [
        "Artificial Intelligence",
        "Machine Learning",
        "Software Development",
        "Cloud Computing",
        "Python",
        "React",
        "DevOps"
    ]

    # Topics to avoid (optional)
    EXCLUDED_TOPICS = [
        "Celebrity News",
        "Sports"
    ]

    # Preferred news sources (optional)
    PREFERRED_SOURCES = [
        "techcrunch.com",
        "arstechnica.com",
        "theverge.com",
        "hacker news"
    ]

    DELIVERY_TIME = "08:00"  # When to receive reports (HH:MM)
    TIMEZONE = "Asia/Kolkata"  # Your timezone

    # ============= END OF EDITABLE SECTION =============

    print("=" * 60)
    print("Creating Custom Profile")
    print("=" * 60)
    print()

    orchestrator = NewsPulseOrchestrator()

    try:
        profile = orchestrator.create_user_profile(
            user_id=USER_ID,
            name=NAME,
            role=ROLE,
            company=COMPANY,
            industry=INDUSTRY,
            topics_of_interest=TOPICS,
            excluded_topics=EXCLUDED_TOPICS,
            preferred_sources=PREFERRED_SOURCES,
            delivery_email=EMAIL,
            delivery_time=DELIVERY_TIME,
            timezone=TIMEZONE
        )

        print("✅ Profile created successfully!")
        print()
        print(f"User ID: {profile.user_id}")
        print(f"Name: {profile.name}")
        print(f"Topics: {len(profile.topics_of_interest)}")
        print()
        print("Next steps:")
        print(f"  python main.py generate {USER_ID} --no-deliver")
        print()

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(create_custom_profile())