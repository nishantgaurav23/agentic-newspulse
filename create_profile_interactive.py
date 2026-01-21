#!/usr/bin/env python3
"""
Interactive Profile Creator for NewsPulse AI
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from core.orchestrator import NewsPulseOrchestrator


def main():
    """Interactive profile creation"""
    print("=" * 60)
    print("NewsPulse AI - Create Your Profile")
    print("=" * 60)
    print()

    orchestrator = NewsPulseOrchestrator()

    # Basic Information
    print("📋 BASIC INFORMATION")
    print("-" * 60)
    user_id = input("User ID (e.g., your_name): ").strip()

    if not user_id:
        print("❌ User ID is required!")
        return 1

    # Check if profile already exists
    from models.user_profile import UserProfileManager
    manager = UserProfileManager()
    existing = manager.load_profile(user_id)

    if existing:
        overwrite = input(f"⚠️  Profile '{user_id}' already exists. Overwrite? (yes/no): ").strip().lower()
        if overwrite != 'yes':
            print("Cancelled.")
            return 0

    name = input("Full Name: ").strip() or "User"
    role = input("Your Role (e.g., CEO, CTO, VP): ").strip() or "Executive"
    company = input("Company: ").strip() or "Company"
    industry = input("Industry: ").strip() or "Technology"
    email = input("Email (for reports): ").strip()

    if not email:
        print("❌ Email is required!")
        return 1

    print()
    print("📰 TOPICS OF INTEREST")
    print("-" * 60)
    print("Enter topics you want to track (one per line, empty line to finish):")
    print("Examples: Artificial Intelligence, Fintech, Cloud Computing, etc.")
    print()

    topics = []
    while True:
        topic = input(f"  Topic {len(topics) + 1}: ").strip()
        if not topic:
            break
        topics.append(topic)

    if not topics:
        print("⚠️  No topics entered. Using defaults: AI, Technology")
        topics = ["Artificial Intelligence", "Technology Trends"]

    print()
    print("🚫 EXCLUDED TOPICS (Optional)")
    print("-" * 60)
    print("Topics to exclude (one per line, empty line to finish):")

    excluded_topics = []
    while True:
        topic = input(f"  Exclude {len(excluded_topics) + 1}: ").strip()
        if not topic:
            break
        excluded_topics.append(topic)

    print()
    print("📰 PREFERRED NEWS SOURCES (Optional)")
    print("-" * 60)
    print("Preferred sources (e.g., bloomberg.com, techcrunch.com):")
    print("One per line, empty line to finish:")

    preferred_sources = []
    while True:
        source = input(f"  Source {len(preferred_sources) + 1}: ").strip()
        if not source:
            break
        preferred_sources.append(source)

    print()
    print("⏰ DELIVERY PREFERENCES")
    print("-" * 60)
    delivery_time = input("Delivery time (HH:MM, e.g., 08:00): ").strip() or "08:00"
    timezone = input("Timezone (e.g., America/New_York): ").strip() or "America/New_York"

    print()
    print("📧 ADDITIONAL RECIPIENTS (Optional)")
    print("-" * 60)
    print("CC emails (visible to all, one per line, empty to finish):")
    cc_emails = []
    while True:
        cc_email = input(f"  CC {len(cc_emails) + 1}: ").strip()
        if not cc_email:
            break
        cc_emails.append(cc_email)

    print("\nBCC emails (hidden from others, one per line, empty to finish):")
    bcc_emails = []
    while True:
        bcc_email = input(f"  BCC {len(bcc_emails) + 1}: ").strip()
        if not bcc_email:
            break
        bcc_emails.append(bcc_email)

    print()
    print("=" * 60)
    print("CREATING PROFILE...")
    print("=" * 60)

    try:
        profile = orchestrator.create_user_profile(
            user_id=user_id,
            name=name,
            role=role,
            company=company,
            industry=industry,
            topics_of_interest=topics,
            excluded_topics=excluded_topics,
            preferred_sources=preferred_sources,
            delivery_email=email,
            cc_emails=cc_emails,
            bcc_emails=bcc_emails,
            delivery_time=delivery_time,
            timezone=timezone
        )

        print()
        print("✅ Profile created successfully!")
        print()
        print("📋 PROFILE SUMMARY")
        print("-" * 60)
        print(f"User ID: {profile.user_id}")
        print(f"Name: {profile.name}")
        print(f"Role: {profile.role}")
        print(f"Company: {profile.company}")
        print(f"Industry: {profile.industry}")
        print(f"Email: {profile.delivery_email}")
        print(f"Delivery Time: {profile.delivery_time} ({profile.timezone})")
        print()
        print(f"Topics of Interest ({len(profile.topics_of_interest)}):")
        for topic in profile.topics_of_interest:
            print(f"  • {topic}")

        if profile.excluded_topics:
            print(f"\nExcluded Topics ({len(profile.excluded_topics)}):")
            for topic in profile.excluded_topics:
                print(f"  • {topic}")

        if profile.preferred_sources:
            print(f"\nPreferred Sources ({len(profile.preferred_sources)}):")
            for source in profile.preferred_sources:
                print(f"  • {source}")

        print()
        print("=" * 60)
        print("NEXT STEPS")
        print("=" * 60)
        print(f"Generate a test report:")
        print(f"  python main.py generate {user_id} --no-deliver")
        print()
        print(f"Generate and send via email:")
        print(f"  python main.py generate {user_id}")
        print()

        return 0

    except Exception as e:
        print(f"\n❌ Error creating profile: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
