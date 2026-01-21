"""
NewsPulse AI Orchestrator
Coordinates the 5-phase multi-agent workflow
"""
import logging
from typing import Optional

from config import settings, setup_logger, set_agent_context
from models.schemas import NewsReport
from models.user_profile import UserProfileManager

from agents.profile_agent import run_profile_agent
from agents.historical_recommender_agent import run_historical_recommender_agent
from agents.search_agent import run_search_agent
from agents.fetch_agent import run_fetch_agent
from agents.dispatch_agent import run_dispatch_agent

from core.loop_agent import run_verification_loop


class NewsPulseOrchestrator:
    """
    Main orchestrator for the NewsPulse AI system

    Coordinates all 5 phases:
    Phase 1: Contextual Planning (Profile + Historical Recommender)
    Phase 2: Grounded Research (Search + Fetch)
    Phase 3: Verification Loop (Writer + Verification)
    Phase 4: Dispatch (Email delivery)
    Phase 5: Feedback (Continuous learning)
    """

    def __init__(self, log_level: str = None):
        """
        Initialize the orchestrator

        Args:
            log_level: Logging level (defaults to settings)
        """
        self.logger = setup_logger(
            "newspulse", level=log_level or settings.log_level
        )
        self.profile_manager = UserProfileManager()

    async def generate_report(
        self, user_id: str, deliver: bool = True
    ) -> NewsReport:
        """
        Generate a complete news report for a user

        This is the main entry point that orchestrates all agents.

        Args:
            user_id: User ID to generate report for
            deliver: Whether to deliver the report via email

        Returns:
            Generated NewsReport
        """
        self.logger.info(f"=== Starting NewsPulse AI for user: {user_id} ===")

        # ===== PHASE 1: CONTEXTUAL PLANNING =====
        self.logger.info(">>> PHASE 1: Contextual Planning")

        # Step 1.1: Profile Agent
        set_agent_context(self.logger, "ProfileAgent")
        self.logger.info("Running Profile Agent...")
        profile_data = await run_profile_agent(user_id)
        user_profile = profile_data["user_profile"]
        priority_topics = profile_data["priority_topics"]

        self.logger.info(
            f"User context loaded: {user_profile.role} at {user_profile.company}"
        )
        self.logger.info(f"Priority topics: {', '.join(priority_topics)}")

        # Step 1.2: Historical Recommender Agent
        set_agent_context(self.logger, "HistoricalRecommender")
        self.logger.info("Running Historical Recommender Agent...")
        historical_rec = await run_historical_recommender_agent(
            user_id, priority_topics
        )

        self.logger.info(
            f"Historical analysis: {len(historical_rec.exclude_urls)} URLs to exclude"
        )

        # ===== PHASE 2: GROUNDED RESEARCH =====
        self.logger.info(">>> PHASE 2: Grounded Research")

        # Step 2.1: Search Agent
        set_agent_context(self.logger, "SearchAgent")
        self.logger.info("Running Search Agent...")

        user_context = {
            "user_id": user_id,
            "role": user_profile.role,
            "company": user_profile.company,
            "industry": user_profile.industry,
            "priority_topics": priority_topics,
            "constraints": user_profile.constraints,
        }

        search_results = await run_search_agent(
            priority_topics=priority_topics,
            user_context=user_context,
            exclude_urls=historical_rec.exclude_urls,
            max_results_per_topic=5,
        )

        self.logger.info(f"Found {len(search_results)} relevant articles")

        if not search_results:
            self.logger.warning("No search results found. Cannot generate report.")
            raise ValueError("No search results found")

        # Step 2.2: Fetch Agent
        set_agent_context(self.logger, "FetchAgent")
        self.logger.info("Running Fetch Agent to retrieve content...")

        processed_articles = await run_fetch_agent(
            search_results=search_results,
            max_articles=settings.max_articles_per_report,
        )

        self.logger.info(
            f"Successfully fetched and processed {len(processed_articles)} articles"
        )

        if not processed_articles:
            self.logger.warning("No articles fetched successfully.")
            raise ValueError("Failed to fetch any article content")

        # ===== PHASE 3: VERIFICATION LOOP =====
        self.logger.info(">>> PHASE 3: Verification Loop")

        set_agent_context(self.logger, "VerificationLoop")
        self.logger.info("Starting Writer-Verification loop...")

        report, is_verified = await run_verification_loop(
            processed_articles=processed_articles,
            user_context=user_context,
            max_articles=settings.max_articles_per_report,
        )

        if is_verified:
            self.logger.info("✓ Report successfully verified!")
        else:
            self.logger.warning(
                "⚠ Report generated but not fully verified after max retries"
            )

        # ===== PHASE 4: DISPATCH =====
        if deliver:
            self.logger.info(">>> PHASE 4: Dispatch")

            set_agent_context(self.logger, "DispatchAgent")
            self.logger.info("Running Dispatch Agent...")

            delivery_result = await run_dispatch_agent(
                report=report, user_profile=user_profile
            )

            if delivery_result["status"] == "delivered":
                self.logger.info(
                    f"✓ Report delivered to {delivery_result['recipient']}"
                )
            else:
                self.logger.error(
                    f"✗ Failed to deliver report: {delivery_result['message']}"
                )
        else:
            self.logger.info("Skipping delivery (deliver=False)")

        self.logger.info(f"=== NewsPulse AI completed for user: {user_id} ===")

        return report

    async def process_feedback(self, feedback_data):
        """
        Process user feedback (Phase 5)

        Args:
            feedback_data: FeedbackData object
        """
        self.logger.info(f">>> PHASE 5: Processing Feedback")

        from agents.feedback_agent import run_feedback_agent

        set_agent_context(self.logger, "FeedbackAgent")

        result = await run_feedback_agent(feedback_data)

        self.logger.info(f"Feedback processed: {result['summary']}")

        return result

    def create_user_profile(
        self,
        user_id: str,
        name: str,
        role: str,
        company: str,
        industry: str,
        topics_of_interest: list,
        delivery_email: str,
        **kwargs,
    ):
        """
        Create a new user profile

        Args:
            user_id: Unique user identifier
            name: User's name
            role: User's role (e.g., "CEO", "CTO")
            company: User's company
            industry: Industry sector
            topics_of_interest: List of topics to track
            delivery_email: Email for report delivery
            **kwargs: Additional profile fields

        Returns:
            Created UserProfile object
        """
        self.logger.info(f"Creating profile for user: {user_id}")

        profile = self.profile_manager.create_profile(
            user_id=user_id,
            name=name,
            role=role,
            company=company,
            industry=industry,
            topics_of_interest=topics_of_interest,
            delivery_email=delivery_email,
            **kwargs,
        )

        self.logger.info(f"✓ Profile created successfully")

        return profile
