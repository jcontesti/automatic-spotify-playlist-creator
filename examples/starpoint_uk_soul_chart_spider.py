"""Class to implement Starpoint Radio UK Soul Chart Scrapy spider."""
from typing import Dict, Generator

import re
import scrapy
from scrapy.http import TextResponse

from extractors.scrapy_extractor import ScrapyExtractor


class StarpointUKSoulChartSpider(
    scrapy.Spider,  # type: ignore
    ScrapyExtractor
):
    """Class to implement Starpoint Radio UK Soul Chart Scrapy spider."""
    name = "StarpointUKSoulChartSpider"
    start_urls = [
        "http://www.uksoulchart.com/top30/",
    ]

    ALBUM_INDICATORS = [" album", "/Album", "/album"]
    REMOVE_TEXT_BETWEEN_PARENTHESES = False

    def _remove_album_indicator(self, song_title: str) -> str:
        song_title_wo_album_indicator: str = song_title
        for album_indicator in self.ALBUM_INDICATORS:
            song_title_wo_album_indicator = (
                song_title_wo_album_indicator.replace(album_indicator, "")
            )

        return song_title_wo_album_indicator

    def _extract_album(self, song_title: str) -> str:
        album: str = song_title
        for album_indicator in self.ALBUM_INDICATORS:
            album = album.replace(album_indicator, "")

        # return empty string any album indicator has been found in the song title
        return album if album != song_title else ""

    @staticmethod
    def _remove_text_between_parentheses(text: str) -> str:
        return re.sub(r"[\(\[].*?[\)\]]", "", text)

    def parse(self, response: TextResponse) -> Generator[Dict[str, str], None, None]:
        chart = response.xpath('//table[@id="tchart"]//tr/td[@class="artist"]')

        for item in chart:

            artist = item.xpath("b//text()").extract_first()
            song_title = item.xpath("span//text()").extract_first().lower()

            song = dict()
            song["artist"] = artist
            song["song_title"] = (
                self._remove_album_indicator(song_title)
                if self.REMOVE_TEXT_BETWEEN_PARENTHESES
                else self._remove_text_between_parentheses(
                        self._remove_album_indicator(song_title)
                )
            )
            song["album_title"] = (
                self._extract_album(song_title)
                if self.REMOVE_TEXT_BETWEEN_PARENTHESES
                else self._remove_text_between_parentheses(
                    self._extract_album(song_title)
                )
            )
            song["label"] = ""

            yield song
