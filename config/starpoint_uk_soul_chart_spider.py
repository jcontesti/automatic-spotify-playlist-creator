import scrapy


class StarpointUKSoulChartSpider(scrapy.Spider):
    name = 'StarpointUKSoulChartSpider'
    start_urls = [
        'http://www.uksoulchart.com/top30/',
    ]

    def parse(self, response):
        chart = response.xpath(
            '//table[@id="tchart"]//tr/td[@class="artist"]'
        )

        for item in chart:

            artist = item.xpath('b//text()').extract_first()
            title = item.xpath('span//text()').extract_first()

            song = dict()
            song['artist'] = artist
            song['title'] = title
            song['album'] = ''
            song['label'] = ''

            yield song
