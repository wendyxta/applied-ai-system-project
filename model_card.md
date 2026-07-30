# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

Music Profiler
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

This recommender generates song recommendations from a list of 20 songs based on a user profiler. It assumes users can clearly state their song preferences, such as favorite genre, mod, energy level and uses those song attributees to recommend songs. It is for classroom exploration.
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

This model works by awarding each song in the provided song list a score based on how well its attributes match with the users song preferences. A genre match will be award the song 2 points, mood match awards 1.5 points, energy level 1 point, and accountuc match preference will be awarded 0.5 points. The songs with the highest points will be recommended to the user.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog contains 20 songs across 7 genres: pop, lofi, rock, indie pop, jazz, ambient, and synthwave. The moods represented are happy, chill, intense, relaxed, focused, and moody. No songs were added or removed from the starter dataset. However, the catalog is missing major genres like hip-hop, classical, and country, and it has no songs tagged with moods like "sad" or "melancholy," which are common listener states.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works best for users whose favorite genre is pop, lofi, or rock, since those genres have the most songs in the catalog, giving the scoring more variety to rank against. The energy proximity score rewards closeness on a smooth scale rather than a simple match or no-match, so a user who wants moderate energy still gets partial credit from nearby songs. Users whose preferences align with common combos like lofi + chill or pop + happy receive intuitive, satisfying top-5 results that feel genuinely relevant. The acoustic bonus also captures a real musical quality that genre and mood alone would miss.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The main limitations and biases are the limited song data and uneven weights. The genre weight is a bit heavier relative to the other signals that it creates a filter bubble. For example, once a user's favorite genre matches any song, that song will almost always rank above a cross-genre song, even if the cross-genre song fits the user's mood and energy far better. This means users whose preferred genre is well-represented in the catalog (like pop or lofi, each with 4 songs) receive a wider, more competitive recommendation pool, while users preferring a rarer genre like ambient (2 songs) get recommendations dominated by the same two songs every time.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I have checked whether the recommender behaved as expected by testing out all 3 user profiles, checking out the recommendations for each distinct profile, and make sure the recommendations are reasonable and that they are not the same across the different profiles. I also made sure that the songs that matched the genre listed in the user profile to appear at the top.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

In the future, I want to add a RAG component to the recommender to recommend songs with attributes based closeness to their meanings rather than a keyword match. This will help account for users creating profiles using specific words that are not already explicitly stated but mean the same thing. I might also add multi genre matches since some users may have multiple genre preferences.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I learned how biased a rule based recommender can be without intending to be biased. The biases came from the catalog of songs that are already biased and the recommender learned to recommend songs based on those biases. This made me realize how the song platforms that we use everyday like Spotify learn to be biased and how they recommend songs to us based on predictions from our music profile.
