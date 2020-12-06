"""Extractor class using Scrapy."""
import json
import shutil
from types import ModuleType
from typing import Any, Final

from scrapy.crawler import CrawlerProcess

from extracted_data.extracted_playlist import ExtractedPlaylist
from extracted_data.extracted_song import ExtractedSong
from extractors.extractor import Extractor


class ScrapyExtractor(Extractor):
    """Extractor class using Scrapy."""

    SPIDER_USER_AGENT: Final[str] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
    SPIDER_FEED_FORMAT: Final[str] = "json"
    SPIDER_DIR: Final[str] = "./tmp/"
    SPIDER_FILE: Final[str] = "%(name)s.json"

    def __init__(
            self,
            module_name: str,
            class_name: str,
            module: ModuleType,
            extractor: Any,
    ) -> None:
        self._module_name: str = module_name
        self._class_name: str = class_name
        self._module: ModuleType = module
        self._extractor: Any = extractor

    def _execute(self) -> None:
        try:
            shutil.rmtree(self.SPIDER_DIR)
        except OSError:
            pass

        process: CrawlerProcess = CrawlerProcess(
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

        with open(self.SPIDER_DIR + self._class_name + ".json") as file:
            results: Any = json.load(file)

        extracted_playlist: ExtractedPlaylist = ExtractedPlaylist()
        for result in results:
            artist: str = result["artist"]
            song_title: str = result["song_title"]
            song_album: str = result["album_title"]
            label: str = result["label"]

            extracted_playlist.add_extracted_song(
                ExtractedSong(
                    artist,
                    song_title,
                    song_album,
                    label)
            )

        return extracted_playlist
