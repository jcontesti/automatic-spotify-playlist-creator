import scrapy


class StarpointUKSoulChartSpider(scrapy.Spider):
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
            title = item.xpath("span//text()").extract_first()

            song = dict()
            song["artist"] = artist
            song["title"] = (
                title.replace(self.ALBUM_INDICATOR, "") + self.VARIOUS_TRACKS
                if self.ALBUM_INDICATOR in title
                else title
            )
            song["album"] = (
                title.replace(self.ALBUM_INDICATOR, "")
                if self.ALBUM_INDICATOR in title
                else ""
            )
            song["label"] = ""

            yield song
