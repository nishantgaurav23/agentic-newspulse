#!/usr/bin/env python3
"""
Example Usage Script for NewsPulse AI
Demonstrates programmatic usage of the system
"""
import asyncio
from core.orchestrator import NewsPulseOrchestrator
from agents.feedback_agent import collect_feedback


async def example_full_workflow():
    """
    Demonstrates the complete workflow:
    1. Create a user profile
    2. Generate a report
    3. Submit feedback
    """
    print("=== NewsPulse AI - Example Full Workflow ===\n")

    # Initialize orchestrator
    orchestrator = NewsPulseOrchestrator()

    # Step 1: Create a user profile
    print("Step 1: Creating user profile...")
    profile = orchestrator.create_user_profile(
        user_id="example_cto",
        name="John Smith",
        role="CTO",
        company="Innovation Labs",
        industry="Technology",
        topics_of_interest=[
            "Artificial Intelligence",
            "Machine Learning",
            "Cloud Infrastructure",
            "Cybersecurity",
        ],
        delivery_email="john.smith@example.com",
        preferred_sources=["techcrunch.com", "arstechnica.com", "theverge.com"],
    )
    print(f"✓ Profile created for {profile.name}\n")

    # Step 2: Generate a news report
    print("Step 2: Generating news report...")
    print("This will take a few minutes as all agents work together...\n")

    report = await orchestrator.generate_report(
        user_id="example_cto",
        deliver=False,  # Set to True to actually send email
    )

    print(f"\n✓ Report generated!")
    print(f"  Report ID: {report.report_id}")
    print(f"  Total Articles: {report.total_articles}")
    print(f"  Topics Covered: {', '.join(report.topics_covered)}")

    print("\n--- Executive Summary ---")
    print(report.executive_summary)

    print("\n--- Articles ---")
    for i, article in enumerate(report.articles, 1):
        print(f"\n{i}. {article.title} [{article.priority.value.upper()}]")
        print(f"   Source: {article.source}")
        print(f"   Summary: {article.summary}")
        print(f"   Citations: {len(article.citations)}")

    # Step 3: Submit feedback
    print("\n\nStep 3: Submitting feedback...")

    feedback = collect_feedback(
        report_id=report.report_id,
        user_id="example_cto",
        rating=5,
        feedback_text="Excellent report! Very insightful and well-cited.",
        liked_topics=["Artificial Intelligence", "Machine Learning"],
        missing_topics=["Quantum Computing"],
    )

    feedback_result = await orchestrator.process_feedback(feedback)

    print(f"✓ Feedback processed!")
    print(f"  Summary: {feedback_result['summary']}")

    print("\n=== Workflow Complete! ===")
    print("\nThe system has now:")
    print("  1. Created a personalized profile")
    print("  2. Generated a verified news report")
    print("  3. Learned from your feedback")
    print("\nFuture reports will be even better based on this feedback!")


async def example_generate_only():
    """
    Simple example: just generate a report for an existing user
    """
    print("=== NewsPulse AI - Generate Report Only ===\n")

    orchestrator = NewsPulseOrchestrator()

    # Generate report for existing user
    try:
        report = await orchestrator.generate_report(
            user_id="example_cto",
            deliver=True,  # Send via email
        )

        print(f"\n✓ Report generated and delivered!")
        print(f"  Report ID: {report.report_id}")
        print(f"  Articles: {report.total_articles}")

    except ValueError as e:
        print(f"\n✗ Error: {e}")
        print("  Make sure you've created a user profile first!")
        print("  Run: python main.py create-profile")


async def example_batch_generation():
    """
    Generate reports for multiple users
    """
    print("=== NewsPulse AI - Batch Generation ===\n")

    orchestrator = NewsPulseOrchestrator()

    # List of users to generate reports for
    user_ids = ["ceo_user", "cto_user", "cfo_user"]

    for user_id in user_ids:
        try:
            print(f"\nGenerating report for {user_id}...")
            report = await orchestrator.generate_report(user_id, deliver=True)
            print(f"✓ Report delivered to {user_id}")

        except Exception as e:
            print(f"✗ Failed for {user_id}: {e}")

    print("\n✓ Batch generation complete!")


def main():
    """Main entry point"""
    print("NewsPulse AI - Example Usage\n")
    print("Choose an example to run:")
    print("1. Full workflow (create profile → generate report → feedback)")
    print("2. Generate report only (for existing user)")
    print("3. Batch generation (multiple users)")
    print("4. Exit")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        asyncio.run(example_full_workflow())
    elif choice == "2":
        asyncio.run(example_generate_only())
    elif choice == "3":
        asyncio.run(example_batch_generation())
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Invalid choice. Please run again and select 1-4.")


if __name__ == "__main__":
    main()
