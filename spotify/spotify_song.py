"""Class that represents a Spotify song."""
import spotipy

from . import spotify_album


class SpotifySong:
    """Class that represents a Spotify song."""

    def __init__(self, session: spotipy.Spotify, song_id: str) -> None:
        source = session.track(song_id)
        self._id: str = source["id"]
        self._album: spotify_album.SpotifyAlbum = (
            spotify_album.SpotifyAlbum(session, source["album"]["id"])
        )
        self._session: spotipy.Spotify = session

    def __hash__(self) -> int:
        return hash(self._id)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SpotifySong):
            return self.song_id == other.song_id
        return False

    @property
    def song_id(self) -> str:
        """Return the Spotify id of the song."""
        return self._id

    @property
    def album(self) -> spotify_album.SpotifyAlbum:
        """Return the Spotify album of the song."""
        return self._album

    def is_released_in_last_year(self) -> bool:
        """
        Check if the song was released in the last 365 days.

        :return: True if the song was released in the last year, False otherwise.
        """
        return self._album.is_released_in_last_year()
