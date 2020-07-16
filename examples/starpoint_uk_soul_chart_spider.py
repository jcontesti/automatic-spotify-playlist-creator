import scrapy
from extractors.scrapy_extractor import ScrapyExtractor


class StarpointUKSoulChartSpider(scrapy.Spider, ScrapyExtractor):
    name = "StarpointUKSoulChartSpider"
    start_urls = [
        "http://www.uksoulchart.com/top30/",
    ]

    ALBUM_INDICATOR = " Album"
    VARIOUS_TRACKS = "/various tracks"

    def parse(self, response):
        chart = response.xpath('//table[@id="tchart"]//tr/td[@class="artist"]')

        for item in chart:

            artist = item.xpath("b//text()").extract_first()
            song_title = item.xpath("span//text()").extract_first()

            song = dict()
            song["artist"] = artist
            song["song_title"] = (
                title.replace(self.ALBUM_INDICATOR, "") + self.VARIOUS_TRACKS
                if self.ALBUM_INDICATOR in song_title
                else song_title
            )
            song["album_title"] = (
                song_title.replace(self.ALBUM_INDICATOR, "")
                if self.ALBUM_INDICATOR in song_title
                else ""
            )
            song["label"] = ""

            yield song
