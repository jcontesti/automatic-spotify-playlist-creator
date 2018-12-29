import json

import spotipy
import spotipy.util as util

import settings

# Manual transformations of misspellings
ARTISTS_NAMES_TRANSFORMATIONS = {
    '480 east': 'four80east',
    'india arie': 'india.arie',
}

SCOPE = 'playlist-modify-public'


def get_chart():
    with open('chart.json') as f:
        chart = json.load(f)
    return chart


def process_song(artist, track_name):
    if 'ft' in artist:
        artists_names = artist.split('ft')
    else:
        artists_names = [artist]

    track_name = track_name.replace('etc', '')

    if '/' in track_name:
        tracks_names = track_name.split('/')
    else:
        tracks_names = [track_name]

    artists_names = [artist_name.strip(' \t\n\r').lower()
                     for artist_name in artists_names]
    tracks_names = [track_name.strip(' \t\n\r').lower()
                    for track_name in tracks_names]

    artists_names_transformed = []
    for artist_name in artists_names:
        if ARTISTS_NAMES_TRANSFORMATIONS.get(artist_name) is None:
            artists_names_transformed.append(artist_name)
        else:
            artists_names_transformed.append(
                ARTISTS_NAMES_TRANSFORMATIONS.get(artist_name)
            )

    return artists_names_transformed, tracks_names


def get_playlist_current_tracks():
    current_tracks = []

    current_playlist_tracks = sp.user_playlist_tracks(
        settings.SPOTIFY_USERNAME,
        playlist_id=settings.SPOTIFY_PLAYLIST)

    for current_track in current_playlist_tracks['items']:
        current_tracks.append(current_track['track']['id'])

    return current_tracks


def update_playlist(sp):

    tracks_to_load = []

    for song in get_chart():
        artists_names, tracks_names = process_song(song['artist'],
                                                   song['title'])

        for artist_name in artists_names:
            for track_name in tracks_names:
                q = 'artist:"' + artist_name + '" track:"' + track_name + '"'

                print(q)

                results = sp.search(q=q, type='track', limit=1)

                if results['tracks']['items']:
                    tracks_to_load.append(results['tracks']['items'][0]['id'])

    current_tracks = get_playlist_current_tracks()

    # Remove all current tracks that have gone out of the chart
    for current_track in current_tracks:
        if current_track not in tracks_to_load:
            # Remove the track
            sp.user_playlist_remove_all_occurrences_of_tracks(
                settings.SPOTIFY_USERNAME,
                playlist_id=settings.SPOTIFY_PLAYLIST,
                tracks=[current_track],
            )

    # Add all the new tracks that weren't on the playlist
    for track_to_load in tracks_to_load:
        if track_to_load not in current_tracks:
            # Add the track
            sp.user_playlist_add_tracks(
                settings.SPOTIFY_USERNAME,
                playlist_id=settings.SPOTIFY_PLAYLIST,
                tracks=[track_to_load],
            )


if __name__ == "__main__":
    token = util.prompt_for_user_token(
        settings.SPOTIFY_USERNAME,
        scope=SCOPE,
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIPY_REDIRECT_URI)

    sp = spotipy.Spotify(auth=token)

    update_playlist(sp)

