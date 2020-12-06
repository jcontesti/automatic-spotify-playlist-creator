"""File to load all the environment variables."""
import os
from typing import NamedTuple

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Settings(NamedTuple):  # pylint: disable=inherit-non-class
    """Class that contains all environment variables values."""
    SPOTIPY_CLIENT_ID: str = os.environ.get("SPOTIPY_CLIENT_ID", "")
    SPOTIPY_CLIENT_SECRET: str = os.environ.get("SPOTIPY_CLIENT_SECRET", "")
    SPOTIPY_REDIRECT_URI: str = os.environ.get("SPOTIPY_REDIRECT_URI", "")
    SPOTIFY_USERNAME: str = os.environ.get("SPOTIFY_USERNAME", "")
    SPOTIFY_SCOPE: str = os.environ.get("SPOTIFY_SCOPE", "")
    GOOGLE_API_KEY: str = os.environ.get("GOOGLE_API_KEY", "")
    GOOGLE_CSE_KEY: str = os.environ.get("GOOGLE_CSE_KEY", "")
