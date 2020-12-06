"""Class that represents a Spotify playlist."""
from typing import List, Set

import spotipy

from . import spotify_song


class SpotifyPlaylist:
    """Class that represents a Spotify playlist."""

    # Spotipy API doesn't allow to load more than 100 songs per call
    SPLIT_MAX = 100

    def __init__(
            self,
            playlist_id: str,
            session: spotipy.Spotify,
            username: str,
    ):
        self._playlist_id = playlist_id
        self._session = session
        self._username = username

    def _get_current_songs(self) -> List[spotify_song.SpotifySong]:
        results = self._session.user_playlist_tracks(
            self._username,
            playlist_id=self._playlist_id
        )

        songs = results["items"]
        while results["next"]:  # to get more than 100 songs
            results = self._session.next(results)
            songs.extend(results["items"])

        return [spotify_song.SpotifySong(self._session, song["track"]["id"]) for song in songs]

    def _remove_current_songs_not_in_songs_to_load(
            self,
            songs_to_load: Set[spotify_song.SpotifySong],
    ) -> None:
        playlist_current_songs = self._get_current_songs()

        for current_song in playlist_current_songs:
            if current_song not in songs_to_load:
                # Remove the song
                self._session.user_playlist_remove_all_occurrences_of_tracks(
                    self._username,
                    playlist_id=self._playlist_id,
                    tracks=[current_song.song_id],
                )

    def update(
            self,
            songs_to_load: Set[spotify_song.SpotifySong],
    ) -> None:
        """
        Update the Spotify playlist with the songs in the parameter.

        :param songs_to_load: Set of Spotify songs ids to replace the current ones in
        the playlist.
        """
        self._remove_current_songs_not_in_songs_to_load(songs_to_load)

        playlist_current_songs = self._get_current_songs()

        final_songs_to_load: List[spotify_song.SpotifySong] = []

        for song_to_load in songs_to_load:
            if song_to_load not in playlist_current_songs:  # to avoid duplicates
                final_songs_to_load.append(song_to_load)

        if final_songs_to_load:
            # Add all the songs in one call in chunks of SPLIT_MAX
            for i in range(0, len(final_songs_to_load), self.SPLIT_MAX):
                self._session.user_playlist_add_tracks(
                    self._username,
                    playlist_id=self._playlist_id,
                    tracks=[song.song_id for song in final_songs_to_load[i: i + self.SPLIT_MAX]],
                )
