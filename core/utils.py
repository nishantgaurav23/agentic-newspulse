"""
Utility functions for NewsPulse AI
"""
from google import genai
from google.genai import types
from config import settings


def get_genai_client():
    """
    Get configured Google genai client

    Returns:
        Configured genai.Client instance
    """
    if not settings or not settings.google_api_key:
        raise ValueError(
            "Google API key not configured. "
            "Please set GOOGLE_API_KEY in your .env file"
        )

    client = genai.Client(api_key=settings.google_api_key)
    return client


def generate_content(
    prompt: str,
    system_instruction: str = None,
    temperature: float = None,
    max_tokens: int = None,
) -> str:
    """
    Generate content using Gemini model

    Args:
        prompt: The prompt to send to the model
        system_instruction: Optional system instruction to prepend
        temperature: Sampling temperature (default from settings)
        max_tokens: Maximum tokens to generate (default from settings)

    Returns:
        Generated text response
    """
    client = get_genai_client()

    # Combine system instruction with prompt if provided
    if system_instruction:
        full_prompt = f"{system_instruction}\n\n{prompt}"
    else:
        full_prompt = prompt

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=full_prompt,
        config=types.GenerateContentConfig(
            temperature=temperature or settings.temperature,
            max_output_tokens=max_tokens or settings.max_tokens,
        )
    )

    return response.text
