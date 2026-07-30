# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version imports songs from a CSV file, constructs a user profile for music taste. It will then score the songs from the CSV based on how well they much the user's music taste. Lastly, it will recommend the top 5 songs that match closest with the user's music profile.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

------------------------------------------------------------
Understanding the Problem (Phase 1)
  My system will use the genre, mood, energym valence, danceability, tempo, and accusticness from each song. The UserProfile stores the user's music taste preference, based on their favorite genre, favorite mood, target energy, and whether or not they like acoustics. 
  The Recommender will calculate a score for each system based on weightings and mathematical formulas. The genre and mood categories are most important so they will have the highest weights at 30%, and 20% respectively. Energy and valence are the most important, and can both be weighted at 15%. Danceability, accousticness, and tempo are less important, and can be weighted at 10%, 7%, and 3% respectively. To calculate the score, the system would mulitply each category weight with the corresponding details for the specific song, and add together all the categories. 
  Both a scoring rule and ranking rule is needed since the scoring rule scores each song based on how well it matches the user's preferences, and the ranking rule scores songs against each other to determine the order to recommend songs for the user. I would use the scoring rule first to find songs that best match the user preferences. Then use the ranking rule to recommend the songs that are closest to the user's preferences first.

---------------------------------------------------------
Algorithmn Logic (Phase 2)
Scoring of points based on weights:
  Feature	| Weight| Points Awarded
  Genre	| 30% |	3.0
  Mood | 20% |	2.0
  Energy	| 15%	| 1.5
  Valence	| 15%	| 1.5
  Danceability	| 10%	|1.0
  Acousticness	| 7%	|0.7
  Tempo	| 3%	| 0.3
  Total	| 100%	|10.0 (max)

Bias
- Since mood and genre are the highest weighted categories, the system may miss songs that may directly align with the user's energy, valence, danceability, tempo, and accousticness preference.

Data Flow
1. Input user preferences --> create user profiles
2. Loop through songs.csv --> use scoring logic to score each song based on user preferences
3. Output list of songs in order with closest matches to recommend first.
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:
Loading songs from data/songs.csv...
Loaded songs: 20

=============================================
   Top 5 Recommendations For You
=============================================

#1  Golden Hour — Paper Lanterns
    Score : 4.49 / 5.00
    Why   : genre match (+2.0), mood match (+1.5), energy proximity (+0.99)

#2  Sunrise City — Neon Echo
    Score : 4.48 / 5.00
    Why   : genre match (+2.0), mood match (+1.5), energy proximity (+0.98)

#3  Gym Hero — Max Pulse
    Score : 2.87 / 5.00
    Why   : genre match (+2.0), energy proximity (+0.87)

#4  Late Night Groove — Max Pulse
    Score : 2.85 / 5.00
    Why   : genre match (+2.0), energy proximity (+0.85)

#5  Electric Daydream — Neon Echo
    Score : 2.50 / 5.00
    Why   : mood match (+1.5), energy proximity (+1.0)

=============================================
```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

- experiment: changing the weight on genre from 2.0 to 0.5
- result: The cores are much lower overall, and the genre no longers seems as important. The song recommendations don't seem to be as reflective of the user's actual music taste.
- sample output:
=============================================
   Top 5 Recommendations For You
=============================================

#1  Thunder Clap — Voltline
    Score : 3.00 / 5.00
    Why   : genre match (+0.5), mood match (+1.5), energy proximity (+1.0)

#2  Storm Runner — Voltline
    Score : 2.96 / 5.00
    Why   : genre match (+0.5), mood match (+1.5), energy proximity (+0.96)

#3  Desert Highway — Sandstone Kings
    Score : 2.93 / 5.00
    Why   : genre match (+0.5), mood match (+1.5), energy proximity (+0.93)

#4  Gym Hero — Max Pulse
    Score : 2.48 / 5.00
    Why   : mood match (+1.5), energy proximity (+0.98)

#5  Sunrise City — Neon Echo
    Score : 0.87 / 5.00
    Why   : energy proximity (+0.87)

=============================================


Experiment 2: trying out different user profiles

test User profile 1: high energy pop
=============================================
   Top 5 Recommendations For You
=============================================

#1  Sunrise City — Neon Echo
    Score : 4.42 / 5.00
    Why   : genre match (+2.0), mood match (+1.5), energy proximity (+0.92)

#2  Golden Hour — Paper Lanterns
    Score : 4.39 / 5.00
    Why   : genre match (+2.0), mood match (+1.5), energy proximity (+0.89)

#3  Gym Hero — Max Pulse
    Score : 2.97 / 5.00
    Why   : genre match (+2.0), energy proximity (+0.97)

#4  Late Night Groove — Max Pulse
    Score : 2.75 / 5.00
    Why   : genre match (+2.0), energy proximity (+0.75)

#5  Electric Daydream — Neon Echo
    Score : 2.40 / 5.00
    Why   : mood match (+1.5), energy proximity (+0.9)

=============================================

test user profile 2: chill lofi
=============================================
   Top 5 Recommendations For You
=============================================

#1  Library Rain — Paper Lanterns
    Score : 5.00 / 5.00
    Why   : genre match (+2.0), mood match (+1.5), energy proximity (+1.0), acoustic match (+0.5)

#2  Midnight Coding — LoRoom
    Score : 4.93 / 5.00
    Why   : genre match (+2.0), mood match (+1.5), energy proximity (+0.93), acoustic match (+0.5)

#3  Study Hall — LoRoom
    Score : 3.47 / 5.00
    Why   : genre match (+2.0), energy proximity (+0.97), acoustic match (+0.5)

#4  Focus Flow — LoRoom
    Score : 3.45 / 5.00
    Why   : genre match (+2.0), energy proximity (+0.95), acoustic match (+0.5)

#5  Spacewalk Thoughts — Orbit Bloom
    Score : 2.93 / 5.00
    Why   : mood match (+1.5), energy proximity (+0.93), acoustic match (+0.5)

=============================================

test profile 3: deep_intense_rock

=============================================
   Top 5 Recommendations For You
=============================================

#1  Thunder Clap — Voltline
    Score : 4.50 / 5.00
    Why   : genre match (+2.0), mood match (+1.5), energy proximity (+1.0)

#2  Storm Runner — Voltline
    Score : 4.46 / 5.00
    Why   : genre match (+2.0), mood match (+1.5), energy proximity (+0.96)

#3  Desert Highway — Sandstone Kings
    Score : 4.43 / 5.00
    Why   : genre match (+2.0), mood match (+1.5), energy proximity (+0.93)

#4  Gym Hero — Max Pulse
    Score : 2.48 / 5.00
    Why   : mood match (+1.5), energy proximity (+0.98)

#5  Sunrise City — Neon Echo
    Score : 0.87 / 5.00
    Why   : energy proximity (+0.87)

=============================================
---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

The main limitations and biases are the limited song data and uneven weights. The genre weight is a bit heavier relative to the other signals that it creates a filter bubble. For example, once a user's favorite genre matches any song, that song will almost always rank above a cross-genre song, even if the cross-genre song fits the user's mood and energy far better. This means users whose preferred genre is well-represented in the catalog (like pop or lofi, each with 4 songs) receive a wider, more competitive recommendation pool, while users preferring a rarer genre like ambient (2 songs) get recommendations dominated by the same two songs every time.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

I learned how biased a rule based recommender can be without intending to be biased. The biases came from the catalog of songs that are already biased and the recommender learned to recommend songs based on those biases. This made me realize how the song platforms that we use everyday like Spotify learn to be biased and how they recommend songs to us based on predictions from our music profile.

