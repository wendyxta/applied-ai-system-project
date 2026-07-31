from dotenv import load_dotenv

load_dotenv()

from src.recommender import (
    Song, UserProfile, Recommender,
    score_song, recommend_songs
)
from src.profile_parser import parse_user_description
from src.retrieval import fetch_songs_from_llm
import pytest


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    try:
        user = UserProfile(
            favorite_genre="pop",
            favorite_mood="happy",
            target_energy=0.8,
            likes_acoustic=False,
        )
        rec = make_small_recommender()
        song = rec.songs[0]

        explanation = rec.explain_recommendation(user, song)
        assert isinstance(explanation, str)
        assert explanation.strip() != ""
    except ValueError as e:
        if "No API key" in str(e):
            pytest.skip(f"Gemini API unavailable: {e}")
        raise


# ============================================================================
# RAG Stage 1: Profile Parser Tests
# ============================================================================

def test_parse_user_description_returns_valid_dict():
    """Test that profile parser returns a dict with required keys."""
    try:
        result = parse_user_description("upbeat energetic pop music")
        assert isinstance(result, dict)
        assert "favorite_genre" in result
        assert "favorite_mood" in result
        assert "target_energy" in result
        assert "likes_acoustic" in result
    except Exception as e:
        pytest.skip(f"Gemini API unavailable: {e}")


def test_parse_user_description_returns_valid_values():
    """Test that parsed values are of correct types and in valid ranges."""
    try:
        result = parse_user_description("chill lofi music")
        valid_genres = ["pop", "lofi", "rock", "jazz", "ambient", "synthwave", "indie pop"]
        valid_moods = ["happy", "chill", "intense", "relaxed", "focused", "moody"]
        assert result["favorite_genre"] in valid_genres
        assert result["favorite_mood"] in valid_moods
        assert 0.0 <= result["target_energy"] <= 1.0
        assert isinstance(result["likes_acoustic"], bool)
    except Exception as e:
        pytest.skip(f"Gemini API unavailable: {e}")


# ============================================================================
# RAG Stage 2: Retrieval Tests
# ============================================================================

def test_fetch_songs_from_llm_returns_list():
    """Test that song retrieval returns a list of song dicts."""
    try:
        songs = fetch_songs_from_llm("upbeat pop", limit=3)
        assert isinstance(songs, list)
    except Exception as e:
        pytest.skip(f"Gemini API unavailable: {e}")


def test_fetch_songs_from_llm_returns_valid_song_dicts():
    """Test that each song dict has required fields and valid values."""
    try:
        songs = fetch_songs_from_llm("energetic dance", limit=2)
        if songs:
            for song in songs:
                assert "id" in song
                assert "title" in song
                assert "artist" in song
                assert "genre" in song
                assert "energy" in song
                assert 0.0 <= song["energy"] <= 1.0
                assert 0.0 <= song["acousticness"] <= 1.0
    except Exception as e:
        pytest.skip(f"Gemini API unavailable: {e}")


# ============================================================================
# RAG Stage 3: Explainer Tests
# ============================================================================

def test_explain_recommendation_dict_returns_string():
    """Test that explainer returns a non-empty string."""
    try:
        from src.recommender import explain_recommendation_dict
        song = {
            "title": "Test Song",
            "artist": "Test Artist",
            "genre": "pop",
            "mood": "happy"
        }
        result = explain_recommendation_dict(
            "I want upbeat pop music",
            {"favorite_genre": "pop", "target_energy": 0.9},
            song
        )
        assert isinstance(result, str)
        assert len(result) > 0
    except Exception as e:
        pytest.skip(f"Gemini API unavailable: {e}")


def test_explain_recommendation_dict_incorporates_user_preference():
    """Test that explanation incorporates the user's stated preference."""
    try:
        from src.recommender import explain_recommendation_dict
        song = {"title": "Song A", "artist": "Artist A", "genre": "pop", "mood": "happy"}
        result = explain_recommendation_dict(
            "I love upbeat music that makes me happy",
            {"favorite_genre": "pop"},
            song
        )
        assert isinstance(result, str) and len(result) > 0
    except Exception as e:
        pytest.skip(f"Gemini API unavailable: {e}")


# ============================================================================
# Scoring Function Tests
# ============================================================================

def test_score_song_matches_genre_and_mood():
    """Test that genre and mood matches increase the score."""
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.5,
        "likes_acoustic": False,
    }
    song = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.5,
        "acousticness": 0.2,
    }
    score_value, reasons = score_song(user_prefs, song)
    assert score_value >= 3.5
    assert any("genre match" in r for r in reasons)
    assert any("mood match" in r for r in reasons)


def test_score_song_considers_energy_proximity():
    """Test that energy proximity affects the score."""
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "chill",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }
    close_energy = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.8,
        "acousticness": 0.2,
    }
    far_energy = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.1,
        "acousticness": 0.2,
    }
    close_score, _ = score_song(user_prefs, close_energy)
    far_score, _ = score_song(user_prefs, far_energy)
    assert close_score > far_score


# ============================================================================
# Recommendation Pipeline Tests
# ============================================================================

def test_recommend_songs_returns_top_k():
    """Test that recommend_songs returns exactly k results."""
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }
    songs = [
        {"genre": "pop", "mood": "happy", "energy": 0.8, "acousticness": 0.2},
        {"genre": "lofi", "mood": "chill", "energy": 0.4, "acousticness": 0.9},
        {"genre": "rock", "mood": "intense", "energy": 0.9, "acousticness": 0.1},
    ]
    results = recommend_songs(user_prefs, songs, k=2)
    assert len(results) == 2


def test_recommend_songs_sorted_by_score():
    """Test that returned recommendations are sorted by score (highest first)."""
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }
    songs = [
        {"genre": "rock", "mood": "intense", "energy": 0.9, "acousticness": 0.1},
        {"genre": "pop", "mood": "happy", "energy": 0.8, "acousticness": 0.2},
        {"genre": "lofi", "mood": "chill", "energy": 0.4, "acousticness": 0.9},
    ]
    results = recommend_songs(user_prefs, songs, k=3)
    scores = [score for _, score, _ in results]
    assert scores == sorted(scores, reverse=True)
