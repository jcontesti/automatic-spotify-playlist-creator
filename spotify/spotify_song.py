from . import spotify_album
import spotipy

class SpotifySong:
    def __init__(self, song: [str]):
        self._song = song

    @property
    def id(self) -> str:
        return self._song["tracks"]["items"][0]["id"]

    @property
    def album(self) -> spotify_album.SpotifyAlbum:
        return spotify_album.SpotifyAlbum(self._song["tracks"]["items"][0]["album"])

    def is_empty(self) -> bool:
        return not self._song["tracks"]["items"]

    def is_released_in_last_year(self) -> bool:
        return self.album.is_released_in_last_year()

    @staticmethod
    def get_song_from_id(
            sp: spotipy.Spotify,
            song_id: str,
    ) -> 'SpotifySong':
        return SpotifySong(sp.track(song_id))
