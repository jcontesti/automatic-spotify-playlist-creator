import scrapy


class ChartSpider(scrapy.Spider):
    name = "chart spider"
    start_urls = [
        'http://www.solarradio.com/show/sweet-rhythms-chart/',
    ]

    def parse(self, response):
        chart_link = response.xpath('//a[contains(@href, "playlists/sweet-rhythms-chart")]/@href').extract_first()
        yield response.follow(chart_link, callback=self.parse_chart)

    def parse_chart(self, response):
        chart = response.xpath('//div[@class="myplaylist-playlist-entires"]/table//tr')

        for item in chart[1:]:
            song = dict()
            song['artist'] = item.xpath('td[3]//text()').extract_first()
            song['title'] = item.xpath('td[4]//text()').extract_first()
            song['album'] = item.xpath('td[5]//text()').extract_first()
            song['label'] = item.xpath('td[6]//text()').extract_first()

            yield song
