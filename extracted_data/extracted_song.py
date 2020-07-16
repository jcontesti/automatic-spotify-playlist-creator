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
                 song_title: str,
                 album_title: str = "",
                 label: str = ""):
        self._artist = artist
        self._song_title = song_title
        self._album_title = album_title
        self._label = label

    @property
    def artist(self) -> str:
        return self._artist

    @property
    def song_title(self) -> str:
        return self._song_title

    @property
    def album_title(self) -> str:
        return self._album_title

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

        replaced_song_titles = None
        for split in self.TITLES_SEPARATORS:
            replaced_song_titles = self._song_title.replace(split, "#")

        if "#" in replaced_song_titles:
            separated_song_titles = replaced_song_titles.split("#")
        else:
            separated_song_titles = [replaced_song_titles]

        return separated_song_titles

    def format(self):
        self._artist = self._artist.lower().strip(" \t\n\r")
        self._song_title = self._song_title.lower().strip(" \t\n\r")
        self._album_title = self._album_title.lower().strip(" \t\n\r")
        self._label = self._label.lower().strip(" \t\n\r")

    def get_copy(self, artist: str, title: str) -> 'ExtractedSong':
        return ExtractedSong(
            artist,
            title,
            self._album_title,
            self._label
        )