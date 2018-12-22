import json

import spotipy
import spotipy.util as util

import settings

ARTISTS_NAMES_TRANSFORMATIONS = {
    '480 east': 'four80east',
    'india arie': 'india.arie',
}


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


scope = 'playlist-modify-public'
token = util.prompt_for_user_token(
    settings.SPOTIFY_USERNAME,
    scope=scope,
    client_id=settings.SPOTIPY_CLIENT_ID,
    client_secret=settings.SPOTIPY_CLIENT_SECRET,
    redirect_uri=settings.SPOTIPY_REDIRECT_URI)

sp = spotipy.Spotify(auth=token)

# empty playlist
current_songs = sp.user_playlist(settings.SPOTIFY_USERNAME,
            playlist_id=settings.SPOTIFY_PLAYLIST)

for song in current_songs['tracks']['items']:

    track_id = song['track']['id']

    sp.user_playlist_remove_all_occurrences_of_tracks(
        settings.SPOTIFY_USERNAME,
        playlist_id=settings.SPOTIFY_PLAYLIST,
        tracks=[track_id],
    )

# fill playlist
for song in get_chart():
    artists_names, tracks_names = process_song(song['artist'], song['title'])

    for artist_name in artists_names:
        for track_name in tracks_names:
            q = 'artist:"' + artist_name + '" track:"' + track_name + '"'

            print(q)

            results = sp.search(q=q, type='track', limit=1)

            if results['tracks']['items']:
                track_id = results['tracks']['items'][0]['id']

                sp.user_playlist_add_tracks(
                    settings.SPOTIFY_USERNAME,
                    playlist_id=settings.SPOTIFY_PLAYLIST,
                    tracks=[track_id])
