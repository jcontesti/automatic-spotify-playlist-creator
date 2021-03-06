"""
Base class to implement misspelling corrections.

This class should be extended and never instantiated.
"""
from pathlib import Path
import json
from abc import ABC, abstractmethod
from typing import Dict, Final, List, Optional


class MisspellingCorrector(ABC):
    """
    Class that implements the cache system for the spelling corrections, to avoid
    asking for the same correction in the future.

    The method 'correct' must be implemented in a new class that extends this one.
    """

    CACHE_SEPARATOR: Final[str] = "@@@"

    def __init__(
        self,
        cache_path: str,
    ) -> None:
        self._cache_path: str = cache_path
        self._load_cached_misspelling_corrections()

    def _load_cached_misspelling_corrections(self) -> None:
        self._misspelling_corrections: Dict[str, str] = {}

        if Path(self._cache_path).exists():
            with open(self._cache_path, "r") as file:
                self._misspelling_corrections = json.loads(file.read())

    def _update_cached_misspelling_corrections(self) -> None:
        with open(self._cache_path, "w") as file:
            file.write(json.dumps(self._misspelling_corrections))

    def _encode_artist_song(self, artist: str, song: str) -> str:
        return artist + self.CACHE_SEPARATOR + song

    def _decode_artist_song(self, artist_song: str) -> Dict[str, str]:
        split: List[str] = artist_song.split(self.CACHE_SEPARATOR)
        return {"artist": split[0], "song": split[1]}

    def _cache_correction(self,
                          artist: str,
                          song: str,
                          corrected_artist: str,
                          corrected_song: str) -> None:
        key: str = self._encode_artist_song(artist, song)
        value: str = self._encode_artist_song(corrected_artist, corrected_song)
        self._misspelling_corrections[key] = value
        self._update_cached_misspelling_corrections()

    def _get_from_cached_misspelling_corrections(
            self,
            artist: str,
            song: str
    ) -> Optional[str]:
        key: str = self._encode_artist_song(artist, song)
        return (
            self._misspelling_corrections[key]
            if key in self._misspelling_corrections
            else None
        )

    @abstractmethod
    def correct(self, artist: str, song: str) -> Optional[Dict[str, str]]:
        """Return artist and song without spelling errors."""
