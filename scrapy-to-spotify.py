import glob
import logging
import importlib
import os
import sys
import json
import yaml
import settings
import spotipy
from scrapy.crawler import CrawlerProcess
import spotipy.util as util
from scrapped_song import ScrappedSong
from scrapped_playlist import ScrappedPlaylist

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

PLAYLISTS_CONFIG_PATH = './config/*.yaml'
SPIDER_USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
SPIDER_FEED_FORMAT = 'json'
SPIDER_FEED_URI = './tmp/playlist_data.json'


def read_yaml(yaml_file):
    with open(yaml_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def execute_spider(module, class_name):
    spider_module = importlib.import_module(module)
    spider_class = getattr(spider_module, class_name)

    try:
        os.remove(SPIDER_FEED_URI)
    except OSError:
        pass

    process = CrawlerProcess({
        'USER_AGENT': SPIDER_USER_AGENT,
        'FEED_FORMAT': SPIDER_FEED_FORMAT,
        'FEED_URI': SPIDER_FEED_URI,
    })
    process.crawl(spider_class)
    process.start()

    with open(SPIDER_FEED_URI) as f:
        return json.load(f)


if __name__ == "__main__":

    token = util.prompt_for_user_token(
        settings.SPOTIFY_USERNAME,
        scope=settings.SPOTIFY_SCOPE,
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI)

    config_files = glob.glob(PLAYLISTS_CONFIG_PATH)

    for config_file in config_files:

        playlist_config = read_yaml(config_file)
        logging.info('Loading ' + playlist_config.get('name'))

        spider_module_name = playlist_config.get('spider_module')
        spider_class_name = playlist_config.get('spider_class')
        spider_results = execute_spider(spider_module_name, spider_class_name)

        scrapped_songs = []
        for spider_result in spider_results:
            artist = spider_result['artist']
            title = spider_result['title']
            album = spider_result['album']
            label = spider_result['label']

            scrapped_song = ScrappedSong(artist, title, album, label)

            scrapped_songs.append(scrapped_song)

        spotify_playlist = playlist_config.get('spotify_playlist')
        spotify_session = spotipy.Spotify(auth=token)
        spotify_username = settings.SPOTIFY_USERNAME
        spotify_country = playlist_config.get('spotify_country')
        spotify_ignored_tracks = playlist_config.get('spotify_ignored_tracks')
        artists_split = playlist_config.get('artists_split')
        songs_titles_split = playlist_config.get('songs_titles_split')
        various_titles_in_one_tokens = \
            playlist_config.get('various_titles_in_one_tokens')
        check_released_last_year = \
            playlist_config.get('check_released_last_year')
        misspelling_corrector_module = \
            playlist_config.get('misspelling_corrector_module')
        misspelling_corrector_class = \
            playlist_config.get('misspelling_corrector_class')
        artists_transformations = \
            playlist_config.get('artists_transformations')

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
            check_released_last_year,
            misspelling_corrector_module,
            misspelling_corrector_class,
            artists_transformations)

        scrapped_playlist.update_playlist()






