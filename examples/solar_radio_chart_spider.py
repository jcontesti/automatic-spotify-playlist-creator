"""Base class for any Solar Radio Chart Scrapy spider."""
from typing import Any, Dict, Generator, Optional

import scrapy
from scrapy.http import TextResponse

from extractors.scrapy_extractor import ScrapyExtractor


class SolarRadioChartSpider(
    scrapy.Spider,  # type: ignore
    ScrapyExtractor
):
    """Base class for any Solar Radio Chart Scrapy spider."""

    chart_link_xpath: Optional[str] = None

    def parse(
            self, response: TextResponse, **kwargs: Optional[Any]
    ) -> Generator[Dict[str, str], None, None]:
        chart_link = response.xpath(self.chart_link_xpath).extract_first()
        yield response.follow(chart_link, callback=self._parse_playlist)

    @staticmethod
    def _parse_playlist(
            response: TextResponse
    ) -> Generator[Dict[str, str], None, None]:
        chart = response.xpath('//div[@class="myplaylist-playlist-entires"]/table//tr')

        for item in chart[1:]:
            artist = item.xpath("td[3]//text()").extract_first() or ""
            song_title = item.xpath("td[4]//text()").extract_first() or ""
            album_title = item.xpath("td[5]//text()").extract_first() or ""
            label = item.xpath("td[6]//text()").extract_first() or ""

            song = dict()
            song["artist"] = artist
            song["song_title"] = song_title
            song["album_title"] = album_title
            song["label"] = label

            yield song
