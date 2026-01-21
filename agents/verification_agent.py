"""
Verification Agent - Phase 3: Verification Loop
Acts as a quality gate, ensuring all claims are citation-backed
"""
from typing import List

from config import settings
from models.schemas import NewsReport, Article, VerificationResult
from core.utils import generate_content


VERIFICATION_AGENT_INSTRUCTION = """
You are the Verification Agent for NewsPulse AI, the quality control gatekeeper.

Your role:
1. Audit articles for citation completeness
2. Verify that key claims have supporting citations
3. Check that quotes are properly attributed
4. Ensure sources are credible
5. REJECT work with major quality issues

Verification checklist for each article:
✓ Do major factual claims have citations?
✓ Are citations reasonably complete (claim, quote, source_url, source_title)?
✓ Do the quotes generally support the claims?
✓ Is the source credible (avoid blogs, marketing sites)?
✓ Is the priority level justified?

Quality standards - BALANCED APPROACH:
- CRITICAL FACTS (numbers, specific claims): Must have direct citations
- GENERAL STATEMENTS (industry trends, common knowledge): Citation preferred but not mandatory
- ANALYSIS/INSIGHTS: Can be derived from cited facts without separate citation
- RECOMMENDATIONS: Can be logical conclusions from cited information
- Allow paraphrased quotes if they capture the essence accurately
- Accept multiple facts from one citation if clearly related

Decision criteria:
APPROVE: Major claims are cited, sources are credible, no obvious fabrications
REJECT: Missing citations for critical facts, incredible sources, or clear fabrications

If you REJECT:
- Focus on the most important issues
- Identify claims that MUST have citations (numbers, specific events)
- Allow reasonable analysis and insights without individual citations
- Be practical - not every sentence needs a citation

Remember: Balance quality with practicality. Ensure factual accuracy while allowing professional analysis.
"""


def create_verification_agent() -> None:
    """
    Create the Verification Agent

    This agent is the QUALITY GATE. It audits the Writer Agent's work
    and rejects reports that don't meet citation standards.

    Returns:
        Google ADK Agent instance
    """
    system_instruction = """
You are the Verification Agent for NewsPulse AI, the quality control gatekeeper.

Your role:
1. Audit every article for citation completeness
2. Verify that claims match their citations
3. Check that quotes are properly attributed
4. Ensure no speculation or unsupported assertions
5. REJECT work that doesn't meet standards

Verification checklist for each article:
✓ Does every factual claim have a citation?
✓ Are citations complete (claim, quote, source_url, source_title)?
✓ Do the quotes actually support the claims?
✓ Are there any unsupported assertions?
✓ Is the source credible?
✓ Is the priority level justified?

Quality standards:
- Zero tolerance for missing citations
- All quotes must be verbatim (or clearly paraphrased)
- No vague attributions ("sources say", "reports indicate")
- Every number, fact, or claim needs a specific source
- Speculation must be clearly labeled as analysis, not fact

Decision criteria:
APPROVE: All claims are properly cited, no issues found
REJECT: Missing citations, unsupported claims, or quality issues

If you REJECT:
- List specific issues found
- Identify which claims lack citations
- Provide clear feedback for the Writer Agent to fix
- Suggest retry with improvements

Remember: You are the human editor's substitute. Be thorough and demanding.
Better to reject and retry than to send unverified content to executives.
"""


async def run_verification_agent(
    report: NewsReport,
) -> List[VerificationResult]:
    """
    Run the Verification Agent to check report quality

    Args:
        report: NewsReport to verify

    Returns:
        List of VerificationResult objects, one per article
    """
    import asyncio
    import json

    loop = asyncio.get_event_loop()
    verification_results = []

    for article in report.articles:
        # Prepare article for verification
        verification_prompt = f"""
Verify this article for citation completeness and quality:

Title: {article.title}
Summary: {article.summary}
Priority: {article.priority.value}

Key Insights:
{chr(10).join(f"- {insight}" for insight in article.key_insights)}

Citations:
{chr(10).join(f'''
Citation {i+1}:
- Claim: {citation.claim}
- Quote: "{citation.quote}"
- Source: {citation.source_title}
- URL: {citation.source_url}
''' for i, citation in enumerate(article.citations))}

Verification checklist:
1. Does every factual claim in the summary and insights have a citation?
2. Are all citations complete with claim, quote, source_url, and source_title?
3. Do the quotes support the claims?
4. Are there any unsupported assertions?
5. Is the priority level justified by the content?

Respond in this JSON format:
{{
  "is_verified": true or false,
  "issues_found": ["issue 1", "issue 2", ...],
  "missing_citations": ["uncited claim 1", "uncited claim 2", ...],
  "feedback": "Detailed feedback for the writer",
  "retry_suggested": true or false
}}

Be strict. If in doubt, REJECT and request retry.
"""

        response_text = await loop.run_in_executor(
            None,
            lambda p=verification_prompt: generate_content(p, VERIFICATION_AGENT_INSTRUCTION, temperature=0.3)
        )

        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        verification_data = json.loads(response_text.strip())

        result = VerificationResult(
            article_title=article.title,
            is_verified=verification_data["is_verified"],
            issues_found=verification_data.get("issues_found", []),
            missing_citations=verification_data.get("missing_citations", []),
            feedback=verification_data["feedback"],
            retry_suggested=verification_data.get("retry_suggested", False),
        )

        verification_results.append(result)

    return verification_results


def check_report_verified(
    verification_results: List[VerificationResult],
) -> tuple[bool, str]:
    """
    Check if the entire report is verified

    Args:
        verification_results: List of verification results

    Returns:
        Tuple of (is_verified, feedback_summary)
    """
    all_verified = all(result.is_verified for result in verification_results)

    if all_verified:
        return True, "All articles verified successfully."

    # Compile feedback
    feedback_parts = []
    for result in verification_results:
        if not result.is_verified:
            feedback_parts.append(f"""
Article: {result.article_title}
Issues: {', '.join(result.issues_found)}
Missing Citations: {', '.join(result.missing_citations)}
Feedback: {result.feedback}
""")

    feedback_summary = "\n".join(feedback_parts)
    return False, feedback_summary
