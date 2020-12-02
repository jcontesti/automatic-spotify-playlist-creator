import spotipy
from typing import Dict, List
from typing import Any


class SpotifyArtist:
    def __init__(self, artist: Dict[str, Any]):
        self._artist = artist

    @property
    def id(self) -> Any:
        return self._artist["id"]

    def top_songs_ids(self, sp: spotipy.Spotify) -> List[str]:
        return [
            t["id"] for t in sp.artist_top_tracks(self.id)["tracks"]
        ]
