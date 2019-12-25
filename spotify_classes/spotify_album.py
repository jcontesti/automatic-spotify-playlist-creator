from . import spotify_artist


class SpotifyAlbum:
    def __init__(self, album):
        self._album = album

    @property
    def id(self):
        return self._album['albums']['items'][0]['id']

    @property
    def main_artist(self):
        return spotify_artist.SpotifyArtist(self._album['albums']['items'][0]['artists'][0])

    @property
    def release_date(self):
        return self._album['release_date']

    @property
    def release_date_precision(self):
        return self._album['release_date_precision']

    def tracks_ids(self, sp):
        return [t['id'] for t in sp.album_tracks(self.id)['items']]

    def is_empty(self):
        return not self._album['albums']['items']
