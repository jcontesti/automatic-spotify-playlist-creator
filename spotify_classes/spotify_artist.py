class SpotifyArtist:
    def __init__(self, artist):
        self._artist = artist

    @property
    def id(self):
        return self._artist['id']

    def top_tracks_ids(self, sp, country):
        return [t['id'] for t in
                sp.artist_top_tracks(self.id, country=country)['tracks']
                ]
