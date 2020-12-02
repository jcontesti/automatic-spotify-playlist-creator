import scrapy
from scrapy.http import TextResponse
from extractors.scrapy_extractor import ScrapyExtractor
from typing import Dict, Generator


class SolarRadioSoulEnergyHouseChartSpider(
    scrapy.Spider,  # type: ignore
    ScrapyExtractor
):
    name = "SolarRadioSoulEnergyHouseChartSpider"
    start_urls = [
        "http://www.solarradio.com/show/soul-energy-house-chart/",
    ]

    def parse(self, response: TextResponse) -> Generator[Dict[str, str], None, None]:
        chart_link = response.xpath(
            '//a[contains(@href, "playlists/soul-energy")]/@href'
        ).extract_first()
        yield response.follow(chart_link, callback=self._parse_playlist)

    @staticmethod
    def _parse_playlist(
            response: TextResponse
    ) -> Generator[Dict[str, str], None, None]:
        chart = response.xpath('//div[@class="myplaylist-playlist-entires"]/table//tr')

        for item in chart[1:]:
            artist = item.xpath("td[3]//text()").extract_first()
            song_title = item.xpath("td[4]//text()").extract_first()
            album_title = item.xpath("td[5]//text()").extract_first() or ""
            label = item.xpath("td[6]//text()").extract_first() or ""

            song = dict()
            song["artist"] = artist
            song["song_title"] = song_title
            song["album_title"] = album_title
            song["label"] = label

            yield song
