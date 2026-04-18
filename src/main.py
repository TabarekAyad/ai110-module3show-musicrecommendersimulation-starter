"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"\n{'='*54}")
    print(f"  Catalog: {len(songs)} songs loaded")
    print(f"{'='*54}")
    for song in songs:
        print(f"  {song['id']:>2}. {song['title']:<28} [{song['genre']:<10}] [{song['mood']:<10}] energy={song['energy']:.2f}")

    # User taste profiles — swap the active one to test different recommendations

    # Profile 1: High-energy pop fan who wants upbeat workout music
    user_prefs = {
        "genre":          "pop",
        "mood":           "happy",
        "target_energy":  0.85,
        "likes_acoustic": False,
    }

    # Profile 2: Late-night focus session — lo-fi, calm, instrumental
    # user_prefs = {
    #     "genre":          "lofi",
    #     "mood":           "focused",
    #     "target_energy":  0.40,
    #     "likes_acoustic": True,
    # }

    # Profile 3: Melancholic evening — folk/indie, sad, acoustic storytelling
    # user_prefs = {
    #     "genre":          "folk",
    #     "mood":           "sad",
    #     "target_energy":  0.30,
    #     "likes_acoustic": True,
    # }

    # Profile 4: Friday night out — EDM/electronic, intense, high danceability
    # user_prefs = {
    #     "genre":          "edm",
    #     "mood":           "intense",
    #     "target_energy":  0.92,
    #     "likes_acoustic": False,
    # }

    print(f"\n{'='*54}")
    print(f"  User Profile")
    print(f"{'='*54}")
    print(f"  Genre   : {user_prefs['genre']}")
    print(f"  Mood    : {user_prefs['mood']}")
    print(f"  Energy  : {user_prefs['target_energy']}")
    print(f"  Acoustic: {'yes' if user_prefs['likes_acoustic'] else 'no'}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\n{'='*54}")
    print(f"  Top {len(recommendations)} Recommendations")
    print(f"{'='*54}\n")
    for i, (song, score, reasons) in enumerate(recommendations, 1):
        filled = round(score / 6.0 * 20)
        bar = f"[{'#' * filled}{'-' * (20 - filled)}]"
        print(f"  #{i}  {song['title']} by {song['artist']}")
        print(f"       Score : {score:.3f} / 6.0  {bar}")
        print(f"       Why   :")
        for reason in reasons:
            print(f"                - {reason}")
        print()


if __name__ == "__main__":
    main()
