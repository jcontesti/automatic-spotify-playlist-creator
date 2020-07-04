class ScrappedSong:
    def __init__(self, artist: str, title: str, album: str, label: str):
        self._artist = artist
        self._title = title
        self._album = album
        self._label = label

    @property
    def artist(self) -> str:
        return self._artist

    @property
    def title(self) -> str:
        return self._title

    @property
    def album(self) -> str:
        return self._album

    @property
    def label(self) -> str:
        return self._label
