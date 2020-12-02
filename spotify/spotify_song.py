from . import spotify_album
import spotipy


class SpotifySong:
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
            return self.id == other.id
        return False

    @property
    def id(self) -> str:
        return self._id

    @property
    def album(self) -> spotify_album.SpotifyAlbum:
        return self._album

    def is_released_in_last_year(self) -> bool:
        return self._album.is_released_in_last_year()
