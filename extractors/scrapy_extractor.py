import importlib
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
    ):
        self._spiders = None

    def add_extractor(self, module_name: str, class_name: str):
        spider_module = importlib.import_module(module_name)
        self._spiders.append(getattr(spider_module, class_name))

    def execute_extractors(self):
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

        for spider in self._spiders:
            process.crawl(spider)

        process.start()

    def get_results(self, class_name: str) -> ExtractedPlaylist:
        with open(self.SPIDER_DIR + class_name + ".json") as f:
            results = json.load(f)

        extracted_playlist = ExtractedPlaylist()
        for result in results:
            artist = result["artist"]
            title = result["title"]
            album = result["album"]
            label = result["label"]

            extracted_playlist.add_extracted_song(
                ExtractedSong(
                    artist,
                    title,
                    album,
                    label)
            )

        return extracted_playlist
