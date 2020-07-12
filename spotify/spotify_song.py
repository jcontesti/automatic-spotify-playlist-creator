from . import spotify_album
from datetime import datetime
from dateutil.relativedelta import relativedelta


class SpotifySong:
    def __init__(self, song: [str]):
        self._song = song

    @property
    def id(self) -> str:
        return self._song["tracks"]["items"][0]["id"]

    @property
    def album(self) -> spotify_album.SpotifyAlbum:
        return spotify_album.SpotifyAlbum(self._song["tracks"]["items"][0]["album"])

    def is_empty(self) -> bool:
        return not self._song["tracks"]["items"]

    def _extract_released_date(self):
        release_date = self._song.album.release_date
        release_date_precision = self._song.album.release_date_precision
        release_date_formatted = datetime.today()

        if release_date_precision == "year":
            release_date_formatted = datetime.strptime(release_date, "%Y")
        if release_date_precision == "month":
            release_date_formatted = datetime.strptime(release_date, "%Y-%m")
        if release_date_precision == "day":
            release_date_formatted = datetime.strptime(release_date, "%Y-%m-%d")

        return release_date_formatted

    def is_released_in_last_year(self):
        return self._extract_released_date() > datetime.now() - relativedelta(
            years=1
        )
