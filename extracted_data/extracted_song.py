class ExtractedSong:

    ARTISTS_SEPARATORS = [
        ' & ',
        ' ft ',
        ' ft. ',
        ' feat ',
        ' feat. ',
        ' presents ',
        ' pres. ',
        ' with ',
        ' and ',
        ', ',
    ]

    TITLES_SEPARATORS = [
        '/',
        ' - ',
    ]

    def __init__(self,
                 artist: str,
                 title: str,
                 album: str = "",
                 label: str = ""):
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

    def get_separated_artists(self) -> [str]:
        # Split artists names into a list
        # For instance "Artist A feat. Artist B" returns ["Artist A", "Artist B"]

        replaced_artists = None
        for split in self.ARTISTS_SEPARATORS:
            replaced_artists = self._artist.replace(split, "#")

        if "#" in replaced_artists:
            separated_artists = replaced_artists.split("#")
        else:
            separated_artists = [replaced_artists]

        return separated_artists

    def get_separated_titles(self) -> [str]:
        # Split songs titles into a list
        # For instance "Song 1 / Song 2" returns ["Song 1", "Song 2"]

        replaced_titles = None
        for split in self.TITLES_SEPARATORS:
            replaced_titles = self._title.replace(split, "#")

        if "#" in replaced_titles:
            separated_titles = replaced_titles.split("#")
        else:
            separated_titles = [replaced_titles]

        return separated_titles

    def format(self):
        self._artist = self._artist.lower().strip(" \t\n\r")
        self._title = self._title.lower().strip(" \t\n\r")
        self._album = self._album.lower().strip(" \t\n\r")
        self._label = self._label.lower().strip(" \t\n\r")

    def get_copy(self, artist: str, title: str) -> ExtractedSong:
        return ExtractedSong(
            artist,
            title,
            self._album,
            self._label
        )
