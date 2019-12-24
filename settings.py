from dotenv import load_dotenv
import os

load_dotenv()
SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI')
SPOTIFY_USERNAME = os.environ.get('SPOTIFY_USERNAME')
SPOTIFY_SCOPE = os.environ.get('SPOTIFY_SCOPE')

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_CSE_KEY = os.environ.get('GOOGLE_CSE_KEY')

LASTFM_API_KEY = os.environ.get('LASTFM_API_KEY')
LASTFM_SECRET = os.environ.get('LASTFM_SECRET')