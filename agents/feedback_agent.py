"""
Feedback Agent - Phase 5: Continuous Learning
Processes user feedback and updates profile constraints
"""
from config import settings
from models.schemas import FeedbackData
from models.user_profile import UserProfileManager
from core.utils import generate_content


FEEDBACK_AGENT_INSTRUCTION = """
You are the Feedback Agent for NewsPulse AI, responsible for continuous learning.

Your role:
1. Analyze user feedback (ratings, comments, preferences)
2. Extract actionable insights and constraints
3. Update user profile with learned preferences
4. Identify patterns in what works and what doesn't
5. Improve future reports based on feedback

Types of feedback to process:
- Star ratings (1-5)
- Liked/disliked topics
- Comments on content quality
- Length preferences (too long/too short)
- Missing topics or coverage gaps

Learning objectives:
- Topic preferences (what to emphasize/avoid)
- Source preferences (trusted outlets)
- Length and depth preferences
- Priority calibration (what they consider critical vs low)
- Format preferences

Constraint extraction:
From feedback, extract rules like:
- "User dislikes articles about [topic]" → add to excluded_topics
- "User wants more coverage of [topic]" → boost priority
- "Reports are too long" → reduce article count
- "Missing [topic]" → add to topics_of_interest

Output format:
- Summary of feedback
- Identified patterns
- Proposed constraint updates
- Recommendations for future reports

Remember: Every piece of feedback is valuable. The system gets smarter with each report.
"""


def create_feedback_agent() -> None:
    """Deprecated: Using direct API calls instead"""
    pass


async def run_feedback_agent(
    feedback: FeedbackData,
) -> dict:
    """
    Run the Feedback Agent to process user feedback

    Args:
        feedback: FeedbackData from the user

    Returns:
        Dictionary with constraint updates
    """
    import asyncio
    import json

    # Analyze feedback
    feedback_prompt = f"""
Analyze this user feedback and extract actionable constraints:

Report ID: {feedback.report_id}
User ID: {feedback.user_id}
Rating: {feedback.rating}/5 stars

Feedback Text: {feedback.feedback_text or "No text provided"}

Liked Topics: {', '.join(feedback.liked_topics) if feedback.liked_topics else "None specified"}
Disliked Topics: {', '.join(feedback.disliked_topics) if feedback.disliked_topics else "None specified"}
Missing Topics: {', '.join(feedback.missing_topics) if feedback.missing_topics else "None specified"}

Too Long: {feedback.too_long}
Too Short: {feedback.too_short}

Based on this feedback, extract:
1. Topics to emphasize more
2. Topics to reduce or exclude
3. Length adjustments needed
4. Priority calibration insights
5. Any other preferences to learn

Provide constraint updates in this JSON format:
{{
  "add_to_interests": ["topic1", "topic2"],
  "add_to_exclusions": ["topic3"],
  "length_preference": "shorter|same|longer",
  "priority_adjustments": {{"topic": "priority_level"}},
  "other_constraints": {{"key": "value"}},
  "summary": "Brief summary of what we learned"
}}
"""

    loop = asyncio.get_event_loop()
    response_text = await loop.run_in_executor(
        None,
        lambda: generate_content(feedback_prompt, FEEDBACK_AGENT_INSTRUCTION)
    )

    response_text = response_text.strip()
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.startswith("```"):
        response_text = response_text[3:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]

    constraint_updates = json.loads(response_text.strip())

    # Update user profile
    profile_manager = UserProfileManager()
    profile = profile_manager.load_profile(feedback.user_id)

    if profile:
        # Add new topics to interests
        if constraint_updates.get("add_to_interests"):
            for topic in constraint_updates["add_to_interests"]:
                if topic not in profile.topics_of_interest:
                    profile.topics_of_interest.append(topic)

        # Add topics to exclusions
        if constraint_updates.get("add_to_exclusions"):
            for topic in constraint_updates["add_to_exclusions"]:
                if topic not in profile.excluded_topics:
                    profile.excluded_topics.append(topic)

        # Update constraints
        new_constraints = {
            "length_preference": constraint_updates.get("length_preference", "same"),
            "priority_adjustments": constraint_updates.get("priority_adjustments", {}),
            "last_feedback_rating": feedback.rating,
            "feedback_count": profile.constraints.get("feedback_count", 0) + 1,
        }

        # Merge with existing constraints
        if constraint_updates.get("other_constraints"):
            new_constraints.update(constraint_updates["other_constraints"])

        profile_manager.update_constraints(feedback.user_id, new_constraints)

    return {
        "status": "processed",
        "constraint_updates": constraint_updates,
        "summary": constraint_updates.get("summary", "Feedback processed"),
    }


def collect_feedback(
    report_id: str,
    user_id: str,
    rating: int,
    feedback_text: str = None,
    liked_topics: list = None,
    disliked_topics: list = None,
    too_long: bool = False,
    too_short: bool = False,
    missing_topics: list = None,
) -> FeedbackData:
    """
    Helper function to create FeedbackData object

    Args:
        report_id: Report ID
        user_id: User ID
        rating: 1-5 star rating
        feedback_text: Optional text feedback
        liked_topics: Topics user liked
        disliked_topics: Topics user disliked
        too_long: Report was too long
        too_short: Report was too short
        missing_topics: Topics user wanted but didn't get

    Returns:
        FeedbackData object
    """
    return FeedbackData(
        report_id=report_id,
        user_id=user_id,
        rating=rating,
        feedback_text=feedback_text,
        liked_topics=liked_topics or [],
        disliked_topics=disliked_topics or [],
        too_long=too_long,
        too_short=too_short,
        missing_topics=missing_topics or [],
    )
