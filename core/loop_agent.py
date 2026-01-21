"""
Verification Loop Agent
Implements the self-correction loop where the Verification Agent
audits the Writer Agent and forces retries if quality standards aren't met
"""
from typing import Tuple
import logging

from config import settings
from models.schemas import NewsReport
from agents.writer_agent import run_writer_agent
from agents.verification_agent import run_verification_agent, check_report_verified


class VerificationLoop:
    """
    Implements the verification loop for self-correction

    This is a key differentiator: unlike standard scripts, this system
    can audit itself and retry when quality standards aren't met.
    """

    def __init__(self, max_retries: int = None):
        """
        Initialize the verification loop

        Args:
            max_retries: Maximum retry attempts (defaults to settings)
        """
        self.max_retries = max_retries or settings.verification_max_retries
        self.logger = logging.getLogger("newspulse")

    async def run(
        self,
        processed_articles: list,
        user_context: dict,
        max_articles: int = 10,
    ) -> Tuple[NewsReport, bool]:
        """
        Run the verification loop

        Process:
        1. Writer Agent creates report
        2. Verification Agent audits it
        3. If verification fails, provide feedback and retry
        4. Repeat until verified or max retries reached

        Args:
            processed_articles: Articles from Fetch Agent
            user_context: User context for personalization
            max_articles: Max articles in report

        Returns:
            Tuple of (NewsReport, success_flag)
        """
        retry_count = 0
        feedback_context = ""

        while retry_count <= self.max_retries:
            self.logger.info(
                f"Verification loop attempt {retry_count + 1}/{self.max_retries + 1}"
            )

            try:
                # Phase 1: Writer Agent creates report
                self.logger.info("Writer Agent: Drafting report...")
                if feedback_context:
                    self.logger.info(f"Applying feedback: {feedback_context}")

                # Add feedback to user context if retrying
                if feedback_context:
                    user_context["writer_feedback"] = feedback_context

                report = await run_writer_agent(
                    processed_articles=processed_articles,
                    user_context=user_context,
                    max_articles=max_articles,
                )

                # Phase 2: Verification Agent audits
                self.logger.info("Verification Agent: Auditing report...")
                verification_results = await run_verification_agent(report)

            except (ValueError, Exception) as e:
                # Writer agent failed (e.g., JSON parsing error, validation error)
                self.logger.warning(f"✗ Writer Agent error: {str(e)}")

                if retry_count >= self.max_retries:
                    self.logger.error(
                        f"Max retries ({self.max_retries}) reached after Writer Agent errors."
                    )
                    raise

                # Prepare feedback for retry
                feedback_context = f"""
PREVIOUS ATTEMPT FAILED

Error: {str(e)}

Instructions:
- Ensure you output valid JSON
- Escape all quotes and newlines properly in JSON strings
- Include complete citations for all claims
- Double-check JSON structure before responding

Try again with proper formatting.
"""
                retry_count += 1
                continue

            # Phase 3: Check if verified
            is_verified, feedback_summary = check_report_verified(
                verification_results
            )

            if is_verified:
                self.logger.info("✓ Report verified successfully!")
                return report, True

            # Phase 4: Not verified, prepare for retry
            self.logger.warning(f"✗ Verification failed. Issues found:")
            self.logger.warning(feedback_summary)

            if retry_count >= self.max_retries:
                self.logger.error(
                    f"Max retries ({self.max_retries}) reached. Returning unverified report."
                )
                return report, False

            # Prepare feedback for next iteration
            feedback_context = f"""
PREVIOUS ATTEMPT REJECTED

Verification Issues:
{feedback_summary}

Instructions:
- Fix all missing citations
- Ensure every claim has a direct quote and source
- Double-check that quotes support the claims
- Be more conservative with assertions

Try again with these corrections applied.
"""

            retry_count += 1

        # Should not reach here, but just in case
        return report, False


async def run_verification_loop(
    processed_articles: list,
    user_context: dict,
    max_articles: int = 10,
) -> Tuple[NewsReport, bool]:
    """
    Convenience function to run the verification loop

    Args:
        processed_articles: Articles from Fetch Agent
        user_context: User context
        max_articles: Max articles in report

    Returns:
        Tuple of (NewsReport, success_flag)
    """
    loop = VerificationLoop()
    return await loop.run(
        processed_articles=processed_articles,
        user_context=user_context,
        max_articles=max_articles,
    )
