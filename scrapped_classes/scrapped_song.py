class ScrappedSong:
    def __init__(self, artist, title, album, label):
        self._artist = artist
        self._title = title
        self._album = album
        self._label = label

    @property
    def artist(self):
        return self._artist

    @property
    def title(self):
        return self._title

    @property
    def album(self):
        return self._album

    @property
    def label(self):
        return self._label
