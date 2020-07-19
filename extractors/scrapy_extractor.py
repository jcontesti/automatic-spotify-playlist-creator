import json
import shutil

from scrapy.crawler import CrawlerProcess

from extracted_data.extracted_playlist import ExtractedPlaylist
from extracted_data.extracted_song import ExtractedSong
from extractors.extractor import Extractor


class ScrapyExtractor(Extractor):
    SPIDER_USER_AGENT = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
    SPIDER_FEED_FORMAT = "json"
    SPIDER_DIR = "./tmp/"
    SPIDER_FILE = "%(name)s.json"

    def __init__(
            self,
            module_name: str,
            class_name: str,
            module: str,
            extractor: callable,
    ):
        self._module_name = module_name
        self._class_name = class_name
        self._module = module
        self._extractor = extractor

    def _execute(self):
        try:
            shutil.rmtree(self.SPIDER_DIR)
        except OSError:
            pass

        process = CrawlerProcess(
            {
                "USER_AGENT": self.SPIDER_USER_AGENT,
                "FEED_FORMAT": self.SPIDER_FEED_FORMAT,
                "FEED_URI": self.SPIDER_DIR + self.SPIDER_FILE,
            }
        )
        process.crawl(self._extractor)
        process.start()

    def extract_playlist(self) -> ExtractedPlaylist:
        self._execute()

        with open(self.SPIDER_DIR + self._class_name + ".json") as f:
            results = json.load(f)

        extracted_playlist = ExtractedPlaylist()
        for result in results:
            artist = result["artist"]
            song_title = result["song_title"]
            song_album = result["album_title"]
            label = result["label"]

            extracted_playlist.add_extracted_song(
                ExtractedSong(
                    artist,
                    song_title,
                    song_album,
                    label)
            )

        return extracted_playlist
