from . import spotify_album


class SpotifyTrack:
    def __init__(self, track: [str]):
        self._track = track

    @property
    def id(self) -> str:
        return self._track["tracks"]["items"][0]["id"]

    @property
    def album(self) -> spotify_album.SpotifyAlbum:
        return spotify_album.SpotifyAlbum(self._track["tracks"]["items"][0]["album"])

    def is_empty(self) -> bool:
        return not self._track["tracks"]["items"]
