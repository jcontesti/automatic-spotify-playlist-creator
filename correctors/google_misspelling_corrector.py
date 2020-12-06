"""Interface to use Google Search Console as a spelling corrector."""
from typing import Dict, Final, Optional

from googleapiclient.discovery import build

from settings import Settings
from . import misspelling_corrector


class GoogleMisspellingCorrector(misspelling_corrector.MisspellingCorrector):
    """
    Class that allows to correct artists and songs titles using Google Search Console.
    """
    GOOGLE_API_KEY: Final[str] = Settings.GOOGLE_API_KEY
    GOOGLE_CSE_KEY: Final[str] = Settings.GOOGLE_CSE_KEY
    SEPARATOR: Final[str] = " : "

    def __init__(self, cache_path: str = "google_misspelling_corrections_cache.json"):
        super().__init__(cache_path)

    def correct(self, artist: str, song: str) -> Optional[Dict[str, str]]:

        # If previously queried, return from cache
        cached_corrected: Optional[str] = (
            self._get_from_cached_misspelling_corrections(artist, song)
        )
        if cached_corrected:
            return self._decode_artist_song(cached_corrected)

        # Not typed because it returns a generic Resource
        service = build(
            "customsearch",
            "v1",
            developerKey=self.GOOGLE_API_KEY,
            cache_discovery=False,
        )

        query: str = artist + self.SEPARATOR + song

        # Not typed because it returns a generic result
        query_result = (
            # pylint: disable=no-member
            service.cse().list(q=query, cx=self.GOOGLE_CSE_KEY).execute()
        )

        corrected_result: Optional[Dict[str, str]] = None

        if "spelling" in query_result:
            corrected: str = (
                query_result["spelling"]["correctedQuery"].split(self.SEPARATOR)
            )

            corrected_artist = corrected[0]
            corrected_song = corrected[1] if len(corrected) == 2 else ""

            # Cache queried values
            self._cache_correction(artist, song, corrected_artist, corrected_song)

            corrected_result = {"artist": corrected_artist, "song": corrected_song}

        return corrected_result
