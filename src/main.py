"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


ADVERSARIAL_PROFILES = [
    {
        # Energy 0.9 pulls toward rock/metal; sad mood pulls toward folk/lofi.
        # The two signals point in opposite directions — who wins?
        "name":           "EDGE: Conflicting Energy vs Mood",
        "genre":          "rock",
        "mood":           "sad",
        "target_energy":  0.90,
        "likes_acoustic": False,
    },
    {
        # Genre that exists in catalog with only one song (metal).
        # After Iron Cathedral, what fills positions 2-5?
        "name":           "EDGE: Single-Song Genre (metal)",
        "genre":          "metal",
        "mood":           "angry",
        "target_energy":  0.95,
        "likes_acoustic": False,
    },
    {
        # Energy 0.5 is equidistant from many songs — nearly every song
        # gets a similar energy score, so genre/mood dominate everything.
        "name":           "EDGE: Dead-Center Energy (0.5)",
        "genre":          "jazz",
        "mood":           "relaxed",
        "target_energy":  0.50,
        "likes_acoustic": True,
    },
    {
        # likes_acoustic=True but high energy target — high-energy songs
        # are almost always electronic (low acousticness). Can a song satisfy both?
        "name":           "EDGE: Acoustic + High Energy Contradiction",
        "genre":          "folk",
        "mood":           "intense",
        "target_energy":  0.90,
        "likes_acoustic": True,
    },
    {
        # Genre and mood that share zero songs in the catalog.
        # Pure energy + acoustic scoring drives all results.
        "name":           "EDGE: No Catalog Match (classical + angry)",
        "genre":          "classical",
        "mood":           "angry",
        "target_energy":  0.50,
        "likes_acoustic": False,
    },
]

PROFILES = [
    {
        "name":           "High-Energy Pop",
        "genre":          "pop",
        "mood":           "happy",
        "target_energy":  0.85,
        "likes_acoustic": False,
    },
    {
        "name":           "Chill Lofi",
        "genre":          "lofi",
        "mood":           "focused",
        "target_energy":  0.40,
        "likes_acoustic": True,
    },
    {
        "name":           "Deep Intense Rock",
        "genre":          "rock",
        "mood":           "intense",
        "target_energy":  0.90,
        "likes_acoustic": False,
    },
    {
        "name":           "Melancholic Evening",
        "genre":          "folk",
        "mood":           "sad",
        "target_energy":  0.30,
        "likes_acoustic": True,
    },
    {
        "name":           "Friday Night EDM",
        "genre":          "edm",
        "mood":           "intense",
        "target_energy":  0.92,
        "likes_acoustic": False,
    },
]


def print_recommendations(profile: dict, songs: list, k: int = 5) -> None:
    """Print a formatted recommendation block for one user profile."""
    print(f"\n{'='*54}")
    print(f"  Profile : {profile['name']}")
    print(f"{'='*54}")
    print(f"  Genre   : {profile['genre']}")
    print(f"  Mood    : {profile['mood']}")
    print(f"  Energy  : {profile['target_energy']}")
    print(f"  Acoustic: {'yes' if profile['likes_acoustic'] else 'no'}")

    user_prefs = {k: v for k, v in profile.items() if k != "name"}
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print(f"\n  Top {len(recommendations)} Recommendations:\n")
    for i, (song, score, reasons) in enumerate(recommendations, 1):
        filled = round(score / 6.0 * 20)
        bar = f"[{'#' * filled}{'-' * (20 - filled)}]"
        print(f"  #{i}  {song['title']} by {song['artist']}")
        print(f"       Score : {score:.3f} / 6.0  {bar}")
        print(f"       Why   :")
        for reason in reasons:
            print(f"                - {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"\n{'='*54}")
    print(f"  Catalog: {len(songs)} songs loaded")
    print(f"{'='*54}")
    for song in songs:
        print(f"  {song['id']:>2}. {song['title']:<28} [{song['genre']:<10}] [{song['mood']:<10}] energy={song['energy']:.2f}")

    for profile in PROFILES:
        print_recommendations(profile, songs, k=5)

    print(f"\n{'='*54}")
    print(f"  ADVERSARIAL / EDGE CASE PROFILES")
    print(f"{'='*54}")
    for profile in ADVERSARIAL_PROFILES:
        print_recommendations(profile, songs, k=5)


if __name__ == "__main__":
    main()
