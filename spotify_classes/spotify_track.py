from . import spotify_album


class SpotifyTrack:
    def __init__(self, track):
        self._track = track

    def _items(self):
        return self._track["tracks"]["items"]

    @property
    def id(self):
        return self._track["tracks"]["items"][0]["id"]

    @property
    def album(self):
        return spotify_album.SpotifyAlbum(self._track["tracks"]["items"][0]["album"])

    def is_empty(self):
        return not self._track["tracks"]["items"]
