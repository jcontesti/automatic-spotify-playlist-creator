from . import spotify_album
import spotipy


class SpotifySong:
    def __init__(self, session: spotipy.Spotify, song_id: str):

        source = session.track(song_id)
        self._id: str = source["id"]
        self._album = spotify_album.SpotifyAlbum(session, source["album"]["id"])
        self._session = session

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._id == other.id

    @property
    def id(self) -> str:
        return self._id

    @property
    def album(self) -> spotify_album.SpotifyAlbum:
        return self._album

    def is_released_in_last_year(self) -> bool:
        return self._album.is_released_in_last_year()
