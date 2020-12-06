"""Class that represents an album in Spotify."""
from datetime import datetime
from typing import Dict, List

import spotipy
from dateutil.relativedelta import relativedelta


class SpotifyAlbum:
    """Class that represents an album in Spotify."""

    def __init__(self, session: spotipy.Spotify, album_id: str) -> None:
        source: Dict[str, str] = session.album(album_id)

        self._id: str = source["id"]
        self._release_date: str = str(source["release_date"])
        self._release_date_precision: str = source["release_date_precision"]
        self._session = session

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
        """
        Check if the album was released in the last 365 days.

        :return: True if the album was released in the last year, False otherwise.
        """
        return self._extract_released_date() > datetime.now() - relativedelta(
            years=1
        )

    def songs_ids(self) -> List[str]:
        """
        Return Spotify ids of all the songs in the album.

        :return: List with ids of all the songs in the album.
        """
        return [song["id"] for song in self._session.album_tracks(self._id)["items"]]
