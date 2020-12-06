"""Class that represents a session in Spotify."""
from typing import Any, Dict, Optional, Set

import spotipy
import spotipy.util as util

from settings import Settings
from correctors.google_misspelling_corrector import GoogleMisspellingCorrector
from correctors.misspelling_corrector import MisspellingCorrector
from extracted_data.extracted_playlist import ExtractedPlaylist
from extracted_data.extracted_song import ExtractedSong
from . import spotify_playlist
from . import spotify_song
from .spotify_album import SpotifyAlbum


class SpotifySession:
    """Class that represents a session in Spotify."""

    def __init__(
            self,
            settings: Settings,
            # pylint: disable=unsubscriptable-object
            misspelling_corrector: Optional[str] = None,
    ) -> None:
        self._username: str = settings.SPOTIFY_USERNAME
        self._token: Any = util.prompt_for_user_token(
            username=settings.SPOTIFY_USERNAME,
            scope=settings.SPOTIFY_SCOPE,
            client_id=settings.SPOTIPY_CLIENT_ID,
            client_secret=settings.SPOTIPY_CLIENT_SECRET,
            redirect_uri=settings.SPOTIPY_REDIRECT_URI,
        )
        self._session: spotipy.Spotify = spotipy.Spotify(auth=self._token)

        self._misspelling_corrector: Optional[MisspellingCorrector] = None
        if misspelling_corrector == 'Google':
            self._misspelling_corrector = (
                GoogleMisspellingCorrector()
            )

    def _find_song(
            self,
            artist: str,
            song_title: str
    ) -> Optional[spotify_song.SpotifySong]:  # pylint: disable=unsubscriptable-object
        query: str = 'artist:"' + artist + '" track:"' + song_title + '"'

        search_result: Dict[str, Any] = self._session.search(
            q=query,
            type="track",
            limit=1
        )

        # pylint: disable=unsubscriptable-object
        song: Optional[spotify_song.SpotifySong] = None

        if search_result["tracks"]["total"] > 0:
            song = spotify_song.SpotifySong(self._session,
                                            search_result["tracks"]["items"][0]["id"])

        return song

    def _get_song(
            self,
            extracted_song: ExtractedSong,
            only_load_songs_released_in_last_year: bool = False,
    ) -> Optional[spotify_song.SpotifySong]:  # pylint: disable=unsubscriptable-object

        artist: str = extracted_song.artist
        song_title: str = extracted_song.song_title

        # pylint: disable=unsubscriptable-object
        song: Optional[spotify_song.SpotifySong] = self._find_song(artist, song_title)

        # If not found, try with a corrected version
        if not song:
            if self._misspelling_corrector:
                corrected_values = self._misspelling_corrector.correct(artist,
                                                                       song_title)

                if corrected_values is not None:
                    corrected_artist = corrected_values["artist"]
                    corrected_song = corrected_values["song"]

                    song = self._find_song(corrected_artist, corrected_song)

        if song:
            if only_load_songs_released_in_last_year and (
                    not song.is_released_in_last_year()
            ):
                return None

        return song

    def _find_album(
            self,
            artist: str,
            album_title: str,
    ) -> Optional[SpotifyAlbum]:  # pylint: disable=unsubscriptable-object

        query: str = 'artist:"' + artist + '" album:"' + album_title + '"'

        search_result: Dict[str, Any] = self._session.search(
            q=query,
            type="album",
            limit=1
        )

        # pylint: disable=unsubscriptable-object
        album: Optional[SpotifyAlbum] = None

        if search_result["albums"]["total"] > 0:
            album = SpotifyAlbum(self._session,
                                search_result["albums"]["items"][0]["id"])

        return album

    def _get_all_songs_from_album(
            self,
            extracted_song: ExtractedSong,
            only_load_songs_released_in_last_year: bool = False,
    ) -> Set[spotify_song.SpotifySong]:
        artist = extracted_song.artist
        album_title = extracted_song.album_title

        songs_in_spotify_album: Set[spotify_song.SpotifySong] = set()

        if album_title:
            spotify_album = self._find_album(artist, album_title)

            if spotify_album:
                if (only_load_songs_released_in_last_year and
                        not spotify_album.is_released_in_last_year()):
                    return set()

                album_songs_ids = spotify_album.songs_ids()

                for album_song_id in album_songs_ids:
                    songs_in_spotify_album.add(
                        spotify_song.SpotifySong(self._session, album_song_id)
                    )

        return songs_in_spotify_album

    def replace_spotify_playlist_from_extracted_playlist(
            self,
            spotify_playlist_destination: str,
            extracted_playlist: ExtractedPlaylist,
            only_load_songs_released_in_last_year: bool = False,
            load_all_songs_from_albums: bool = False
    ) -> None:
        """Replace a Spotify playlist with the new extracted songs."""
        playlist = spotify_playlist.SpotifyPlaylist(
            spotify_playlist_destination,
            self._session,
            self._username,
        )

        songs_to_load: Set[spotify_song.SpotifySong] = set()

        for extracted_song in extracted_playlist.get_songs():

            # Load song from Spotify
            # pylint: disable=unsubscriptable-object
            song: Optional[spotify_song.SpotifySong] = self._get_song(
                extracted_song,
                only_load_songs_released_in_last_year
            )

            if song:
                songs_to_load.add(song)

            if load_all_songs_from_albums:
                spotify_album_songs: Set[spotify_song.SpotifySong] = (
                    self._get_all_songs_from_album(
                        extracted_song,
                        only_load_songs_released_in_last_year
                    )
                )

                songs_to_load = songs_to_load.union(spotify_album_songs)

        # Add extracted songs to Spotify playlist
        playlist.update(songs_to_load)
