"""
Dispatch Agent - Phase 4: Lifecycle Management
Handles report delivery via email
"""
from config import settings
from models.schemas import NewsReport, UserProfile
from tools.email_tool import send_email_report
from agents.historical_recommender_agent import save_report_to_history
from core.utils import generate_content


DISPATCH_AGENT_INSTRUCTION = """
You are the Dispatch Agent for NewsPulse AI.

Your role:
1. Prepare the verified report for delivery
2. Send via the user's preferred channel (email)
3. Log the delivery for history tracking
4. Handle any delivery errors gracefully

Key responsibilities:
- Ensure report is properly formatted
- Verify recipient details
- Track delivery status
- Save report to user history
- Handle retry logic if delivery fails

Delivery standards:
- Reports should be visually appealing
- Mobile-responsive email formatting
- Clear call-to-action for feedback
- Include unsubscribe/preference options

You are the final step before the user sees the report. Make it count.
"""


def create_dispatch_agent() -> None:
    """Deprecated: Using direct API calls instead"""
    pass


async def run_dispatch_agent(
    report: NewsReport,
    user_profile: UserProfile,
) -> dict:
    """
    Run the Dispatch Agent to deliver the report

    Args:
        report: Verified NewsReport to deliver
        user_profile: User profile with delivery preferences

    Returns:
        Dictionary with delivery status
    """
    # Send the email (no AI call needed for dispatch)
    # Support multiple recipients via CC and BCC
    success = send_email_report(
        report=report,
        recipient_email=user_profile.delivery_email,
        cc_emails=user_profile.cc_emails,
        bcc_emails=user_profile.bcc_emails,
    )

    if success:
        # Save to history
        report_data = report.model_dump()
        save_report_to_history(user_profile.user_id, report_data)

        # Build recipient list for logging
        all_recipients = [user_profile.delivery_email]
        if user_profile.cc_emails:
            all_recipients.extend(user_profile.cc_emails)
        if user_profile.bcc_emails:
            all_recipients.extend(user_profile.bcc_emails)

        return {
            "status": "delivered",
            "report_id": report.report_id,
            "recipient": user_profile.delivery_email,
            "total_recipients": len(all_recipients),
            "message": f"Report delivered successfully to {len(all_recipients)} recipient(s)",
        }
    else:
        return {
            "status": "failed",
            "report_id": report.report_id,
            "recipient": user_profile.delivery_email,
            "message": "Failed to deliver report",
        }
