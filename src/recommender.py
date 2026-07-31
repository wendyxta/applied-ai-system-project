from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv
import os
from google import genai

_MODEL = "gemini-3.5-flash-lite"

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        prompt = (
            f"A user wants {user.favorite_mood} {user.favorite_genre} music "
            f"with {'acoustic' if user.likes_acoustic else 'non-acoustic'} vibes "
            f"and energy around {user.target_energy}.\n"
            f"We recommended '{song.title}' by {song.artist} "
            f"(genre: {song.genre}, mood: {song.mood}).\n"
            "Write one sentence (max 20 words) explaining why this song fits."
        )
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
        response = client.models.generate_content(model=_MODEL, contents=prompt)
        return response.text.strip()


def explain_recommendation_dict(user_description: str, user_prefs: Dict, song: Dict) -> str:
    """Generate a one-sentence AI explanation for why a song fits the user's description."""
    prompt = (
        f"User wants: \"{user_description}\"\n"
        f"Song: '{song['title']}' by {song['artist']} (genre: {song['genre']}, mood: {song['mood']}).\n"
        "One sentence (max 20 words): why does this song fit?"
    )
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
    response = client.models.generate_content(model=_MODEL, contents=prompt)
    return response.text.strip()


def load_songs(csv_path: str) -> List[Dict]:
    """Load and return all songs from a CSV file as a list of dicts."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences and return the score with reasons."""
    score = 0.0
    reasons = []

    if song.get("genre", "").lower() == user_prefs.get("favorite_genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song.get("mood", "").lower() == user_prefs.get("favorite_mood", "").lower():
        score += 1.5
        reasons.append("mood match (+1.5)")

    target_energy = user_prefs.get("target_energy", 0.5)
    energy_diff = abs(song.get("energy", 0.5) - target_energy)
    energy_score = round(max(0.0, 1.0 - energy_diff), 2)
    if energy_score > 0:
        score += energy_score
        reasons.append(f"energy proximity (+{energy_score})")

    if user_prefs.get("likes_acoustic", False) and song.get("acousticness", 0.0) > 0.5:
        score += 0.5
        reasons.append("acoustic match (+0.5)")

    return (round(score, 2), reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by score and return the top-k results with scores and reasons."""
    scored = [
        (song, score, reasons)
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return [
        (song, score, ", ".join(reasons) if reasons else "no strong matches")
        for song, score, reasons in ranked[:k]
    ]
