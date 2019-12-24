from dotenv import load_dotenv
import os

load_dotenv()
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")
SPOTIFY_USERNAME = os.environ.get("SPOTIFY_USERNAME")
SPOTIFY_SCOPE = os.environ.get("SPOTIFY_SCOPE")

GOOGLE_API_KEY=os.environ.get("GOOGLE_API_KEY")
GOOGLE_CSE_KEY=os.environ.get("GOOGLE_CSE_KEY")
