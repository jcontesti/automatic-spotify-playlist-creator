import importlib
import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta

from spotify.spotify_album import SpotifyAlbum
from spotify.spotify_song import SpotifySong


class ExtractedPlaylistOld:
    def __init__(
        self,
        spotify_playlist,
        spotify_session,
        spotify_username,
        spotify_country,
        scrapped_songs,
        spotify_ignored_songs,
        artists_split,
        songs_titles_split,
        get_full_albums,
        get_only_most_played_songs_from_albums,
        check_released_last_year,
        artists_transformations,
        misspelling_correctors,
    ):
        self._spotify_playlist = spotify_playlist
        self._spotify_session = spotify_session
        self._spotify_username = spotify_username
        self._spotify_country = spotify_country
        self._scrapped_songs = scrapped_songs
        self._spotify_ignored_songs = spotify_ignored_songs
        self._artists_split = artists_split
        self._songs_titles_split = songs_titles_split
        self._get_only_most_played_songs_from_albums = (
            get_only_most_played_songs_from_albums
        )
        self._get_full_albums = get_full_albums
        self._check_released_last_year = check_released_last_year
        self._artists_transformations = artists_transformations
        self._misspelling_correctors = misspelling_correctors
        self._load_misspelling_correctors()

    def _load_misspelling_correctors(self):
        # moved to SpotifySession

    def _format_scrapped_song(self, scrapped_song):
        # moved to extracted_playlist()

    def _format_scrapped_songs(self):
        # moved to extracted_playlist()

    def _is_released_in_last_year(self, song):
        # moved to SpotifySong

    def _get_albums_songs(self, artist_name, album):
        # moved to spotify_session

    @staticmethod
    def _get_artist_album_query(artist, album):
        # moved to spotify_session

    @staticmethod
    def _get_artist_song_query(artist, song):
        # moved to spotify_sessions

    def _find_song(self, artist, song):
        # moved to spotify_session

    def _get_song(self, artist, song):
        # moved to spotify_session

    def _get_new_songs_to_load(self):
        # moved to spotify_session

    def _get_playlist_current_songs(self):
        # moved to spotify_sessions

    def _remove_deleted_songs(self, playlist_current_songs):
        # moved to spotify_sessions

    def _add_new_songs(self, playlist_current_songs):
        # moved to spotify_sessions

    def update_playlist(self):
        # moved to main function
