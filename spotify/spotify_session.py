import spotipy
import spotipy.util as util

import settings
from correctors.google_misspelling_corrector import GoogleMisspellingCorrector
from extracted_data.extracted_playlist import ExtractedPlaylist
from extracted_data.extracted_song import ExtractedSong
from .spotify_album import SpotifyAlbum
from . import spotify_song
from . import spotify_playlist


class SpotifySession:

    def __init__(
            self,
            username: [str] = settings.SPOTIFY_USERNAME,
            scope: [str] = settings.SPOTIFY_SCOPE,
            client_id: [str] = settings.SPOTIPY_CLIENT_ID,
            client_secret: [str] = settings.SPOTIPY_CLIENT_SECRET,
            redirect_uri: [str] = settings.SPOTIPY_REDIRECT_URI,
    ):
        self._username = username
        self._token = util.prompt_for_user_token(
            username=username,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
        )
        self._session = spotipy.Spotify(auth=self._token)
        self._misspelling_corrector = GoogleMisspellingCorrector()

    def _find_song(
            self,
            artist: str,
            song_title: str
    ) -> spotify_song.SpotifySong:
        q: str = 'artist:"' + artist + '" track:"' + song_title + '"'

        song = spotify_song.SpotifySong(self._session.search(q=q, type="track", limit=1))

        return None if song.is_empty() else song

    def _get_song(
            self,
            extracted_song: ExtractedSong,
            only_load_songs_released_in_last_year: bool = False,
    ) -> spotify_song.SpotifySong:

        artist = extracted_song.artist
        song_title = extracted_song.song_title

        song = self._find_song(artist, song_title)

        # If not found, try with a corrected version
        if not song:
            if self._misspelling_corrector:
                corrected_values = self._misspelling_corrector.correct(artist, song_title)

                if corrected_values is not None:
                    corrected_artist = corrected_values["artist"]
                    corrected_song = corrected_values["song"]

                    song = self._find_song(corrected_artist, corrected_song)

        if song:
            if only_load_songs_released_in_last_year and not song.is_released_in_last_year():
                return None

        return song

    def _find_album(
            self,
            artist: str,
            album_title: str,
    ) -> SpotifyAlbum:

        q: str = 'artist:"' + artist + '" album:"' + album_title + '"'

        return SpotifyAlbum(self._session.search(q=q, type="album", limit=1))

    def _get_all_songs_from_album(
            self,
            extracted_song: ExtractedSong,
            only_load_songs_released_in_last_year: bool = False,
    ) -> [spotify_song.SpotifySong]:
        artist = extracted_song.artist
        album_title = extracted_song.album_title

        spotify_album = self._find_album(artist, album_title)

        songs_in_spotify_album: [spotify_song.SpotifySong] = []

        if not spotify_album.is_empty():
            if only_load_songs_released_in_last_year and not spotify_album.is_released_in_last_year():
                return None

            album_songs = spotify_album.songs_ids(self._session)
            
            for album_song in album_songs:
                songs_in_spotify_album.append(album_song)

        return songs_in_spotify_album

    def replace_spotify_playlist_from_extracted_playlist(
            self,
            spotify_playlist_destination: str,
            extracted_playlist: ExtractedPlaylist,
            only_load_songs_released_in_last_year: bool = False,
            load_all_songs_from_albums: bool = False
    ):
        playlist = spotify_playlist.SpotifyPlaylist(
            spotify_playlist_destination,
            self._session,
            self._username,
        )

        songs_to_load: [spotify_song.SpotifySong] = []

        for extracted_song in extracted_playlist.get_songs():
            # Get song in Spotify
            spotify_song = self._get_song(extracted_song, only_load_songs_released_in_last_year)

            songs_to_load.append(spotify_song)

            if load_all_songs_from_albums:
                spotify_album_songs = self._get_all_songs_from_album(
                    extracted_song,
                    only_load_songs_released_in_last_year
                )

                songs_to_load = songs_to_load + spotify_album_songs

        # Add extracted songs to Spotify playlist
        playlist.update(songs_to_load)
