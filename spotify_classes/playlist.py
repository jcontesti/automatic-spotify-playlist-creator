class Playlist:
    def __init__(self, playlist):
        self._playlist = playlist

    @property
    def tracks_ids(self):
        return [t['track']['id'] for t in self._playlist['items']]
