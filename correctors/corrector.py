from pathlib import Path
import json
import importlib


class Corrector:

    SEPARATOR = "@@@"

    def __init__(
        self, misspelling_correctors, cache_path="./misspelling_corrections_cache.json",
    ):
        self._misspelling_correctors = misspelling_correctors
        self._cache_path = cache_path
        self._load_misspelling_correctors()
        self._load_cached_misspelling_corrections()

    def _load_misspelling_correctors(self):
        self._correctors = []

        if self._misspelling_correctors:
            for misspelling_corrector in self._misspelling_correctors:
                misspelling_corrector_module = list(misspelling_corrector.keys())[0]
                misspelling_corrector_class = misspelling_corrector.get(
                    misspelling_corrector_module
                )

                corrector_module = importlib.import_module(misspelling_corrector_module)

                corrector = getattr(corrector_module, misspelling_corrector_class)

                self._correctors.append(corrector)

    def _load_cached_misspelling_corrections(self):
        self._misspelling_corrections = {}

        if Path(self._cache_path).exists():
            with open(self._cache_path, "r") as file:
                self._misspelling_corrections = json.loads(file.read())

        print(self._misspelling_corrections)

    def _update_cache_misspelling_corrections(self):
        Path(self._cache_path).rmdir()
        with open(self._cache_path, "w") as file:
            file.write(json.dumps(self._misspelling_corrections))

    def _get_key_cache_from_artist_song(self, artist, song):
        return artist + self.SEPARATOR + song

    def _cache_correction(self, artist, song, corrected_artist, corrected_song):
        key = self._get_key_cache_from_artist_song(artist, song)
        value = self._get_key_cache_from_artist_song(corrected_artist, corrected_song)
        self._misspelling_corrections[key] = value
        self._update_cache_misspelling_corrections()

    def correct(self, artist, song, func_find_song):

        artist_song_key = self._get_key_cache_from_artist_song(artist, song)

        corrected_values = self._misspelling_corrections.get(artist_song_key)
        if corrected_values is not None:
            corrected_artist = corrected_values.split(self.SEPARATOR)[0]
            corrected_song = corrected_values.split(self.SEPARATOR)[1]

            song_found = func_find_song(corrected_artist, corrected_song)

            if song_found:
                return song_found

        for corrector in self._correctors:

            corrected_values = corrector.correct(artist, song)

            if corrected_values is not None:
                corrected_artist = corrected_values["artist"]
                corrected_song = corrected_values["song"]

                song_found = func_find_song(corrected_artist, corrected_song)
                if song_found:
                    self._cache_correction(
                        artist, song, corrected_artist, corrected_song
                    )
                    return song_found
