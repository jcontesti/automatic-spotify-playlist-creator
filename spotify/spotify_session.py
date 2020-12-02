from typing import Set, Optional

import spotipy
import spotipy.util as util

import settings
from correctors.google_misspelling_corrector import GoogleMisspellingCorrector
from extracted_data.extracted_playlist import ExtractedPlaylist
from extracted_data.extracted_song import ExtractedSong
from . import spotify_playlist
from . import spotify_song
from .spotify_album import SpotifyAlbum
from typing import Any, Dict
from correctors.misspelling_corrector import MisspellingCorrector

class SpotifySession:

    def __init__(
            self,
            username: Optional[str] = settings.SPOTIFY_USERNAME,
            scope: Optional[str] = settings.SPOTIFY_SCOPE,
            client_id: Optional[str] = settings.SPOTIPY_CLIENT_ID,
            client_secret: Optional[str] = settings.SPOTIPY_CLIENT_SECRET,
            redirect_uri: Optional[str] = settings.SPOTIPY_REDIRECT_URI,
            misspelling_corrector: Optional[str] = None,
    ) -> None:
        self._username: str = username or ""
        self._token: Any = util.prompt_for_user_token(
            username=username,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
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
    ) -> Optional[spotify_song.SpotifySong]:
        q: str = 'artist:"' + artist + '" track:"' + song_title + '"'

        search_result: Dict[str, Any] = self._session.search(q=q, type="track", limit=1)

        if search_result["tracks"]["total"] > 0:
            return spotify_song.SpotifySong(self._session,
                                            search_result["tracks"]["items"][0]["id"])
        else:
            return None

    def _get_song(
            self,
            extracted_song: ExtractedSong,
            only_load_songs_released_in_last_year: bool = False,
    ) -> Optional[spotify_song.SpotifySong]:

        artist: str = extracted_song.artist
        song_title: str = extracted_song.song_title

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
    ) -> Optional[SpotifyAlbum]:

        q: str = 'artist:"' + artist + '" album:"' + album_title + '"'

        search_result = self._session.search(q=q, type="album", limit=1)

        if search_result["albums"]["total"] > 0:
            return SpotifyAlbum(self._session,
                                search_result["albums"]["items"][0]["id"])
        else:
            return None

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
                if only_load_songs_released_in_last_year and not spotify_album.is_released_in_last_year():
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
        playlist = spotify_playlist.SpotifyPlaylist(
            spotify_playlist_destination,
            self._session,
            self._username,
        )

        songs_to_load: Set[spotify_song.SpotifySong] = set()

        for extracted_song in extracted_playlist.get_songs():

            # Load song from Spotify
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
