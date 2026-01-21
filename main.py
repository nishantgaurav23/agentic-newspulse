#!/usr/bin/env python3
"""
NewsPulse AI - Main Entry Point
Self-Correcting AI Analyst for Executives

Usage:
    python main.py create-profile    # Create a new user profile
    python main.py generate <user_id>  # Generate report for a user
    python main.py feedback <report_id> <user_id> <rating>  # Submit feedback
"""
import asyncio
import sys
import argparse
from datetime import datetime

from core.orchestrator import NewsPulseOrchestrator
from agents.feedback_agent import collect_feedback
from models.user_profile import UserProfileManager


def create_profile_interactive():
    """Interactive user profile creation"""
    print("\n=== NewsPulse AI - Create User Profile ===\n")

    user_id = input("User ID (e.g., john_doe): ").strip()
    name = input("Full Name: ").strip()
    role = input("Role (e.g., CEO, CTO, VP Marketing): ").strip()
    company = input("Company: ").strip()
    industry = input("Industry: ").strip()
    delivery_email = input("Email for delivery: ").strip()

    print("\nTopics of Interest (enter one per line, empty line to finish):")
    topics = []
    while True:
        topic = input("  - ").strip()
        if not topic:
            break
        topics.append(topic)

    print("\nOptional: Preferred sources (enter one per line, empty line to finish):")
    preferred_sources = []
    while True:
        source = input("  - ").strip()
        if not source:
            break
        preferred_sources.append(source)

    orchestrator = NewsPulseOrchestrator()
    profile = orchestrator.create_user_profile(
        user_id=user_id,
        name=name,
        role=role,
        company=company,
        industry=industry,
        topics_of_interest=topics,
        delivery_email=delivery_email,
        preferred_sources=preferred_sources,
    )

    print(f"\n✓ Profile created successfully for {name} ({user_id})")
    print(f"  Topics: {', '.join(topics)}")
    print(f"  Delivery: {delivery_email}")


async def generate_report(user_id: str, deliver: bool = True):
    """Generate a report for a user"""
    print(f"\n=== NewsPulse AI - Generating Report for {user_id} ===\n")

    orchestrator = NewsPulseOrchestrator()

    try:
        report = await orchestrator.generate_report(user_id, deliver=deliver)

        print(f"\n✓ Report generated successfully!")
        print(f"  Report ID: {report.report_id}")
        print(f"  Articles: {report.total_articles}")
        print(f"  Topics: {', '.join(report.topics_covered)}")

        if deliver:
            print(f"  Status: Delivered via email")
        else:
            print(f"  Status: Generated but not delivered")

        return report

    except Exception as e:
        print(f"\n✗ Error generating report: {e}")
        raise


async def submit_feedback(report_id: str, user_id: str, rating: int):
    """Submit feedback for a report"""
    print(f"\n=== NewsPulse AI - Submit Feedback ===\n")

    feedback_text = input("Feedback text (optional): ").strip() or None

    print("\nLiked topics (comma-separated, optional): ")
    liked_input = input().strip()
    liked_topics = [t.strip() for t in liked_input.split(",")] if liked_input else []

    print("Disliked topics (comma-separated, optional): ")
    disliked_input = input().strip()
    disliked_topics = (
        [t.strip() for t in disliked_input.split(",")] if disliked_input else []
    )

    print("Missing topics (comma-separated, optional): ")
    missing_input = input().strip()
    missing_topics = (
        [t.strip() for t in missing_input.split(",")] if missing_input else []
    )

    too_long = input("Was the report too long? (y/n): ").strip().lower() == "y"
    too_short = input("Was the report too short? (y/n): ").strip().lower() == "y"

    feedback = collect_feedback(
        report_id=report_id,
        user_id=user_id,
        rating=rating,
        feedback_text=feedback_text,
        liked_topics=liked_topics,
        disliked_topics=disliked_topics,
        too_long=too_long,
        too_short=too_short,
        missing_topics=missing_topics,
    )

    orchestrator = NewsPulseOrchestrator()
    result = await orchestrator.process_feedback(feedback)

    print(f"\n✓ Feedback processed successfully!")
    print(f"  Summary: {result['summary']}")


def list_profiles():
    """List all user profiles"""
    manager = UserProfileManager()
    profiles = manager.list_profiles()

    print("\n=== User Profiles ===\n")
    if not profiles:
        print("No profiles found.")
    else:
        for user_id in profiles:
            profile = manager.load_profile(user_id)
            print(f"  - {user_id}: {profile.name} ({profile.role} at {profile.company})")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="NewsPulse AI - Self-Correcting AI Analyst for Executives"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Create profile command
    subparsers.add_parser("create-profile", help="Create a new user profile")

    # Generate report command
    generate_parser = subparsers.add_parser(
        "generate", help="Generate a report for a user"
    )
    generate_parser.add_argument("user_id", help="User ID to generate report for")
    generate_parser.add_argument(
        "--no-deliver",
        action="store_true",
        help="Generate but don't deliver via email",
    )

    # Feedback command
    feedback_parser = subparsers.add_parser("feedback", help="Submit feedback")
    feedback_parser.add_argument("report_id", help="Report ID")
    feedback_parser.add_argument("user_id", help="User ID")
    feedback_parser.add_argument(
        "rating", type=int, choices=[1, 2, 3, 4, 5], help="Rating (1-5)"
    )

    # List profiles command
    subparsers.add_parser("list", help="List all user profiles")

    args = parser.parse_args()

    if args.command == "create-profile":
        create_profile_interactive()

    elif args.command == "generate":
        asyncio.run(generate_report(args.user_id, deliver=not args.no_deliver))

    elif args.command == "feedback":
        asyncio.run(submit_feedback(args.report_id, args.user_id, args.rating))

    elif args.command == "list":
        list_profiles()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
