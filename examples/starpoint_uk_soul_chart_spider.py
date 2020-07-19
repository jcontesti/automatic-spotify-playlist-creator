import scrapy
from extractors.scrapy_extractor import ScrapyExtractor


class StarpointUKSoulChartSpider(scrapy.Spider, ScrapyExtractor):
    name = "StarpointUKSoulChartSpider"
    start_urls = [
        "http://www.uksoulchart.com/top30/",
    ]

    ALBUM_INDICATOR = " album"

    def parse(self, response):
        chart = response.xpath('//table[@id="tchart"]//tr/td[@class="artist"]')

        for item in chart:

            artist = item.xpath("b//text()").extract_first()
            song_title = item.xpath("span//text()").extract_first().lower()

            song = dict()
            song["artist"] = artist
            song["song_title"] = song_title.replace(self.ALBUM_INDICATOR, "")
            song["album_title"] = (
                song_title.replace(self.ALBUM_INDICATOR, "")
                if self.ALBUM_INDICATOR in song_title
                else ""
            )
            song["label"] = ""

            yield song
