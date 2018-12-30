import json

import spotipy
import spotipy.util as util

import settings

# Manual transformations of misspellings
ARTISTS_NAMES_TRANSFORMATIONS = {
    '480 east': 'four80east',
    'agape soul': 'darryl anders agapesoul',
    'india arie': 'india.arie',
    'vivian sessions': 'vivian sessoms',
}

# Tracks ids to ignore
# Useful when we are loading the wrong track but the algorithm can't avoid it
TRACKS_IDS_TO_IGNORE = ['7pDgsRaydwphT8FlnlzMZd']

ARTISTS_NAMES_SPLIT = [' & ', ' ft ']
SONGS_NAMES_SPLIT = ['/']
VARIOUS_TRACKS = 'various tracks'
COUNTRY = 'GB'

SCOPE = 'playlist-modify-public'


def get_chart():
    with open('chart.json') as f:
        chart = json.load(f)
    return chart


def process_song(artist, track_name, album):
    for split in ARTISTS_NAMES_SPLIT:
        artist = artist.replace(split, '#')

    if '#' in artist:
        artists_names = artist.split('#')
    else:
        artists_names = [artist]

    track_name = track_name.replace('etc', '')

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

    current_playlist_tracks = sp.user_playlist_tracks(
        settings.SPOTIFY_USERNAME,
        playlist_id=settings.SPOTIFY_PLAYLIST)

    for current_track in current_playlist_tracks['items']:
        current_tracks.append(current_track['track']['id'])

    return current_tracks


def remove_deleted_tracks(current_tracks, sp, tracks_to_load):
    for current_track in current_tracks:
        if current_track not in tracks_to_load:
            # Remove the track
            sp.user_playlist_remove_all_occurrences_of_tracks(
                settings.SPOTIFY_USERNAME,
                playlist_id=settings.SPOTIFY_PLAYLIST,
                tracks=[current_track],
            )


def add_new_tracks(current_tracks, sp, tracks_to_load):
    for track_to_load in tracks_to_load:
        if track_to_load not in current_tracks:
            # Add the track
            sp.user_playlist_add_tracks(
                settings.SPOTIFY_USERNAME,
                playlist_id=settings.SPOTIFY_PLAYLIST,
                tracks=[track_to_load],
            )


def get_tracks_to_load(sp):
    tracks_to_load = []

    for song in get_chart():

        artists_names, tracks_names, album = process_song(song['artist'],
                                                          song['title'],
                                                          song['album'])

        for artist_name in artists_names:

            for track_name in tracks_names:
                if track_name == VARIOUS_TRACKS:
                    # We will try to collect the most interesting tracks
                    # of the album. Spotify doesn't allow to know the
                    # number of plays per album, but we'll use a work-around:
                    # if any track is included in the most played tracks of
                    # the artist, we'll add it to the playlist

                    q = 'artist:"' + artist_name + \
                        '" album:"' + album + '"'

                    print(q)

                    results = sp.search(q=q, type='album', limit=1)

                    if results['albums']['items']:
                        album_id = results['albums']['items'][0]['id']
                        artist_id = results['albums']['items'][0]['artists'][0]['id']

                        album_tracks = sp.album_tracks(album_id)
                        artist_top_tracks = sp.artist_top_tracks(artist_id,
                                                                 country=COUNTRY)

                        album_tracks_id = []
                        for album_track in album_tracks['items']:
                            album_tracks_id.append(album_track['id'])

                        artist_top_tracks_id = []
                        for artist_top_track in artist_top_tracks['tracks']:
                            artist_top_tracks_id.append(artist_top_track['id'])

                        for album_track_id in album_tracks_id:
                            if album_track_id in artist_top_tracks_id:
                                tracks_to_load.append(album_track_id)

                else:
                    q = 'artist:"' + artist_name + \
                        '" track:"' + track_name + '"'

                    print(q)

                    results = sp.search(q=q, type='track', limit=1)

                    if results['tracks']['items']:
                        tracks_to_load.append(results['tracks']['items'][0]['id'])

    for track_to_load in tracks_to_load:
        if track_to_load in TRACKS_IDS_TO_IGNORE:
            tracks_to_load.remove(track_to_load)

    return tracks_to_load


def update_playlist(sp):

    tracks_to_load = get_tracks_to_load(sp)

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

