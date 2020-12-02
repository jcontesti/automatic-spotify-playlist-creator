from .extracted_song import ExtractedSong
from typing import List


class ExtractedPlaylist:

    def __init__(
            self,
    ) -> None:
        self._extracted_songs: List[ExtractedSong] = []

    def add_extracted_song(self, extracted_song: ExtractedSong) -> None:
        self._extracted_songs.append(extracted_song)

    def clean_playlist(self) -> None:
        # One scrapped song can include many artists and song titles, but one album
        # and one label

        cleaned_extracted_songs: List[ExtractedSong] = []

        for extracted_song in self._extracted_songs:
            separated_artists = extracted_song.get_separated_artists()
            separated_titles = extracted_song.get_separated_titles()
            album_title = extracted_song.album_title
            label = extracted_song.label

            for separated_artist in separated_artists:
                for separated_title in separated_titles:

                    separated_labels_song = ExtractedSong(
                        separated_artist,
                        separated_title,
                        album_title,
                        label,
                    )
                    separated_labels_song.format()

                    cleaned_extracted_songs.append(separated_labels_song)

        self._extracted_songs = cleaned_extracted_songs

    def get_songs(self) -> List[ExtractedSong]:
        return self._extracted_songs
