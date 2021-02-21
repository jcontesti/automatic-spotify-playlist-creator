"""Environment variables loader."""
import os
from typing import NamedTuple

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Settings(NamedTuple):  # pylint: disable=inherit-non-class
    """Class that contains all environment variables values."""
    SPOTIPY_CLIENT_ID: str
    SPOTIPY_CLIENT_SECRET: str
    SPOTIPY_REDIRECT_URI: str
    SPOTIFY_USERNAME: str
    SPOTIFY_SCOPE: str
    GOOGLE_API_KEY: str
    GOOGLE_CSE_KEY: str


# Initialize Settings with environment values
environment_settings = Settings(
     SPOTIPY_CLIENT_ID=os.environ.get("SPOTIPY_CLIENT_ID", ""),
     SPOTIPY_CLIENT_SECRET=os.environ.get("SPOTIPY_CLIENT_SECRET", ""),
     SPOTIPY_REDIRECT_URI=os.environ.get("SPOTIPY_REDIRECT_URI", ""),
     SPOTIFY_USERNAME=os.environ.get("SPOTIFY_USERNAME", ""),
     SPOTIFY_SCOPE=os.environ.get("SPOTIFY_SCOPE", ""),
     GOOGLE_API_KEY=os.environ.get("GOOGLE_API_KEY", ""),
     GOOGLE_CSE_KEY=os.environ.get("GOOGLE_CSE_KEY", "")
)
