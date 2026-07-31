import os
import json
import re
from google import genai

_MODEL = "gemini-3.5-flash-lite"
_BASE_SONG_ID = 2000

_PROMPT = """Suggest {limit} real songs matching: "{description}"
Return ONLY a raw JSON array. Each item: title, artist, genre (pop/lofi/rock/jazz/ambient/synthwave/indie pop), mood (happy/chill/intense/relaxed/focused/moody), energy (0.0-1.0), acousticness (0.0-1.0).
No explanation, no markdown."""

_DEFAULTS = {
    "title": "Unknown",
    "artist": "Unknown",
    "genre": "pop",
    "mood": "unknown",
    "energy": 0.5,
    "acousticness": 0.5,
}

def _extract_json_from_text(text: str) -> str:
    """Extract JSON from potentially markdown-wrapped response."""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    return text


def fetch_songs_from_llm(description: str, limit: int = 10) -> list:
    """Ask Gemini to suggest real songs matching the description, return as song dicts."""
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
    prompt = _PROMPT.format(limit=limit, description=description)
    try:
        response = client.models.generate_content(model=_MODEL, contents=prompt)
        json_text = _extract_json_from_text(response.text)
        tracks = json.loads(json_text)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"  [retrieval] Song fetch failed: {e}")
        return []

    songs = [
        {
            "id": _BASE_SONG_ID + i,
            "title": t.get("title", _DEFAULTS["title"]),
            "artist": t.get("artist", _DEFAULTS["artist"]),
            "genre": t.get("genre", _DEFAULTS["genre"]),
            "mood": t.get("mood", _DEFAULTS["mood"]),
            "energy": float(t.get("energy", _DEFAULTS["energy"])),
            "tempo_bpm": 120.0,
            "valence": 0.5,
            "danceability": 0.5,
            "acousticness": float(t.get("acousticness", _DEFAULTS["acousticness"])),
        }
        for i, t in enumerate(tracks)
    ]

    print(f"  [retrieval] AI suggested {len(songs)} additional songs.")
    return songs
