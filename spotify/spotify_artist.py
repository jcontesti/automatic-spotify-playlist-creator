"""Class that represents an artist in Spotify."""
from typing import Any
from typing import Dict, List

import spotipy


class SpotifyArtist:
    """Class that represents an artist in Spotify."""

    def __init__(self, artist: Dict[str, Any]):
        self._artist = artist

    @property
    def id(self) -> Any:  # pylint: disable=invalid-name
        """
        Return the Spotify identification of the artist.

        :return: Spotify identification of the artist.
        """
        return self._artist["id"]

    # pylint: disable=invalid-name
    def top_songs_ids(self, sp: spotipy.Spotify) -> List[str]:
        """
        Return the most played songs of the artist.

        :param sp: Spotify session object.
        :return: Spotify ids of the most played songs of the artist.
        """
        return [
            t["id"] for t in sp.artist_top_tracks(self.id)["tracks"]
        ]
