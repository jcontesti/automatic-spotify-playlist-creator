from googleapiclient.discovery import build

import settings

SEPARATOR = ' : '


def correct(artist_name,
            track_name,
            google_api_key=settings.GOOGLE_API_KEY,
            google_cse_key=settings.GOOGLE_CSE_KEY,
            **kwargs):

    service = build('customsearch', 'v1', developerKey=google_api_key)

    query = artist_name + SEPARATOR + track_name

    result = service.cse().list(q=query, cx=google_cse_key, **kwargs).execute()

    if 'spelling' in result:
        corrected = result['spelling']['correctedQuery'].split(SEPARATOR)

        artist_name = corrected[0]
        track_name = corrected[1]

        return {'artist_name': artist_name, 'track_name': track_name}
    else:
        return None
