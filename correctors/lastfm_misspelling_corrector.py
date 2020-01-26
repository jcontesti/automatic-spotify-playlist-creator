import settings
import requests
from . import misspelling_corrector


class LastFMMisspellingCorrector(misspelling_corrector.MisspellingCorrector):
    LASTFM_API_KEY = settings.LASTFM_API_KEY

    def __init__(self, cache_path="lastfm_misspelling_corrections_cache.json"):
        super(LastFMMisspellingCorrector, self).__init__(cache_path)

    def correct(self, artist, song):

        # If previously queried, return from cache
        cached_corrected = self._get_from_cached_misspelling_corrections(artist, song)
        if cached_corrected:
            return self._decode_artist_song(cached_corrected)

        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "track.getcorrection",
            "artist": artist,
            "track": song,
            "api_key": self.LASTFM_API_KEY,
            "format": "json",
        }

        result = requests.get(url=url, params=params)

        data = result.json()

        if "corrections" in data:
            correction = data.get("corrections").get("correction")
            track = correction.get("track")

            if "name" in track:
                corrected_artist = track.get("artist").get("name")
                corrected_song = track.get("name")

                # Cache queried values
                self._cache_correction(artist, song, corrected_artist, corrected_song)

                return {"artist": corrected_artist, "song": corrected_song}

        return None
