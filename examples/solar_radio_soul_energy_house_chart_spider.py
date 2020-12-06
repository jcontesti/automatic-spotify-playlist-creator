"""Class to implement Solar Radio Soul Energy House Chart Scrapy spider."""

from typing import List, Optional

from examples.solar_radio_chart_spider import SolarRadioChartSpider


class SolarRadioSoulEnergyHouseChartSpider(SolarRadioChartSpider):
    """Class to implement Solar Radio Soul Energy House Chart Scrapy spider."""
    name: str = "SolarRadioSoulEnergyHouseChartSpider"
    start_urls: List[str] = [
        "http://www.solarradio.com/show/soul-energy-house-chart/",
    ]
    chart_link_xpath: Optional[str] = (
        '//a[contains(@href, "playlists/soul-energy")]/@href'
    )
