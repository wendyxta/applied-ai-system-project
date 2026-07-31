import os
import json
from google import genai

_MODEL = "gemini-3.5-flash-lite"

_PROMPT = """Suggest {limit} real songs matching: "{description}"
Return ONLY a raw JSON array. Each item: title, artist, genre (pop/lofi/rock/jazz/ambient/synthwave/indie pop), mood (happy/chill/intense/relaxed/focused/moody), energy (0.0-1.0), acousticness (0.0-1.0).
No explanation, no markdown."""


def fetch_songs_from_llm(description: str, limit: int = 10) -> list:
    """Ask Gemini to suggest real songs matching the description, return as song dicts."""
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
    prompt = _PROMPT.format(limit=limit, description=description)
    try:
        response = client.models.generate_content(model=_MODEL, contents=prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        tracks = json.loads(text.strip())
    except Exception as e:
        print(f"  [retrieval] Song fetch failed: {e}")
        return []

    songs = []
    for i, t in enumerate(tracks):
        songs.append({
            "id":           2000 + i,
            "title":        t.get("title", "Unknown"),
            "artist":       t.get("artist", "Unknown"),
            "genre":        t.get("genre", "pop"),
            "mood":         t.get("mood", "unknown"),
            "energy":       float(t.get("energy", 0.5)),
            "tempo_bpm":    120.0,
            "valence":      0.5,
            "danceability": 0.5,
            "acousticness": float(t.get("acousticness", 0.5)),
        })

    print(f"  [retrieval] AI suggested {len(songs)} additional songs.")
    return songs
