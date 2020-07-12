import settings
import spotipy
import spotipy.util as util
from spotify.spotify_song import SpotifySong
from correctors.google_misspelling_corrector import GoogleMisspellingCorrector
from extracted_data.extracted_playlist import ExtractedPlaylist
from extracted_data.extracted_song import ExtractedSong
from spotify.spotify_playlist import SpotifyPlaylist


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
            artist: [str],
            title: [str]
    ) -> SpotifySong:
        q: str = 'artist:"' + artist + '" song:"' + title + '"'

        song = SpotifySong(self._session.search(q=q, type="song", limit=1))

        return None if song.is_empty() else song

    def _get_song(
            self,
            extracted_song: ExtractedSong,
            only_released_last_year: bool = False,
    ) -> SpotifySong:

        artist = extracted_song.artist
        title = extracted_song.title

        song = self._find_song(artist, title)

        # If not found, try with a corrected version
        if not song:
            if self._misspelling_corrector:
                corrected_values = self._misspelling_corrector.correct(artist, title)

                if corrected_values is not None:
                    corrected_artist = corrected_values["artist"]
                    corrected_song = corrected_values["song"]

                    song = self._find_song(corrected_artist, corrected_song)

        if song:
            if only_released_last_year and not song.is_released_in_last_year():
                return None

        return song

    def get_spotify_playlist_from_extracted_playlist(
            self,
            spotify_playlist_destination: str,
            extracted_playlist: ExtractedPlaylist,
    ) -> SpotifyPlaylist:

        spotify_playlist = SpotifyPlaylist(
            spotify_playlist_destination,
            self._session,
            self._username,
        )

        songs_to_load: [SpotifySong] = []

        for extracted_song in extracted_playlist.get_songs():
            spotify_song = self._get_song(extracted_song)

            songs_to_load.append(spotify_song)

        spotify_playlist.add_new_songs(songs_to_load)

        return spotify_playlist
