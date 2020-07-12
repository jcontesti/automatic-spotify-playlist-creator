import spotipy

from . import spotify_artist


class SpotifyAlbum:
    def __init__(self, album: [str]):
        self._album = album

    @property
    def id(self) -> str:
        return self._album["albums"]["items"][0]["id"]

    @property
    def main_artist(self) -> spotify_artist.SpotifyArtist:
        return spotify_artist.SpotifyArtist(
            self._album["albums"]["items"][0]["artists"][0]
        )

    @property
    def release_date(self) -> str:
        return self._album["release_date"]

    @property
    def release_date_precision(self) -> str:
        return self._album["release_date_precision"]

    def songs(self, sp: spotipy.Spotify) -> [str]:
        return [t["id"] for t in sp.album_tracks(self.id)["items"]]

    def is_empty(self) -> bool:
        return not self._album["albums"]["items"]
