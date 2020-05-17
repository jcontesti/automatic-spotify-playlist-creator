import importlib
from datetime import datetime
import logging
from dateutil.relativedelta import relativedelta

from spotify_classes.spotify_album import SpotifyAlbum
from spotify_classes.spotify_track import SpotifyTrack


class ScrappedPlaylist:
    def __init__(
        self,
        spotify_playlist,
        spotify_session,
        spotify_username,
        spotify_country,
        scrapped_tracks,
        spotify_ignored_tracks,
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
        self._scrapped_tracks = scrapped_tracks
        self._spotify_ignored_tracks = spotify_ignored_tracks
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
        self._callable_correctors = []

        if self._misspelling_correctors:
            for misspelling_corrector in self._misspelling_correctors:
                misspelling_corrector_module = list(misspelling_corrector.keys())[0]
                misspelling_corrector_class = misspelling_corrector.get(
                    misspelling_corrector_module
                )

                corrector_module = importlib.import_module(misspelling_corrector_module)

                corrector = getattr(corrector_module, misspelling_corrector_class)

                self._callable_correctors.append(corrector())

    def _format_scrapped_song(self, scrapped_song):
        # One scrapped song can include many artists and song titles, but one album

        artist = scrapped_song.artist.lower()
        song_title = scrapped_song.title.lower()
        album_title = scrapped_song.album.lower()

        # Split artists names into a list
        for split in self._artists_split:
            artist = artist.replace(split, "#")

        if "#" in artist:
            artists_names = artist.split("#")
        else:
            artists_names = [artist]

        # Split songs titles into a list
        for split in self._songs_titles_split:
            song_title = song_title.replace(split, "#")

        if "#" in song_title:
            songs_titles = song_title.split("#")
        else:
            songs_titles = [song_title]

        artists_names = [artist_name.strip(" \t\n\r") for artist_name in artists_names]
        songs_titles = [song_title.strip(" \t\n\r") for song_title in songs_titles]
        album_title = (
            album_title.strip(" \t\n\r") if album_title is not None else album_title
        )

        # Correct artists names using the correspondences found in the variable
        # _artists_transformations
        artists_names_transformed = []
        for artist_name in artists_names:
            if self._artists_transformations and self._artists_transformations[0].get(
                artist_name
            ):
                artists_names_transformed.append(
                    self._artists_transformations[0].get(artist_name)
                )
            else:
                artists_names_transformed.append(artist_name)

        return {
            "artists_names": artists_names_transformed,
            "songs_titles": songs_titles,
            "album": album_title,
        }

    def _format_scrapped_tracks(self):
        self._formatted_songs = []
        for scrapped_song in self._scrapped_tracks:
            formatted_song = self._format_scrapped_song(scrapped_song)
            self._formatted_songs.append(formatted_song)

    @staticmethod
    def _extract_released_date(track):
        release_date = track.album.release_date
        release_date_precision = track.album.release_date_precision
        release_date_formatted = datetime.today()

        if release_date_precision == "year":
            release_date_formatted = datetime.strptime(release_date, "%Y")
        if release_date_precision == "month":
            release_date_formatted = datetime.strptime(release_date, "%Y-%m")
        if release_date_precision == "day":
            release_date_formatted = datetime.strptime(release_date, "%Y-%m-%d")

        return release_date_formatted

    def _is_released_in_last_year(self, track):
        return self._extract_released_date(track) > datetime.now() - relativedelta(
            years=1
        )

    def _get_albums_songs(self, artist_name, album):
        q = self._get_artist_album_query(artist_name, album)

        logging.info("Querying album: " + q)

        album = SpotifyAlbum(self._spotify_session.search(q=q, type="album", limit=1))

        if not album.is_empty():
            artist = album.main_artist

            album_tracks_ids = album.tracks_ids(self._spotify_session)

            artist_top_tracks_ids = []
            if self._get_only_most_played_songs_from_albums:
                # We will try to collect the most interesting tracks
                # of the album. Spotify doesn't allow to know the
                # number of plays per album, but we'll use
                # a work-around: if any track is included in the most
                # played tracks of the artist, we'll add it
                # to the playlist
                artist_top_tracks_ids = artist.top_tracks_ids(
                    self._spotify_session, self._spotify_country
                )

            for album_track_id in album_tracks_ids:
                if (
                    self._get_only_most_played_songs_from_albums
                    and album_track_id in artist_top_tracks_ids
                ) or not self._get_only_most_played_songs_from_albums:
                    if (
                        self._spotify_ignored_tracks
                        and album_track_id not in self._spotify_ignored_tracks
                    ) or self._spotify_ignored_tracks is None:
                        logging.info(
                            "Adding " + q + " " + album_track_id + " to tracks to load"
                        )
                        self._tracks_to_load.add(album_track_id)

    @staticmethod
    def _get_artist_album_query(artist, album):
        return 'artist:"' + artist + '" album:"' + album + '"'

    @staticmethod
    def _get_artist_track_query(artist, song):
        return 'artist:"' + artist + '" track:"' + song + '"'

    def _find_song(self, artist, song):
        q = self._get_artist_track_query(artist, song)

        logging.info("Querying track: " + q)

        track = SpotifyTrack(self._spotify_session.search(q=q, type="track", limit=1))

        return None if track.is_empty() else track

    def _get_song(self, artist, song):
        track = self._find_song(artist, song)

        # If not found, try with a corrected misspelling version
        if not track:
            for corrector in self._callable_correctors:
                corrected_values = corrector.correct(artist, song)

                if corrected_values is not None:
                    corrected_artist = corrected_values["artist"]
                    corrected_song = corrected_values["song"]

                    track = self._find_song(corrected_artist, corrected_song)
                    if track:
                        break

        if track:
            if self._check_released_last_year:
                if not self._is_released_in_last_year(track):
                    return

            if (
                self._spotify_ignored_tracks
                and track.id not in self._spotify_ignored_tracks
            ) or self._spotify_ignored_tracks is None:

                logging.info("Adding " + track.id + " to tracks to load")
                self._tracks_to_load.add(track.id)

    def _get_new_tracks_to_load(self):
        self._tracks_to_load = set()

        # save result to to self._formatted_songs
        self._format_scrapped_tracks()

        for formatted_song in self._formatted_songs:

            artists_names = formatted_song.get("artists_names")
            songs_titles = formatted_song.get("songs_titles")
            album = formatted_song.get("album")

            for artist_name in artists_names:
                for song_title in songs_titles:
                    if song_title:
                        self._get_song(artist_name, song_title)

                if album and self._get_full_albums:
                    # Get songs from the artist and album
                    self._get_albums_songs(artist_name, album)

    def _get_playlist_current_tracks(self):
        results = self._spotify_session.user_playlist_tracks(
            self._spotify_username, playlist_id=self._spotify_playlist
        )
        tracks = results["items"]
        while results["next"]:  # to get more than 100 tracks
            results = self._spotify_session.next(results)
            tracks.extend(results["items"])

        return [t["track"]["id"] for t in tracks]

    def _remove_deleted_tracks(self, playlist_current_tracks):
        for current_track in playlist_current_tracks:
            if current_track not in self._tracks_to_load:
                # Remove the track
                self._spotify_session.user_playlist_remove_all_occurrences_of_tracks(
                    self._spotify_username,
                    playlist_id=self._spotify_playlist,
                    tracks=[current_track],
                )

    def _add_new_tracks(self, playlist_current_tracks):

        # Spotipy API doesn't allow to load more than 100 tracks per call
        SPLIT_MAX = 100

        final_tracks_to_append = []
        for track_to_load in self._tracks_to_load:
            if track_to_load not in playlist_current_tracks:  # to avoid duplicates
                final_tracks_to_append.append(track_to_load)

        if final_tracks_to_append:
            # Add all the tracks in one call in chunks of SPLIT_MAX
            for i in range(0, len(final_tracks_to_append), SPLIT_MAX):
                self._spotify_session.user_playlist_add_tracks(
                    self._spotify_username,
                    playlist_id=self._spotify_playlist,
                    tracks=final_tracks_to_append[i : i + SPLIT_MAX],
                )

    def update_playlist(self):
        self._get_new_tracks_to_load()

        playlist_current_tracks = self._get_playlist_current_tracks()

        # Remove all current tracks that have gone out of the playlist
        self._remove_deleted_tracks(playlist_current_tracks)

        # Add all the new tracks that weren't on the playlist
        self._add_new_tracks(playlist_current_tracks)
