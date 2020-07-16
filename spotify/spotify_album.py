import spotipy

from spotify.spotify_artist import SpotifyArtist
from spotify.spotify_song import SpotifySong
from datetime import datetime
from dateutil.relativedelta import relativedelta


class SpotifyAlbum:
    def __init__(self, album: [str]):
        self._album = album

    @property
    def id(self) -> str:
        return self._album["albums"]["items"][0]["id"]

    @property
    def main_artist(self) -> SpotifyArtist:
        return SpotifyArtist(
            self._album["albums"]["items"][0]["artists"][0]
        )

    def _release_date(self) -> str:
        return self._album["release_date"]

    def _release_date_precision(self) -> str:
        return self._album["release_date_precision"]

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

    def songs(self, sp: spotipy.Spotify) -> [SpotifySong]:
        return [SpotifySong(song) for song in sp.album_tracks(self.id)["items"]]

    def is_empty(self) -> bool:
        return not self._album["albums"]["items"]
