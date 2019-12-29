import scrapy


class SolarRadioSoulEnergyHouseChartSpider(scrapy.Spider):
    name = "SolarRadioSoulEnergyHouseChartSpider"
    start_urls = [
        "http://www.solarradio.com/show/soul-energy-house-chart/",
    ]

    def parse(self, response):
        chart_link = response.xpath(
            '//a[contains(@href, "playlists/soul-energy")]/@href'
        ).extract_first()
        yield response.follow(chart_link, callback=self._parse_playlist)

    @staticmethod
    def _parse_playlist(response):
        chart = response.xpath('//div[@class="myplaylist-playlist-entires"]/table//tr')

        for item in chart[1:]:
            artist = item.xpath("td[3]//text()").extract_first()
            title = item.xpath("td[4]//text()").extract_first()
            album = item.xpath("td[5]//text()").extract_first() or ""
            label = item.xpath("td[6]//text()").extract_first() or ""

            song = dict()
            song["artist"] = artist
            song["title"] = title
            song["album"] = album
            song["label"] = label

            yield song
