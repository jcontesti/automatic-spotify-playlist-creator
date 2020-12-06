"""Class to implement Solar Radio Sweet Rhythms Chart Scrapy spider."""

from typing import List, Optional

from examples.solar_radio_chart_spider import SolarRadioChartSpider


class SolarRadioSweetRhythmsChartSpider(SolarRadioChartSpider):
    """Class to implement Solar Radio Sweet Rhythms Chart Scrapy spider."""
    name: str = "SolarRadioSweetRhythmsChartSpider"
    start_urls: List[str] = [
        "http://www.solarradio.com/show/sweet-rhythms-chart/",
    ]
    chart_link_xpath: Optional[str] = (
        '//a[contains(@href, "playlists/")]/@href'
    )
