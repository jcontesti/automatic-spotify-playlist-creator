import glob
import importlib
import json
import logging
import shutil
import sys

import spotipy
import spotipy.util as util
import yaml
from scrapy.crawler import CrawlerProcess

import settings
from scrapped_classes.scrapped_playlist import ScrappedPlaylist
from scrapped_classes.scrapped_song import ScrappedSong

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

PLAYLISTS_CONFIG_PATH = "./config/*.yaml"
SPIDER_USER_AGENT = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
SPIDER_FEED_FORMAT = "json"
SPIDER_DIR = "./tmp/"
SPIDER_FILE = "%(name)s.json"


def read_yaml(yaml_file):
    with open(yaml_file, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def execute_spider(spiders):
    try:
        shutil.rmtree(SPIDER_DIR)
    except OSError:
        pass

    process = CrawlerProcess(
        {
            "USER_AGENT": SPIDER_USER_AGENT,
            "FEED_FORMAT": SPIDER_FEED_FORMAT,
            "FEED_URI": SPIDER_DIR + SPIDER_FILE,
        }
    )

    for spider in spiders:
        process.crawl(spider)

    process.start()


if __name__ == "__main__":

    token = util.prompt_for_user_token(
        settings.SPOTIFY_USERNAME,
        scope=settings.SPOTIFY_SCOPE,
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIPY_REDIRECT_URI,
    )

    config_files = glob.glob(PLAYLISTS_CONFIG_PATH)

    spiders = []
    for config_file in config_files:

        playlist_config = read_yaml(config_file)
        logging.info("Loading " + playlist_config.get("name"))

        spider_module_name = playlist_config.get("spider_module")
        spider_class_name = playlist_config.get("spider_class")
        spider_module = importlib.import_module(spider_module_name)
        spider = getattr(spider_module, spider_class_name)
        spiders.append(spider)

    execute_spider(spiders)

    for config_file in config_files:

        playlist_config = read_yaml(config_file)

        spider_class = playlist_config.get("spider_class")

        with open(SPIDER_DIR + spider_class + ".json") as f:
            results = json.load(f)

        scrapped_songs = []
        for result in results:
            artist = result["artist"]
            title = result["title"]
            album = result["album"]
            label = result["label"]

            scrapped_song = ScrappedSong(artist, title, album, label)

            scrapped_songs.append(scrapped_song)

        if scrapped_songs:
            spotify_playlist = playlist_config.get("spotify_playlist")
            spotify_session = spotipy.Spotify(auth=token)
            spotify_username = settings.SPOTIFY_USERNAME
            spotify_country = playlist_config.get("spotify_country")
            spotify_ignored_tracks = playlist_config.get("spotify_ignored_tracks")
            artists_split = playlist_config.get("artists_split")
            songs_titles_split = playlist_config.get("songs_titles_split")
            various_titles_in_one_tokens = playlist_config.get(
                "various_titles_in_one_tokens"
            )
            get_full_albums = playlist_config.get(
                "get_full_albums"
            )
            get_only_most_played_songs_from_albums = playlist_config.get(
                "get_only_most_played_songs_from_albums"
            )
            check_released_last_year = playlist_config.get("check_released_last_year")
            artists_transformations = playlist_config.get("artists_transformations")
            misspelling_correctors = playlist_config.get("misspelling_correctors")

            scrapped_playlist = ScrappedPlaylist(
                spotify_playlist,
                spotify_session,
                spotify_username,
                spotify_country,
                scrapped_songs,
                spotify_ignored_tracks,
                artists_split,
                songs_titles_split,
                various_titles_in_one_tokens,
                get_full_albums,
                get_only_most_played_songs_from_albums,
                check_released_last_year,
                artists_transformations,
                misspelling_correctors,
            )

            scrapped_playlist.update_playlist()
