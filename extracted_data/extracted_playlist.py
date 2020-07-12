from .extracted_song import ExtractedSong


class ExtractedPlaylist:

    def __init__(
            self,
    ):
        self._extracted_songs = []

    def add_extracted_song(self, extracted_song: ExtractedSong):
        self._extracted_songs.append(extracted_song)

    def clean_playlist(self):
        # One scrapped song can include many artists and song titles, but one album
        # and one label

        for extracted_song in self._extracted_songs:

            separated_artists = extracted_song.get_separated_artists()
            separated_titles = extracted_song.get_separated_titles()

            for separated_artist in separated_artists:
                for separated_title in separated_titles:
                    separated_labels_song = extracted_song.get_copy(
                        separated_artist,
                        separated_title
                    ).format()

                    self._extracted_songs.append(separated_labels_song)

            self._extracted_songs.remove(extracted_song)

    def get_songs(self) -> [ExtractedSong]:
        return self._extracted_songs
