# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests the top 5 songs from a small catalog that best fit a user's favorite genre, favorite mood, and preferred energy level. It assumes the user can describe their taste with one genre, one mood, and one energy number. It is built for classroom exploration of how recommenders work, not for real users.

**Not intended for:** real streaming products, users with mixed or changing tastes, or any decision where fairness to artists matters. It has no listening history and a tiny catalog.

---

## 3. How the Model Works

Every song gets points:

- **+2 points** if its genre is the user's favorite genre.
- **+1 point** if its mood is the user's favorite mood.
- **Up to +1 point** for energy. A song with the exact energy the user wants gets the full point; the further away it is, the fewer points it gets.
- **Up to +0.5 points** for acoustic sound, only if the user says whether they like acoustic music.

Then every song is sorted from highest to lowest score and the top 5 are shown with the reasons they earned points. Compared to the starter code (which returned nothing), I added the CSV loader, the scoring rules, the ranking, and readable explanations.

---

## 4. Data

The catalog has **18 songs**. I started with 10 and added 8 to cover more genres and moods.

- **Genres:** pop (2), lofi (3), rock, ambient, jazz, synthwave, indie pop, hip hop, r&b, country, edm, classical, metal, blues, reggae (1 each).
- **Moods:** happy, chill, intense, relaxed, moody, focused, confident, romantic, nostalgic, euphoric, peaceful, angry, sad.
- **Features:** genre, mood, energy, tempo, valence, danceability, acousticness.

Missing: lyrics, language, era, artist popularity, and real listening behavior. Most genres have only one song, so many users get only one true match.

---

## 5. Strengths

- Clear profiles (Chill Lofi, Deep Intense Rock) get results that match intuition: the top picks share genre, mood, and energy.
- The energy rule correctly fills the rest of the list with songs that "feel" similar, like EDM and metal for a rock fan.
- Every recommendation comes with reasons, so it's easy to see why a song was chosen.

---

## 6. Limitations and Bias

The biggest weakness is that genre dominates. A genre match is worth 2 points, more than a perfect mood and perfect energy match combined in most cases, so "Gym Hero" (an intense workout pop song) ranks above "Rooftop Lights" (a happy indie pop song) for someone who wants happy pop. Genre is also matched by exact text, so "indie pop" gets zero genre credit from a "pop" fan. Because most genres have only one song, users of those genres get one strong match and then a list padded with unrelated songs that just have similar energy. This creates a filter bubble where the system keeps repeating the same few songs from the user's genre instead of exploring songs with the right vibe.

---

## 7. Evaluation

I tested five profiles: three normal ones (High-Energy Pop, Chill Lofi, Deep Intense Rock) and two edge cases (a conflicting "high energy + sad" blues fan and a "k-pop" fan whose genre isn't in the catalog).

```
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

```
============================================================
Profile: Chill Lofi  {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}
============================================================
1. Library Rain by Paper Lanterns  [lofi/chill]
   Score: 4.43
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+1.00), acoustic fit (+0.43)
2. Midnight Coding by LoRoom  [lofi/chill]
   Score: 4.29
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+0.93), acoustic fit (+0.35)
3. Focus Flow by LoRoom  [lofi/focused]
   Score: 3.34
   Reasons: genre match (+2.0), energy similarity (+0.95), acoustic fit (+0.39)
4. Spacewalk Thoughts by Orbit Bloom  [ambient/chill]
   Score: 2.39
   Reasons: mood match (+1.0), energy similarity (+0.93), acoustic fit (+0.46)
5. Coffee Shop Stories by Slow Stereo  [jazz/relaxed]
   Score: 1.43
   Reasons: energy similarity (+0.98), acoustic fit (+0.45)
```

```
============================================================
Profile: Deep Intense Rock  {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}
============================================================
1. Storm Runner by Voltline  [rock/intense]
   Score: 4.44
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+0.99), acoustic fit (+0.45)
2. Gym Hero by Max Pulse  [pop/intense]
   Score: 2.44
   Reasons: mood match (+1.0), energy similarity (+0.97), acoustic fit (+0.47)
3. Neon Overdrive by Pulse Arcade  [edm/euphoric]
   Score: 1.43
   Reasons: energy similarity (+0.94), acoustic fit (+0.48)
4. Iron Verdict by Graveshift  [metal/angry]
   Score: 1.40
   Reasons: energy similarity (+0.92), acoustic fit (+0.48)
5. Sunrise City by Neon Echo  [pop/happy]
   Score: 1.33
   Reasons: energy similarity (+0.92), acoustic fit (+0.41)
```

```
============================================================
Profile: Conflicted (High Energy + Sad)  {'genre': 'blues', 'mood': 'sad', 'energy': 0.9}
============================================================
1. Rainy Window Blues by Otis Gray  [blues/sad]
   Score: 3.43
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+0.43)
2. Storm Runner by Voltline  [rock/intense]
   Score: 0.99
   Reasons: energy similarity (+0.99)
3. Gym Hero by Max Pulse  [pop/intense]
   Score: 0.97
   Reasons: energy similarity (+0.97)
4. Neon Overdrive by Pulse Arcade  [edm/euphoric]
   Score: 0.94
   Reasons: energy similarity (+0.94)
5. Iron Verdict by Graveshift  [metal/angry]
   Score: 0.92
   Reasons: energy similarity (+0.92)
```

```
============================================================
Profile: Unknown Genre (K-Pop)  {'genre': 'k-pop', 'mood': 'happy', 'energy': 0.7}
============================================================
1. Rooftop Lights by Indigo Parade  [indie pop/happy]
   Score: 1.94
   Reasons: mood match (+1.0), energy similarity (+0.94)
2. Sunrise City by Neon Echo  [pop/happy]
   Score: 1.88
   Reasons: mood match (+1.0), energy similarity (+0.88)
3. Night Drive Loop by Neon Echo  [synthwave/moody]
   Score: 0.95
   Reasons: energy similarity (+0.95)
4. Concrete Crown by Block Theory  [hip hop/confident]
   Score: 0.92
   Reasons: energy similarity (+0.92)
5. Island Sway by Coral Kings  [reggae/relaxed]
   Score: 0.88
   Reasons: energy similarity (+0.88)
```

### Comparing profiles

- **High-Energy Pop vs. Chill Lofi:** The pop profile gets bright, upbeat songs around energy 0.8, while the lofi profile shifts to quiet, acoustic tracks around 0.35. This makes sense because the two profiles want opposite energy levels and the lofi fan likes acoustic sound.
- **High-Energy Pop vs. Deep Intense Rock:** Both want high energy, so they share songs like Gym Hero and Sunrise City. Gym Hero is #2 for both, but for different reasons: for pop it matches the genre, for rock it matches the "intense" mood.
- **Chill Lofi vs. Deep Intense Rock:** These have zero overlap. Lofi gets soft acoustic songs and rock gets loud electric ones. The acoustic rule pushes them even further apart.
- **Deep Intense Rock vs. Conflicted (High Energy + Sad):** After the one blues song, the conflicted list looks almost identical to the rock list (Storm Runner, Gym Hero, Neon Overdrive, Iron Verdict). With no "sad and loud" songs in the catalog, energy takes over and the user gets intense workout music, which doesn't fit "sad" at all.
- **High-Energy Pop vs. Unknown Genre (K-Pop):** Without any genre match, the k-pop profile falls back to mood and energy. Rooftop Lights beats Sunrise City because its energy (0.76) is closer to 0.7. This is a reasonable fallback, but the system can't tell that k-pop is close to pop.

### Why does "Gym Hero" keep showing up for Happy Pop?

Gym Hero is labeled "pop," and a genre match alone is worth 2 points. Rooftop Lights is happy, which is what the user asked for, but it's labeled "indie pop," so it only gets 1 point for mood. In plain terms: the system cares more about the label on the box than the feeling of the song.

### Experiment: Weight Shift

I halved the genre weight (2.0 → 1.0) and doubled the energy weight (1.0 → 2.0). The math stays valid: the maximum score is still 4.0 without the acoustic rule.

```
Profile: High-Energy Pop  {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
1. Sunrise City by Neon Echo  [pop/happy]          Score: 3.96
2. Rooftop Lights by Indigo Parade  [indie pop/happy]  Score: 2.92
3. Gym Hero by Max Pulse  [pop/intense]            Score: 2.74
4. Concrete Crown by Block Theory  [hip hop/confident] Score: 1.96
5. Night Drive Loop by Neon Echo  [synthwave/moody]    Score: 1.90
```

Rooftop Lights moved above Gym Hero, which feels more accurate for a happy listener. For the conflicted profile, the high-energy songs moved much closer to the blues song (1.98 vs. 2.86), so the results became different but not better there. I kept the original weights as the default.

### What surprised me

How quickly the list falls back to "whatever has similar energy" once the genre and mood matches run out. Iron Verdict (an angry metal song) shows up for a sad blues listener just because both are loud.

---

## 8. Future Work

- Use genre similarity (so "indie pop" counts partly as "pop") instead of exact matching.
- Add valence, tempo, and danceability to the score, and let users like multiple genres or moods.
- Add a diversity rule so the top 5 doesn't repeat the same genre or artist.

---

## 9. Personal Reflection

My biggest learning moment was seeing how much the weights control the results. Changing two numbers reshuffled the top 5 for every user. AI tools helped me brainstorm new songs for the CSV, suggest edge-case profiles, and explain the difference between `.sort()` (changes the list in place) and `sorted()` (returns a new list). I still had to double-check the outputs by running the code and checking the math by hand, for example confirming that the energy similarity never goes below zero since all energies are between 0 and 1.

It surprised me that something this simple still "feels" like a real recommendation. Seeing reasons next to each song makes it seem smart, even though it's just adding up points. If I kept going, I would try a small collaborative-filtering version with fake listening histories and compare it to this content-based approach.
