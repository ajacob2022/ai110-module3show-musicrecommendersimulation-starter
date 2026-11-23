from src.recommender import load_songs, recommend_songs

PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
    "Conflicted (High Energy + Sad)": {"genre": "blues", "mood": "sad", "energy": 0.9},
    "Unknown Genre (K-Pop)": {"genre": "k-pop", "mood": "happy", "energy": 0.7},
}


def print_recommendations(name: str, prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top k recommendations for a profile."""
    print("=" * 60)
    print(f"Profile: {name}  {prefs}")
    print("=" * 60)
    for i, (song, score, explanation) in enumerate(recommend_songs(prefs, songs, k), 1):
        print(f"{i}. {song['title']} by {song['artist']}  [{song['genre']}/{song['mood']}]")
        print(f"   Score: {score:.2f}")
        print(f"   Reasons: {explanation}")
    print()


def main() -> None:
    """Load the catalog and print recommendations for each profile."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")
    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
