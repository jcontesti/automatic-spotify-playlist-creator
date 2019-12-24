import importlib
from datetime import datetime

from dateutil.relativedelta import relativedelta

from spotify_classes.spotify_album import SpotifyAlbum
from spotify_classes.spotify_track import SpotifyTrack


class ScrappedPlaylist:
    def __init__(self,
                 spotify_playlist,
                 spotify_session,
                 spotify_username,
                 spotify_country,
                 scrapped_tracks,
                 spotify_ignored_tracks,
                 artists_split,
                 songs_titles_split,
                 various_titles_in_one_tokens,
                 check_released_last_year,
                 misspelling_corrector_module,
                 misspelling_corrector_class,
                 artists_transformations):
        self._spotify_playlist = spotify_playlist
        self._spotify_session = spotify_session
        self._spotify_username = spotify_username
        self._spotify_country = spotify_country
        self._scrapped_tracks = scrapped_tracks
        self._spotify_ignored_tracks = spotify_ignored_tracks
        self._artists_split = artists_split
        self._songs_titles_split = songs_titles_split
        self._various_titles_in_one_tokens = various_titles_in_one_tokens
        self._check_released_last_year = check_released_last_year
        self._artists_transformations = artists_transformations

        corrector_module = importlib.import_module(
            misspelling_corrector_module
        )

        self._corrector = getattr(
            corrector_module,
            misspelling_corrector_class
        )

    def _format_scrapped_song(self, scrapped_song):
        # One scrapped song can include many artists and song titles

        artist = scrapped_song.artist
        song_title = scrapped_song.title
        album_title = scrapped_song.album

        for split in self._artists_split:
            artist = artist.replace(split, '#')

        if '#' in artist:
            artists_names = artist.split('#')
        else:
            artists_names = [artist]

        for split in self._songs_titles_split:
            song_title = song_title.replace(split, '#')

        if '#' in song_title:
            songs_titles = song_title.split('#')
        else:
            songs_titles = [song_title]

        artists_names = [artist_name.strip(' \t\n\r').lower()
                         for artist_name in artists_names]
        songs_titles = [song_title.strip(' \t\n\r').lower()
                        for song_title in songs_titles]
        album_title = album_title.strip(' \t\n\r').lower() \
            if album_title is not None else album_title

        artists_names_transformed = []
        for artist_name in artists_names:
            if self._artists_transformations[0].get(artist_name) is None:
                artists_names_transformed.append(artist_name)
            else:
                artists_names_transformed.append(
                    self._artists_transformations[0].get(artist_name)
                )

        return {'artists_names': artists_names_transformed,
                'songs_titles': songs_titles,
                'album': album_title}

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

        if release_date_precision == 'year':
            release_date_formatted = datetime.strptime(release_date, '%Y')
        if release_date_precision == 'month':
            release_date_formatted = datetime.strptime(release_date, '%Y-%m')
        if release_date_precision == 'day':
            release_date_formatted = datetime.strptime(
                release_date, '%Y-%m-%d'
            )

        return release_date_formatted

    def _is_released_in_last_year(self, track):
        return self._extract_released_date(track) > datetime.now() - \
               relativedelta(years=1)

    def _get_most_interesting_songs_of_album(
            self,
            artist_name,
            album
    ):
        # We will try to collect the most interesting tracks
        # of the album. Spotify doesn't allow to know the
        # number of plays per album, but we'll use
        # a work-around: if any track is included in the most
        # played tracks of the artist, we'll add it
        # to the playlist

        q = 'artist:"' + artist_name + \
            '" album:"' + album + '"'

        print(q)

        album = SpotifyAlbum(
            self._spotify_session.search(q=q,
                                         type='album',
                                         limit=1)
        )

        if not album.is_empty():
            artist = album.main_artist

            album_tracks_ids = album.tracks_ids(
                self._spotify_session
            )
            artist_top_tracks_ids = artist.top_tracks_ids(
                self._spotify_session,
                self._spotify_country
            )

            for album_track_id in album_tracks_ids:
                if album_track_id in artist_top_tracks_ids:
                    if album_track_id not in self._spotify_ignored_tracks:
                        self._tracks_to_load.add(album_track_id)

    @staticmethod
    def _get_artist_track_query(artist_name, song_name):
        return 'artist:"' + artist_name + '" track:"' + song_name + '"'

    def _get_song(
            self,
            artist_name,
            song_name
    ):
        q = self._get_artist_track_query(artist_name, song_name)

        print(q)

        track = SpotifyTrack(
            self._spotify_session.search(
                q=q,
                type='track',
                limit=1
            )
        )

        # If not found, try with a corrected misspelling version
        if track.is_empty() and self._corrector:

            corrected_values = self._corrector.correct(
                artist_name,
                song_name
            )
            if corrected_values is not None:
                q = self._get_artist_track_query(
                    corrected_values['artist'],
                    corrected_values['song']
                )

                print("(corrected) " + q)

                track = SpotifyTrack(
                    self._spotify_session.search(
                        q=q,
                        type='track',
                        limit=1
                    )
                )

        if not track.is_empty():
            if self._check_released_last_year:
                released_last_year = self._is_released_in_last_year(track)
                if not released_last_year:
                    return

            if track.id not in self._spotify_ignored_tracks:
                self._tracks_to_load.add(track.id)

    def _get_current_tracks_to_load(self):
        self._tracks_to_load = set()

        self._format_scrapped_tracks()

        for formatted_song in self._formatted_songs:

            artists_names = formatted_song.get('artists_names')
            songs_titles = formatted_song.get('songs_titles')
            album = formatted_song.get('album')

            for artist_name in artists_names:

                for song_title in songs_titles:

                    if song_title in self._various_titles_in_one_tokens \
                            and album:

                        self._get_most_interesting_songs_of_album(
                            artist_name,
                            album
                        )

                    else:

                        self._get_song(artist_name, song_title)

    def _get_playlist_current_tracks(self):
        results = self._spotify_session.user_playlist_tracks(
            self._spotify_username,
            playlist_id=self._spotify_playlist
        )
        tracks = results['items']
        while results['next']:  # to get more than 100 tracks
            results = self._spotify_session.next(results)
            tracks.extend(results['items'])

        return [t['track']['id'] for t in tracks]

    def _remove_deleted_tracks(self, current_tracks):
        for current_track in current_tracks:
            if current_track not in self._tracks_to_load:
                # Remove the track
                self._spotify_session\
                    .user_playlist_remove_all_occurrences_of_tracks(
                        self._spotify_username,
                        playlist_id=self._spotify_playlist,
                        tracks=[current_track],
                    )

    def _add_new_tracks(self, current_tracks):

        # Spotipy API doesn't allow to load more than 100 tracks per call
        SPLIT_MAX = 100

        final_tracks_to_append = []
        for track_to_load in self._tracks_to_load:
            if track_to_load not in current_tracks: # to avoid duplicates
                final_tracks_to_append.append(track_to_load)

        if final_tracks_to_append:
            # Add all the tracks in one call in chunks of SPLIT_MAX
            for i in range(0, len(final_tracks_to_append), SPLIT_MAX):
                self._spotify_session.user_playlist_add_tracks(
                    self._spotify_username,
                    playlist_id=self._spotify_playlist,
                    tracks=final_tracks_to_append[i:i + SPLIT_MAX],
                )

    def update_playlist(self):
        self._get_current_tracks_to_load()

        current_tracks = self._get_playlist_current_tracks()

        # Remove all current tracks that have gone out of the chart
        self._remove_deleted_tracks(current_tracks)

        # Add all the new tracks that weren't on the playlist
        self._add_new_tracks(current_tracks)
