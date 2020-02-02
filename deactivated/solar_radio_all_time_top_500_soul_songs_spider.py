import scrapy


class SolarRadioAllTimeTop500SoulSongsSpider(scrapy.Spider):
    name = "SolarRadioAllTimeTop500SoulSongsSpider"
    start_urls = [
        "http://www.solarradio.com/solar-radio-top-500-2020/",
        "http://www.solarradio.com/solar-radio-top-500-2020-101-200/",
        "http://www.solarradio.com/solar-radio-top-500-2020-201-300/",
    ]

    def parse(self, response):
        top_500 = response.xpath(
            '//section[contains(@class, "entry")]/p[normalize-space()]/text()'
        ).extract()

        for item in top_500:

            item_separators = ["-", "–", "LP", "."]

            for separator in item_separators:
                item = item.replace(separator, "#")

            tokens = item.split("#")

            print(tokens)

            song = dict()

            artist = tokens[0]
            song["artist"] = artist[artist.find(" ") :]  # remove initial digits
            song["title"] = tokens[-1]
            song["album"] = ""
            song["label"] = ""

            yield song
