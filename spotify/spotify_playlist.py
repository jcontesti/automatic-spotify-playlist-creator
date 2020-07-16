import spotipy
from . import spotify_song


class SpotifyPlaylist:

    # Spotipy API doesn't allow to load more than 100 songs per call
    SPLIT_MAX = 100

    def __init__(
            self,
            id: str,
            session: spotipy.Spotify,
            username: str,
    ):
        self._id = id
        self._session = session
        self._username = username

    def _get_current_songs(self) -> [spotify_song.SpotifySong]:
        results = self._session.user_playlist_tracks(
            self._username,
            playlist_id=self._id
        )
        songs = results["items"]
        while results["next"]:  # to get more than 100 songs
            results = self._session.next(results)
            songs.extend(results["items"])

        return [spotify_song.SpotifySong(song) for song in songs]

    def _remove_current_songs_not_in_songs_to_load(
            self,
            songs_to_load: [str],
    ):
        playlist_current_songs = self._get_current_songs()

        for current_song in playlist_current_songs:
            if current_song not in songs_to_load:
                # Remove the song
                self._session.user_playlist_remove_all_occurrences_of_tracks(
                    self._username,
                    playlist_id=self._id,
                    tracks=[current_song],
                )

    def update(
            self,
            songs_to_load: [str],
    ):
        self._remove_current_songs_not_in_songs_to_load(songs_to_load)

        playlist_current_songs = self._get_current_songs()

        final_songs_to_append = []
        for song_to_load in songs_to_load:
            if song_to_load not in playlist_current_songs:  # to avoid duplicates
                final_songs_to_append.append(song_to_load)

        if final_songs_to_append:
            # Add all the songs in one call in chunks of SPLIT_MAX
            for i in range(0, len(final_songs_to_append), self.SPLIT_MAX):
                self._session.user_playlist_add_tracks(
                    self._username,
                    playlist_id=self._id,
                    tracks=final_songs_to_append[i: i + self.SPLIT_MAX],
                )
