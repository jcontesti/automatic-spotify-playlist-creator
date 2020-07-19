import spotipy
from typing import List

class SpotifyArtist:
    def __init__(self, artist: [str]):
        self._artist = artist

    @property
    def id(self) -> str:
        return self._artist["id"]

    def top_songs_ids(self, sp: spotipy.Spotify) -> List[str]:
        return [
            t["id"] for t in sp.artist_top_tracks(self.id)["tracks"]
        ]
