import json
from datetime import datetime

import spotipy
import spotipy.util as util
from dateutil.relativedelta import relativedelta

import settings
from album import Album
from playlist import Playlist
from track import Track

from misspelling_corrector import correct

# Manual transformations of misspellings
ARTISTS_NAMES_TRANSFORMATIONS = {
    '480 east': 'four80east',
    'agape soul': 'darryl anders agapesoul',
    'christian grey': 'christon gray',
    'india arie': 'india.arie',
    'vivian sessions': 'vivian sessoms',
}

# Tracks ids to ignore
# Useful when we are loading the wrong track but the algorithm can't avoid it
TRACKS_IDS_TO_IGNORE = ['7pDgsRaydwphT8FlnlzMZd']

ARTISTS_NAMES_SPLIT = [' & ', ' ft ']
SONGS_NAMES_SPLIT = ['/']
VARIOUS_TRACKS = ['various tracks', 'various songs']
COUNTRY = 'GB'

SCOPE = 'playlist-modify-public'


def get_chart():
    with open('chart.json') as f:
        chart = json.load(f)
    return chart


def format_song(artist, track_name, album):
    for split in ARTISTS_NAMES_SPLIT:
        artist = artist.replace(split, '#')

    if '#' in artist:
        artists_names = artist.split('#')
    else:
        artists_names = [artist]

    track_name = track_name.replace('etc', '').replace("'", '')

    for split in SONGS_NAMES_SPLIT:
        track_name = track_name.replace(split, '#')

    if '#' in track_name:
        tracks_names = track_name.split('#')
    else:
        tracks_names = [track_name]

    artists_names = [artist_name.strip(' \t\n\r').lower()
                     for artist_name in artists_names]
    tracks_names = [track_name.strip(' \t\n\r').lower()
                    for track_name in tracks_names]
    album = album.strip(' \t\n\r').lower() if album is not None else album

    artists_names_transformed = []
    for artist_name in artists_names:
        if ARTISTS_NAMES_TRANSFORMATIONS.get(artist_name) is None:
            artists_names_transformed.append(artist_name)
        else:
            artists_names_transformed.append(
                ARTISTS_NAMES_TRANSFORMATIONS.get(artist_name)
            )

    return artists_names_transformed, tracks_names, album


def get_playlist_current_tracks(sp):
    current_tracks = []

    current_playlist_tracks = Playlist(
        sp.user_playlist_tracks(
            settings.SPOTIFY_USERNAME,
            playlist_id=settings.SPOTIFY_PLAYLIST)
    )

    return current_playlist_tracks.tracks_ids


def remove_deleted_tracks(current_tracks, sp, tracks_to_load):
    for current_track in current_tracks:
        if current_track not in tracks_to_load:
            # Remove the track
            sp.user_playlist_remove_all_occurrences_of_tracks(
                settings.SPOTIFY_USERNAME,
                playlist_id=settings.SPOTIFY_PLAYLIST,
                tracks=[current_track],
            )


def is_release_date_in_last_year(track):
    if track.empty():
        return False
    else:
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

        return release_date_formatted > datetime.now() - relativedelta(years=1)


def get_artist_track_query(artist_name, track_name):
    return 'artist:"' + artist_name + '" track:"' + track_name + '"'


def get_current_tracks_to_load(sp):
    tracks_to_load = set()

    for song in get_chart():

        artists_names, tracks_names, album_name = format_song(song['artist'],
                                                              song['title'],
                                                              song['album'])

        for artist_name in artists_names:

            for track_name in tracks_names:

                if track_name in VARIOUS_TRACKS and album_name is not None:
                    # We will try to collect the most interesting tracks
                    # of the album. Spotify doesn't allow to know the
                    # number of plays per album, but we'll use a work-around:
                    # if any track is included in the most played tracks of
                    # the artist, we'll add it to the playlist

                    q = 'artist:"' + artist_name + \
                        '" album:"' + album_name + '"'

                    print(q)

                    album = Album(sp.search(q=q, type='album', limit=1))

                    if not album.empty():
                        artist = album.main_artist

                        album_tracks_ids = album.tracks_ids(sp)
                        artist_top_tracks_ids = artist.top_tracks_ids(
                            sp,
                            COUNTRY
                        )

                        for album_track_id in album_tracks_ids:
                            if album_track_id in artist_top_tracks_ids:
                                tracks_to_load.add(album_track_id)

                else:
                    q = get_artist_track_query(artist_name, track_name)

                    print(q)

                    track = Track(sp.search(q=q, type='track', limit=1))

                    # If not found, try with a corrected misspelling version
                    if track.empty():
                        corrected_values = correct(artist_name, track_name)
                        if corrected_values is not None:
                            q = get_artist_track_query(
                                corrected_values['artist_name'],
                                corrected_values['track_name']
                            )

                            print("(corrected) " + q)

                            track = Track(
                                sp.search(
                                    q=q,
                                    type='track',
                                    limit=1
                                )
                            )

                    if is_release_date_in_last_year(track):
                        tracks_to_load.add(track.id)

    for track_to_load in tracks_to_load:
        if track_to_load in TRACKS_IDS_TO_IGNORE:
            tracks_to_load.remove(track_to_load)

    return tracks_to_load


def add_new_tracks(current_tracks, sp, tracks_to_load):
    for track_to_load in tracks_to_load:
        if track_to_load not in current_tracks:
            # Add the track
            sp.user_playlist_add_tracks(
                settings.SPOTIFY_USERNAME,
                playlist_id=settings.SPOTIFY_PLAYLIST,
                tracks=[track_to_load],
            )


def update_playlist(sp):

    tracks_to_load = get_current_tracks_to_load(sp)

    current_tracks = get_playlist_current_tracks(sp)

    # Remove all current tracks that have gone out of the chart
    remove_deleted_tracks(current_tracks, sp, tracks_to_load)

    # Add all the new tracks that weren't on the playlist
    add_new_tracks(current_tracks, sp, tracks_to_load)


if __name__ == "__main__":
    token = util.prompt_for_user_token(
        settings.SPOTIFY_USERNAME,
        scope=SCOPE,
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIPY_REDIRECT_URI)

    update_playlist(spotipy.Spotify(auth=token))

