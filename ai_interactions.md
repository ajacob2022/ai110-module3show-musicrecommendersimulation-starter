# AI Interactions Log

---

## Agentic Workflow (SF8)

**What task did you give the agent?**

I asked an AI coding agent to complete the full recommender in one pass: expand the dataset, implement loading, scoring, and ranking, build a multi-profile CLI, run an experiment, and fill in the README and model card with real terminal output.

**Prompts used:**

- "Implement `load_songs` using Python's `csv` module so it returns a list of dictionaries, converting `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness` to floats and `id` to an int."
- "Implement `score_song` with +2.0 for a genre match, +1.0 for a mood match, and up to +1.0 for energy based on `1 - abs(song_energy - target_energy)`. Return the score and a list of reasons like `genre match (+2.0)`."
- "Write `recommend_songs` in the most Pythonic way: score every song, sort from highest to lowest, and return the top k."
- "Add 8 songs to `songs.csv` with genres and moods not already in the file."
- "Suggest adversarial user profiles that could trick the scoring logic, then run all profiles and show the top 5 for each."
- "Halve the genre weight and double the energy weight, verify the math is still valid, and compare the rankings."

**What did the agent generate or change?**

- `data/songs.csv`: added 8 songs (hip hop, r&b, country, edm, classical, metal, blues, reggae).
- `src/recommender.py`: implemented `load_songs`, `score_song`, `recommend_songs`, and the `Recommender` class methods, with weights stored as constants so experiments only need a number change.
- `src/main.py`: fixed the import so `python -m src.main` works, added five user profiles, and formatted the output with title, score, and reasons.
- Ran `python -m src.main` and `pytest`, and ran the weight-shift experiment without editing the source file.
- `README.md` and `model_card.md`: wrote the documentation and pasted the real terminal output.

**What did you verify or fix manually?**

- Ran `python -m src.main` myself to confirm the output in the docs matched the actual results.
- Checked the scores by hand. For example, Sunrise City for the pop profile: 2.0 + 1.0 + (1 − |0.82 − 0.80|) = 3.98.
- Confirmed the energy score can never go negative, since all energy values are between 0 and 1.
- Ran `pytest` to make sure both starter tests pass.
- Reviewed the bias and reflection sections and rewrote them in my own words where they didn't match what I noticed.

---

## Design Pattern (SF10)

**Which design pattern did you use?**

Facade (with a small Adapter step).

**How did AI help you brainstorm or implement it?**

The starter code needed two interfaces: dictionary-based functions for `main.py` and a `Recommender` class with `Song` and `UserProfile` dataclasses for the tests. I asked the AI how to support both without writing the scoring logic twice. It suggested keeping one scoring function as the single source of truth and making the class a thin wrapper that converts its dataclasses into dictionaries before calling it.

**How does the pattern appear in your final code?**

In `src/recommender.py`, `Recommender.recommend` and `Recommender.explain_recommendation` act as a facade over `score_song`. The helper `_profile_to_prefs` adapts a `UserProfile` into the preference dictionary, and `dataclasses.asdict` adapts each `Song`. Changing a weight constant like `GENRE_WEIGHT` updates both the CLI and the class-based interface at once.
