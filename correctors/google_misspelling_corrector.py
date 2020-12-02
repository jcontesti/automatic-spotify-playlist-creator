from googleapiclient.discovery import build
from . import misspelling_corrector
from typing import Dict, Optional
import settings


class GoogleMisspellingCorrector(misspelling_corrector.MisspellingCorrector):
    GOOGLE_API_KEY = settings.GOOGLE_API_KEY
    GOOGLE_CSE_KEY = settings.GOOGLE_CSE_KEY
    SEPARATOR = " : "

    def __init__(self, cache_path: str = "google_misspelling_corrections_cache.json"):
        super(GoogleMisspellingCorrector, self).__init__(cache_path)

    def correct(self, artist: str, song: str) -> Optional[Dict[str, str]]:

        # If previously queried, return from cache
        cached_corrected = self._get_from_cached_misspelling_corrections(artist, song)
        if cached_corrected:
            return self._decode_artist_song(cached_corrected)

        service = build(
            "customsearch",
            "v1",
            developerKey=self.GOOGLE_API_KEY,
            cache_discovery=False,
        )

        query = artist + self.SEPARATOR + song

        result = service.cse().list(q=query, cx=self.GOOGLE_CSE_KEY).execute()

        if "spelling" in result:
            corrected = result["spelling"]["correctedQuery"].split(self.SEPARATOR)

            corrected_artist = corrected[0]
            corrected_song = corrected[1] if len(corrected) == 2 else ""

            # Cache queried values
            self._cache_correction(artist, song, corrected_artist, corrected_song)

            return {"artist": corrected_artist, "song": corrected_song}
        else:
            return None
