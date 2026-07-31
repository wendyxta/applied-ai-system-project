import os
import json
from google import genai

_MODEL = "gemini-3.5-flash-lite"

_SYSTEM = """Extract music preferences from the user's description.
Return ONLY valid JSON with exactly these keys and allowed values:
{
  "favorite_genre": one of: pop, lofi, rock, jazz, ambient, synthwave, indie pop,
  "favorite_mood":  one of: happy, chill, intense, relaxed, focused, moody,
  "target_energy":  float between 0.0 (very calm) and 1.0 (very energetic),
  "likes_acoustic": true or false
}
No explanation, no markdown — raw JSON only."""


def parse_user_description(description: str) -> dict:
    """Send free-text description to Gemini and return a structured profile dict."""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=_MODEL,
        contents=f"{_SYSTEM}\n\nUser said: {description}",
    )
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())
