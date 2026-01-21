"""
Profile Agent - Phase 1: Contextual Planning
Loads user profile and ensures personalization
"""
from config import settings
from models.schemas import UserProfile
from models.user_profile import UserProfileManager
from core.utils import generate_content


PROFILE_AGENT_INSTRUCTION = """
You are the Profile Agent for NewsPulse AI, responsible for understanding user context.

Your role:
1. Load the user's profile (interests, role, company, industry)
2. Review learned constraints from previous feedback
3. Identify key personalization requirements for this report
4. Output a structured summary of what matters most to this user

Key responsibilities:
- Ensure the user's topics of interest are prioritized
- Apply any exclusion rules (topics, sources)
- Incorporate constraints learned from feedback
- Provide context about the user's role and why certain news matters to them

Output format:
You must provide:
- User context (role, company, industry)
- Priority topics (what to search for)
- Exclusion rules (what to avoid)
- Personalization notes (how to tailor content)

Be thorough and precise. The quality of the entire report depends on accurate personalization.
"""


async def run_profile_agent(user_id: str) -> dict:
    """
    Run the Profile Agent to get user context

    Args:
        user_id: User ID to load profile for

    Returns:
        Dictionary with user context and personalization requirements
    """
    profile_manager = UserProfileManager()
    profile = profile_manager.load_profile(user_id)

    if profile is None:
        raise ValueError(f"No profile found for user_id: {user_id}")

    prompt = f"""
Analyze this user profile and provide personalization requirements:

User Profile:
- Name: {profile.name}
- Role: {profile.role}
- Company: {profile.company}
- Industry: {profile.industry}

Topics of Interest:
{chr(10).join(f"- {topic}" for topic in profile.topics_of_interest)}

Excluded Topics:
{chr(10).join(f"- {topic}" for topic in profile.excluded_topics) if profile.excluded_topics else "None"}

Preferred Sources:
{chr(10).join(f"- {source}" for source in profile.preferred_sources) if profile.preferred_sources else "Any"}

Excluded Sources:
{chr(10).join(f"- {source}" for source in profile.excluded_sources) if profile.excluded_sources else "None"}

Learned Constraints:
{profile.constraints if profile.constraints else "None yet"}

Provide a clear analysis of:
1. What news topics are most relevant for this user's role
2. How to prioritize and filter content
3. Any specific constraints to apply
4. How to explain relevance in terms this user cares about
"""

    # Run in thread pool to avoid blocking
    import asyncio
    loop = asyncio.get_event_loop()
    response_text = await loop.run_in_executor(
        None,
        lambda: generate_content(prompt, PROFILE_AGENT_INSTRUCTION)
    )

    return {
        "user_profile": profile,
        "personalization_analysis": response_text,
        "priority_topics": profile.topics_of_interest,
        "excluded_topics": profile.excluded_topics,
        "constraints": profile.constraints,
    }
