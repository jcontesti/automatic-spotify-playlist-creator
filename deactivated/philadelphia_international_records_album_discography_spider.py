import scrapy


class PhiladelphiaInternationalRecordsAlbumDiscographySpider(scrapy.Spider):
    name = "PhiladelphiaInternationalRecordsAlbumDiscographySpider"
    start_urls = [
        "http://www.bsnpubs.com/columbia/pi.html",
    ]

    def parse(self, response):

        # We only are interested in the <b> tags after "Distributed by Columbia"
        # Exclude <b> tags which don't correspond to any artist name
        pir_artists_names = response.xpath(
            "//b[contains(text(),'Distributed by Columbia')]/following::b[not(contains(text(), ':'))]/text()"
        ).extract()

        # We only are interested in the <i> tags after "Distributed by Columbia"
        pir_albums_names = response.xpath(
            "//b[contains(text(),'CBS 30000 consolidated series (Distributed by Columbia):')]/following::i/text()"
        ).extract()

        for artist, album in zip(pir_artists_names, pir_albums_names):

            print(artist, " - ", album)

            song = dict()
            song["artist"] = artist
            song["title"] = ""  # load only complete albums
            song["album"] = album
            song["label"] = ""  # leave it empty, not important for Spotify

            yield song
