from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """A single song and its audio/metadata attributes loaded from songs.csv."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    instrumentalness: float
    speechiness: float
    liveness: float

@dataclass
class UserProfile:
    """A user's taste preferences used to score and rank songs."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

MOOD_NEIGHBORS = {
    "happy":     ["relaxed"],
    "chill":     ["relaxed", "focused"],
    "intense":   ["moody"],
    "moody":     ["intense"],
    "relaxed":   ["happy", "chill"],
    "focused":   ["chill"],
    "sad":       ["moody"],
    "dreamy":    ["chill", "relaxed"],
    "nostalgic": ["sad", "moody"],
    "romantic":  ["relaxed", "happy"],
    "angry":     ["intense"],
}

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences; return (score, reasons) with max 6.0."""
    score = 0.0
    reasons = []

    # Genre match: +2.0 exact, +0.0 miss
    if song["genre"] == user_prefs["genre"]:
        score += 2.0
        reasons.append(f"genre match ({song['genre']}) (+2.0)")

    # Mood match: +1.5 exact, +0.75 adjacent, +0.0 miss
    if song["mood"] == user_prefs["mood"]:
        score += 1.5
        reasons.append(f"mood match ({song['mood']}) (+1.5)")
    elif song["mood"] in MOOD_NEIGHBORS.get(user_prefs["mood"], []):
        score += 0.75
        reasons.append(f"adjacent mood ({song['mood']} ~ {user_prefs['mood']}) (+0.75)")

    # Energy similarity: up to +2.0 using squared distance penalty
    energy_pts = 2.0 * (1.0 - (song["energy"] - user_prefs["target_energy"]) ** 2)
    score += energy_pts
    reasons.append(f"energy {song['energy']} vs target {user_prefs['target_energy']} (+{energy_pts:.2f})")

    # Acoustic alignment: up to +0.5
    if user_prefs["likes_acoustic"]:
        acoustic_pts = 0.5 * song["acousticness"]
    else:
        acoustic_pts = 0.5 * (1.0 - song["acousticness"])
    score += acoustic_pts
    reasons.append(f"acoustic alignment (+{acoustic_pts:.2f})")

    return round(score, 3), reasons


class Recommender:
    """OOP wrapper around the scoring and ranking logic for use in tests."""

    def __init__(self, songs: List[Song]):
        """Store the song catalog for repeated recommendation calls."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by score for the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language string explaining why this song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to int/float."""
    import csv

    int_fields   = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness",
                    "instrumentalness", "speechiness", "liveness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)

    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort by score descending, and return the top k as (song, score, reasons)."""
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]

    return sorted(scored, key=lambda x: (x[1], x[0]["valence"]), reverse=True)[:k]
