# 🎵 Music Recommender Simulation

## Project Summary

VibeFinder 1.0 is a small content-based music recommender written in Python. It loads an 18-song catalog from a CSV file, compares every song to a user's taste profile (favorite genre, favorite mood, target energy, and optionally a liking for acoustic sound), gives each song a score with a list of reasons, and prints the top 5 matches in the terminal.

---

## How The System Works

Real platforms like Spotify and YouTube mix two ideas. **Collaborative filtering** looks at the behavior of many users (likes, skips, replays, playlist adds, follows) and recommends what similar listeners enjoyed. **Content-based filtering** looks at the songs themselves (genre, mood, tempo, energy, acousticness) and recommends tracks that resemble what a user already likes. Big apps combine both with huge amounts of data. My version is purely content-based: it only uses song attributes and one user profile, and it prioritizes genre first, then mood, then how close the energy level is.

**Song features used:** `genre`, `mood`, `energy`, `acousticness` (the CSV also stores `tempo_bpm`, `valence`, and `danceability`).

**UserProfile features used:** `favorite_genre` / `genre`, `favorite_mood` / `mood`, `target_energy` / `energy`, `likes_acoustic`.

### Algorithm Recipe

| Rule | Points |
|---|---|
| Genre matches the user's genre | +2.0 |
| Mood matches the user's mood | +1.0 |
| Energy similarity | +1.0 × (1 − \|song energy − target energy\|) |
| Acoustic fit (only if the profile sets `likes_acoustic`) | +0.5 × acousticness (or 1 − acousticness if they dislike acoustic) |

The energy rule rewards songs that are *close* to the target instead of simply higher or lower. The **scoring rule** judges one song at a time; the **ranking rule** applies it to every song in the catalog, sorts by score from highest to lowest, and keeps the top k. You need both: a score alone doesn't tell you what to show first, and a ranking needs a score to sort by.

### Data Flow

```
User prefs (genre, mood, energy)
        |
        v
Load data/songs.csv  ->  for each song: score_song() -> (score, reasons)
        |
        v
sorted(..., reverse=True)  ->  Top K recommendations with reasons
```

### Expected Biases

Genre is worth twice as much as mood, so the system may over-prioritize genre and ignore great songs that match the user's mood. Exact string matching also means "indie pop" gets no genre credit for a "pop" fan.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

```bash
pytest
```

---

## Sample Recommendation Output

Default "pop / happy" profile:

```
Loaded songs: 18

============================================================
Profile: High-Energy Pop  {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
============================================================
1. Sunrise City by Neon Echo  [pop/happy]
   Score: 3.98
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+0.98)
2. Gym Hero by Max Pulse  [pop/intense]
   Score: 2.87
   Reasons: genre match (+2.0), energy similarity (+0.87)
3. Rooftop Lights by Indigo Parade  [indie pop/happy]
   Score: 1.96
   Reasons: mood match (+1.0), energy similarity (+0.96)
4. Concrete Crown by Block Theory  [hip hop/confident]
   Score: 0.98
   Reasons: energy similarity (+0.98)
5. Night Drive Loop by Neon Echo  [synthwave/moody]
   Score: 0.95
   Reasons: energy similarity (+0.95)
```

Output for all tested profiles is in the [Model Card](model_card.md#7-evaluation).

---

## Experiments You Tried

- **Expanded the dataset** from 10 to 18 songs, adding hip hop, r&b, country, edm, classical, metal, blues, and reggae.
- **Weight shift:** halved genre (2.0 → 1.0) and doubled energy (1.0 → 2.0). For the pop/happy profile, Rooftop Lights (indie pop, happy) jumped above Gym Hero (pop, intense). That felt more accurate, since a happy listener probably prefers a happy song over a workout track. The results became different and slightly better for mood, but songs with no genre or mood match also crept closer to the top.
- **Edge cases:** a "high energy + sad" profile and an unknown genre ("k-pop") profile. See the model card for details.

---

## Limitations and Risks

- It only works on a tiny 18-song catalog.
- It does not understand lyrics, language, or listening history.
- Genre is matched by exact text, so related genres ("pop" vs. "indie pop") get no credit.
- Genre is weighted heavily, which can trap users in a filter bubble.

---

## Reflection

[**Model Card**](model_card.md)

Building this showed me that a recommender is just a scoring rule plus a sort. Turning a user's taste into numbers (a genre, a mood, a target energy) and measuring how close each song is to those numbers is enough to produce results that feel personal. The explanations ("genre match (+2.0)") made it easy to see exactly why a song ranked where it did.

It also showed me where bias comes from. The weights I picked decide what matters, and the catalog decides what is even possible. Most genres have only one song, so a metal fan gets one real match and then a pile of loosely related high-energy tracks. A real system with skewed data or heavy weights could quietly keep users in the same small bubble without them noticing.
