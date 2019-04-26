import json
import sys
from datetime import datetime

import spotipy
import spotipy.util as util
from dateutil.relativedelta import relativedelta

import settings
from correctors.misspelling_corrector import correct
from spotify_classes.album import Album
from spotify_classes.track import Track

# Manual transformations of misspellings
ARTISTS_NAMES_TRANSFORMATIONS = {
    '480 east': 'four80east',
    'agape soul': 'darryl anders agapesoul',
    'christian grey': 'christon gray',
    'india arie': 'india.arie',
    'o\'jays': 'the ojays',
    'vivian sessions': 'vivian sessoms',
}

# Tracks ids to ignore
# Useful when we are loading the wrong track but the algorithm can't avoid it
TRACKS_IDS_TO_IGNORE = [

    # Solar Radio
    '7pDgsRaydwphT8FlnlzMZd',

    # Sitting in the Park
    '23bXewXrq3uZgGXbJOeUfb',
    '5OeGxh9dqXO1w3qK9oIRXM',
    '6ET3hABad2RwhqKRG8QCVW',
    '1JKFEswNdaxDZWajFRYhV1',
    '4o7O3JojG5diqkjq0upo0T',
    '31UiUtkjFJDnJM5fkgVJHM',
    '0Q32v70v1QUtLwGsYHW6rf',
    '00atCPWLQHH4dGbmkG40Ha',
    '2tB8w6IDeKXLvdIMD2d7cK',
    '08wAwH3T9tpQZJqCommPQ4',
    '50ZNRhSgme0R1VVtyeg0CT',
    '4AIQCpHyDFf8RFQjN8kvSR',
    '0q86wtltM3bLjHlDUuKpp3',
    '3vs955p0PD6RVZIneleAR9',
    '4L6LeoPbxenjDV0PaVS0CM',
    '4H5Of0Q4GC1R8juNFLASTr',
    '0z6kwqZiVdhfkwIuWwG8pM',
    '4FCwx5XYXU5WQhfstq7Hdq',
    '2Ue94Ecin4XTH43bMV8Gjw',
    '1jU0OWb7urv3a1VfDYu93R',
    '1MRmJF1SrVFymkZWFfHYSz',
    '6gYQOCg1tK5mxbkOFsS6Y0',
    '1mO0lZ5se7oxI7sZweF1MP',
    '796CSByzzzxhGFVzdvcOOJ',
    '1CPt6KmQ7pIr9J2exiV7KD',
    '1CSrlw4sF2dV2MBxwJGKVA',
    '0AFcSOTmCQgDCkyQMvUH6S',
    '0h7vUwwfrGOL3UFPzhlWsf',
    '63vk9gScFYXy2DzGYdDSct',
    '0DJ9r5Zaxtl2Ph90yA6m1Z',
    '1bC2Lxrd6IXDiAhIh4iTQF',
    '0nqVfRdvzleIZImGGUU1wu',
    '6xhiVDN9RIlYEGxmUUQvjX',
    '2MHkBOKkzaBmofdadKuetQ',
    '6fhvokluWpuQy5TgcNQkLo',
    '3tv5TYe7ynHpVhEJpxfUJN',
    '706yOGnWFkzW3XvMefTkCn',
    '7avSJE80Rz7qudDKjQOkwB',
    '5QEKdKOOncqC1ON17Ik1zb',
    '0cThXovxrvU68JuzYUXhJT',
    '0JqDibjI2kbbnUFgEN6V7x',
    '0Gr2y4yFZlBPcMAHdu0ggC',
    '2gKcZ4L2nbOdQpmTY9XwBW',
    '64X5L1sTEx1daLnJioeNT5',
    '1Y1qzhQDgbEkTw0CyXEz79',
    '5xQgDM04FDIBO6K04qaf6C',
    '58Obk57g8KXqQM4tAlCZdF',
]

ARTISTS_NAMES_SPLIT = [' & ',
                       ' ft ',
                       ' feat ',
                       ' feat. ',
                       ' with ',
                       ' and ',
                       ]
SONGS_NAMES_SPLIT = ['/']
VARIOUS_TRACKS = ['various tracks', 'various songs']
COUNTRY = 'GB'

SCOPE = 'playlist-modify-public'


def get_chart(scrapped_songs):
    with open(scrapped_songs) as f:
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


def get_playlist_current_tracks(sp, playlist_id):
    results = sp.user_playlist_tracks(
        settings.SPOTIFY_USERNAME,
        playlist_id=playlist_id
    )
    tracks = results['items']
    while results['next']:  # get more than 100 tracks
        results = sp.next(results)
        tracks.extend(results['items'])

    return [t['track']['id'] for t in tracks]


def remove_deleted_tracks(current_tracks, sp, tracks_to_load, playlist_id):
    for current_track in current_tracks:
        if current_track not in tracks_to_load:
            # Remove the track
            sp.user_playlist_remove_all_occurrences_of_tracks(
                settings.SPOTIFY_USERNAME,
                playlist_id=playlist_id,
                tracks=[current_track],
            )


def extract_released_date(track):
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


def is_release_date_in_last_year(track):
    return \
        extract_released_date(track) > datetime.now() - relativedelta(years=1)


def is_released_date_in_range_years(track, year_from, year_to):
    print(datetime(year_from, 1, 1))
    print(extract_released_date(track))
    return datetime(year_from, 1, 1) <= extract_released_date(track) \
            and extract_released_date(track) <= datetime(year_to, 1, 1)


def is_relesead_in_expected_dates(track, check_released_year):
    if check_released_year.get('last_year'):
        return is_release_date_in_last_year(track)
    elif check_released_year.get('year_from'):
        return is_released_date_in_range_years(
            track,
            check_released_year.get('year_from'),
            check_released_year.get('year_to')
        )
    else:
        return True


def get_artist_track_query(artist_name, track_name):
    return 'artist:"' + artist_name + '" track:"' + track_name + '"'


def get_current_tracks_to_load(sp,
                               scrapped_songs,
                               correct_songs,
                               check_released_year):
    tracks_to_load = set()

    for song in get_chart(scrapped_songs):

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
                                if album_track_id not in TRACKS_IDS_TO_IGNORE:
                                    tracks_to_load.add(album_track_id)

                else:
                    q = get_artist_track_query(artist_name, track_name)

                    print(q)

                    track = Track(sp.search(q=q, type='track', limit=1))

                    # If not found, try with a corrected misspelling version
                    if track.empty() and correct_songs == True:
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

                    if not track.empty() and is_relesead_in_expected_dates(
                            track,
                            check_released_year):
                        if track.id not in TRACKS_IDS_TO_IGNORE:
                            tracks_to_load.add(track.id)

    return tracks_to_load


def add_new_tracks(current_tracks, sp, tracks_to_load, playlist_id):

    # Spotify API doesn't allow to load more than 100 tracks per call
    SPLIT_MAX = 100

    final_tracks_to_append = []
    for track_to_load in tracks_to_load:
        if track_to_load not in current_tracks:
            final_tracks_to_append.append(track_to_load)

    if final_tracks_to_append:
        # Add all the tracks in one call in chunks of SPLIT_MAX
        for i in range(0, len(final_tracks_to_append), SPLIT_MAX):
            sp.user_playlist_add_tracks(
                settings.SPOTIFY_USERNAME,
                playlist_id=playlist_id,
                tracks=final_tracks_to_append[i:i+SPLIT_MAX],
            )


def update_playlist(sp,
                    scrapped_songs,
                    playlist_id,
                    correct_songs,
                    check_released_year):
    tracks_to_load = get_current_tracks_to_load(sp,
                                                scrapped_songs,
                                                correct_songs,
                                                check_released_year)

    current_tracks = get_playlist_current_tracks(sp, playlist_id)

    # Remove all current tracks that have gone out of the chart
    remove_deleted_tracks(current_tracks, sp, tracks_to_load, playlist_id)

    # Add all the new tracks that weren't on the playlist
    add_new_tracks(current_tracks, sp, tracks_to_load, playlist_id)


if __name__ == "__main__":
    scrapped_songs = sys.argv[1]
    if scrapped_songs == 'solar_radio.json':
        playlist_id = settings.SPOTIFY_SOLAR_RADIO_PLAYLIST
        split_artists_names = False
        correct_songs = True
        check_released_year = {'last_year': True}
    elif scrapped_songs == 'sitting_in_the_park.json':
        playlist_id = settings.SPOTIFY_SITTING_IN_THE_PARK_PLAYLIST
        correct_songs = False
        check_released_year = dict()
    else:
        sys.exit(-1)

    token = util.prompt_for_user_token(
        settings.SPOTIFY_USERNAME,
        scope=SCOPE,
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIPY_REDIRECT_URI)

    update_playlist(spotipy.Spotify(auth=token),
                    scrapped_songs,
                    playlist_id,
                    correct_songs,
                    check_released_year)
