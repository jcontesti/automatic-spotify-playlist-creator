from pathlib import Path
import json
from abc import ABC, abstractmethod


class MisspellingCorrector(ABC):

    CACHE_SEPARATOR = "@@@"

    def __init__(
        self, cache_path,
    ):
        self._cache_path = cache_path
        self._load_cached_misspelling_corrections()

    def _load_cached_misspelling_corrections(self):
        self._misspelling_corrections = {}

        if Path(self._cache_path).exists():
            with open(self._cache_path, "r") as file:
                self._misspelling_corrections = json.loads(file.read())

    def _update_cached_misspelling_corrections(self):
        with open(self._cache_path, "w") as file:
            file.write(json.dumps(self._misspelling_corrections))

    def _encode_artist_song(self, artist, song):
        return artist + self.CACHE_SEPARATOR + song

    def _decode_artist_song(self, artist_song):
        split = artist_song.split(self.CACHE_SEPARATOR)
        return {"artist": split[0], "song": split[1]}

    def _cache_correction(self, artist, song, corrected_artist, corrected_song):
        key = self._encode_artist_song(artist, song)
        value = self._encode_artist_song(corrected_artist, corrected_song)
        self._misspelling_corrections[key] = value
        self._update_cached_misspelling_corrections()

    def _get_from_cached_misspelling_corrections(self, artist, song):
        key = self._encode_artist_song(artist, song)
        return (
            self._misspelling_corrections[key]
            if key in self._misspelling_corrections
            else None
        )

    @abstractmethod
    def correct(self, artist, song):
        pass
