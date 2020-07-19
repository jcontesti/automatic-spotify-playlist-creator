import spotipy

from datetime import datetime
from dateutil.relativedelta import relativedelta


class SpotifyAlbum:
    def __init__(self, session: spotipy.Spotify, album_id: str):

        source = session.album(album_id)
        self._id: str = source["id"]
        self._release_date: str = source["release_date"]
        self._release_date_precision: str = source["release_date_precision"]
        self._session = session

    @property
    def id(self) -> str:
        return self._id

    def _release_date(self) -> str:
        return self._release_date

    def _release_date_precision(self) -> str:
        return self._release_date_precision

    def _extract_released_date(self) -> datetime:
        release_date = self._release_date
        release_date_precision = self._release_date_precision
        release_date_formatted = datetime.today()

        if release_date_precision == "year":
            release_date_formatted = datetime.strptime(release_date, "%Y")
        if release_date_precision == "month":
            release_date_formatted = datetime.strptime(release_date, "%Y-%m")
        if release_date_precision == "day":
            release_date_formatted = datetime.strptime(release_date, "%Y-%m-%d")

        return release_date_formatted

    def is_released_in_last_year(self) -> bool:
        return self._extract_released_date() > datetime.now() - relativedelta(
            years=1
        )

    def songs_ids(self) -> [str]:
        return [song["id"] for song in self._session.album_tracks(self._id)["items"]]
