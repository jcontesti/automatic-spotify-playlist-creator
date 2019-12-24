import settings
import requests


class LastFMMisspellingCorrector:

    @staticmethod
    def correct(artist_name,
                track_name,
                lastfm_api_key=settings.LASTFM_API_KEY,
                **kwargs):

        url = 'http://ws.audioscrobbler.com/2.0/'
        params = {
            'method': 'track.getcorrection',
            'artist': artist_name,
            'track': track_name,
            'api_key': lastfm_api_key,
            'format': 'json'
        }

        result = requests.get(url=url, params=params)

        data = result.json()

        if 'corrections' in data:
            correction = data.get('corrections').get('correction')
            track = correction.get('track')

            if 'name' in track:
                artist_name = track.get('artist').get('name')
                track_name = track.get('name')

                return {'artist': artist_name, 'song': track_name}

        return None
