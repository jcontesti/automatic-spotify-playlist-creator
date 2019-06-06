from . import album


class Track:
    def __init__(self, track):
        self._track = track

    def _items(self):
        return self._track['tracks']['items']

    @property
    def id(self):
        return self._track['tracks']['items'][0]['id']

    @property
    def album(self):
        return album.Album(self._track['tracks']['items'][0]['album'])

    def empty(self):
        return not self._track['tracks']['items']
