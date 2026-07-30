# 🎵 Music Recommender Simulation (Part 2)

## Project Summary

**Original Project Goals:**
- The Music Recommender imports 20 songs from a CSV file and constructs predefined music taste user profiles. The system will then score the songs based on how well a given user profiles and recommends the top 5 songs with the closest match to the user's music taste. 

**Extended Capabilities (Retrieval-Augmented Generation (RAG) Integration):**
- The extended Music Recommender will integrate RAG components to use semantic search to parse user preference input to expand beyond the 3 hard-coded user profiles from the original project. This better matches real life user input and allows for mroe flexible input. 
- The original 20 song catalog will also be expanded to use the Last.fm API to fetch real songs with matching user moods/genres. This allows users to have more song optiosn to explore that may more closely align with user preferences.
- An additional explanation for why each song was recommended based on the user's provided description will also be provided. This will provide a more meaningful understanding of why this song matches the user's music taste.

---

## Architecture Overview

The system is a three-stage RAG pipeline wrapped around the original rule-based scorer. See [`architecture.mmd`] for the full diagram.

**Stage 1 — Semantic Profile Parser (`profile_parser.py`):** The user types a free-text description and Gemini extracts a structured profile (genre, mood, energy, acoustic preference), enabling natural language input instead of hardcoded profiles.

**Stage 2 — Retriever (`retrieval.py` + `recommender.py`):** The local `songs.csv` (20 songs) is combined with real songs fetched from the Last.fm API by genre tag, expanding the catalog to ~40 candidates for the scorer to rank.

**Stage 3 — Explainer (`recommender.py`):** Each top-5 result is passed to Gemini with the user's original description, which generates one natural-language sentence explaining why that song fits.

**Testing and Human Evaluation:** `pytest` tests verify the scorer ranks correctly and the explainer returns a non-empty string. The user also manually spot-checks whether results match their description.

---

## Setup Instructions
Setup Instructions: Step-by-step directions to run your code.

---

## Sample Interactions
Sample Interactions: Include at least 2-3 examples of inputs and the resulting AI outputs to demonstrate the system is functional.

---

## Design Decisions
Design Decisions: Why you built it this way, and what trade-offs you made.

---

## Testing Summary
Testing Summary: What worked, what didn't, and what you learned.

---

## Reflection
Reflection: A brief note on what this project taught you about AI and problem-solving. Your graded responsible-AI reflection — how you collaborated with AI, one helpful and one flawed AI suggestion, and your system's limitations — goes in model_card.md (see Step 5), not here. Reflection content placed only in the README does not earn the reflection points.