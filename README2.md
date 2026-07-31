# 🎵 Music Recommender with RAG Integration (Part 2)

## Project Summary

**Original Project Goals:**
- The Music Recommender imports 20 songs from a CSV file and constructs predefined music taste user profiles. The system will then score the songs based on how well a given user profiles and recommends the top 5 songs with the closest match to the user's music taste. 

**Extended Capabilities (Retrieval-Augmented Generation (RAG) Integration):**
- The extended Music Recommender will integrate RAG components to use semantic search to parse user preference input to expand beyond the 3 hard-coded user profiles from the original project. This better matches real life user input and allows for mroe flexible input. 
- The original 20 song catalog will also be expanded by asking Gemini to suggest additional real songs matching the user's description. This allows users to have more song options to explore that may more closely align with user preferences.
- An additional explanation for why each song was recommended based on the user's provided description will also be provided. This will provide a more meaningful understanding of why this song matches the user's music taste.

---

## Architecture Overview

The system is a three-stage RAG pipeline wrapped around the original rule-based scorer. See [`architecture.mmd`] for the full diagram.

**Stage 1 — Semantic Profile Parser (`profile_parser.py`):** The user types a free-text description and Gemini extracts a structured profile (genre, mood, energy, acoustic preference), enabling natural language input instead of hardcoded profiles.

**Stage 2 — Retriever (`retrieval.py` + `recommender.py`):** The local `songs.csv` (20 songs) is combined with 10 real songs suggested by Gemini based on the user's description, expanding the catalog to ~30 candidates for the scorer to rank.

**Stage 3 — Explainer (`recommender.py`):** Each top-5 result is passed to Gemini with the user's original description, which generates one natural-language sentence explaining why that song fits.

**Testing and Human Evaluation:** `pytest` tests verify the scorer ranks correctly and the explainer returns a non-empty string. The user also manually spot-checks whether results match their description.

---

## Setup Instructions

1. **Clone and Install Required Packages:**
   - pip install -r requirements.txt

2. **Get a Gemini API Key:**
   - Go to https://aistudio.google.com/app/apikeys and create a free Gemini API key.

3. **Configure Environment:**
   - Create a `.env` file in the project root:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

4. **Run the Recommender:**
   - python -m src.main
   - Enter a text description of your desired music taste

---

## Sample Interactions
Sample Interactions: Include at least 2-3 examples of inputs and the resulting AI outputs to demonstrate the system is functional.

**Sample Run #1:**
Music Recommender — RAG Edition
=============================================
Describe the music you're in the mood for:
> upbeat to wake me up

[1/3] Parsing your description...
      Detected: genre=pop, mood=happy, energy=0.9, acoustic=False

[2/3] Retrieving songs...
Loading songs from data/songs.csv...
Loaded songs: 20
  [retrieval] AI suggested 10 additional songs.
      Catalog size: 30 songs total

[3/3] Finding your top 5 and generating explanations...

=============================================
   Top 5 Recommendations For You
=============================================

#1  I Gotta Feeling — The Black Eyed Peas
    Score : 4.50
    Why   : This infectious, high-energy pop anthem delivers pure positivity and excitement to instantly pump you up and start your day right!

#2  Dance The Night — Dua Lipa
    Score : 4.48
    Why   : Dua Lipa’s vibrant disco-pop beat and joyful energy will instantly energize you and start your morning right!

#3  Uptown Funk — Mark Ronson ft. Bruno Mars
    Score : 4.47
    Why   : Its infectious brass hooks and Bruno Mars' high-energy vocals provide an instant, joyful burst of morning motivation.

#4  Wake Me Up Before You Go-Go — Wham!
    Score : 4.46
    Why   : Its high-energy pop beats and joyful vocals provide an instant, cheerful burst of motivation to start your morning.

#5  Walking On Sunshine — Katrina & The Waves
    Score : 4.45
    Why   : Its explosive horn section, driving rhythm, and purely joyous energy make it the ultimate wakeup anthem.

=============================================

**Sample Run #2:**
Music Recommender — RAG Edition
=============================================
Describe the music you're in the mood for:
> sad songs for a rainy day

[1/3] Parsing your description...
      Detected: genre=ambient, mood=moody, energy=0.2, acoustic=True

[2/3] Retrieving songs...
Loading songs from data/songs.csv...
Loaded songs: 20
  [retrieval] AI suggested 10 additional songs.
      Catalog size: 30 songs total

[3/3] Finding your top 5 and generating explanations...

=============================================
   Top 5 Recommendations For You
=============================================

#1  Galactic Drift — Orbit Bloom
    Score : 3.48
    Why   : Its dreamy, spacious ambient soundscapes provide a gentle, melancholic soundtrack for a quiet, rainy afternoon.

#2  Spacewalk Thoughts — Orbit Bloom
    Score : 3.42
    Why   : Its soothing ambient tones provide a gentle, reflective soundtrack for gazing out a rain-streaked window.

#3  Lua — Bright Eyes
    Score : 2.98
    Why   : Conor Oberst’s fragile vocals and stark acoustic melancholy perfectly capture the heavy, isolated feeling of a rainy day.

#4  Hurt — Johnny Cash
    Score : 2.95
    Why   : Cash’s haunting, weathered vocals and melancholic acoustic guitar create a devastatingly somber atmosphere that mirrors a rainy day.

#5  Liability — Lorde
    Score : 2.94
    Why   : Lord's haunting vocals and minimalist piano capture the profound, rainy-day loneliness of feeling like too much baggage.

=============================================
---

## Design Decisions

**Gemini-Only RAG:**
- Avoided using additional song retrieval APIS (such as Last.fm API) since Gemini can suggest real songs directly, which eliminated the need for a second API key and simplified deployment.

**Three-Stage Pipeline:**
- Parse → Retrieve → Explain workflow cleanly separates concerns. The parser focuses on understanding user's music preference; the retriever expands the catalog; the explainer contextualizes each recommendation. This makes the system easy to extend or replace individual stages.

**Prompt Engineering for Token Efficiency:**
- All prompts are kept brief to minimize token usage and quota limits on the free tier. The parser and explainer use single sentences; the retriever uses minimal formatting.

---

## Reliability Testing Summary

**Test Cases (`tests/test_recommender.py`):**
============================================================================== test session starts ==============================================================================
platform win32 -- Python 3.13.9, pytest-9.0.3, pluggy-1.6.0 -- c:\Users\wendy2.0\Downloads\Codepath\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\wendy2.0\Downloads\Codepath\AI110\applied-ai-system-final\tests
plugins: anyio-4.13.0
collected 12 items                                                                                                                                                               

test_recommender.py::test_recommend_returns_songs_sorted_by_score PASSED                                                                                                   [  8%]
test_recommender.py::test_explain_recommendation_returns_non_empty_string PASSED                                                                                           [ 16%]
test_recommender.py::test_parse_user_description_returns_valid_dict PASSED                                                                                                 [ 25%]
test_recommender.py::test_parse_user_description_returns_valid_values PASSED                                                                                               [ 33%]
test_recommender.py::test_fetch_songs_from_llm_returns_list PASSED                                                                                                         [ 41%]
test_recommender.py::test_fetch_songs_from_llm_returns_valid_song_dicts PASSED                                                                                             [ 50%]
test_recommender.py::test_explain_recommendation_dict_returns_string PASSED                                                                                                [ 58%]
test_recommender.py::test_explain_recommendation_dict_incorporates_user_preference PASSED                                                                                  [ 66%]
test_recommender.py::test_score_song_matches_genre_and_mood PASSED                                                                                                         [ 75%]
test_recommender.py::test_score_song_considers_energy_proximity PASSED                                                                                                     [ 83%]
test_recommender.py::test_recommend_songs_returns_top_k PASSED                                                                                                             [ 91%]
test_recommender.py::test_recommend_songs_sorted_by_score PASSED                                                                                                           [100%]

============================================================================== 12 passed in 9.03s ===============================================================================
---

## Reflection

I learned how to integrate a RAG system to make projects more powerful and practical for real users. Semantic parsing and search allows users to freely enter input without being constrained to pre-defined music taste categories. It also expanded understanding of the user and allowed better song recommendations. 

This project reinforced that RAG systems require careful orchestration. It was difficult to find the right LLM model that worked on a free tier with no billing. That taught me to test early and iterate on model choice, not just assume the latest model or the most advanced model is the best fit for my resource constraints.

---