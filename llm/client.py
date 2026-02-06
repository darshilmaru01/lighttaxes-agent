import os
from dotenv import load_dotenv

load_dotenv()

USE_LLM = os.getenv("USE_LLM", "true").lower() == "true"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")

def ask_llm(prompt: str) -> str:
    """
    Gemini (new SDK) LLM call with graceful fallback.
    """
    if not USE_LLM:
        return (
            "LLM disabled. According to IRS Form 1040 instructions, "
            "most taxpayers take the standard deduction unless itemizing."
        )

    if LLM_PROVIDER != "gemini":
        return "Unsupported LLM provider configured."

    try:
        from google import genai

        client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config={
                "temperature": 0.0,
                "max_output_tokens": 800
            }
        )

        return response.text

    except Exception as e:
        return (
            "Gemini API unavailable or quota exceeded. "
            "Defaulting to standard deduction per IRS rules."
        )
