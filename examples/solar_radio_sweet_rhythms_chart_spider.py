"""Class to implement Solar Radio Sweet Rhythms Chart Scrapy spider."""

from typing import List

from examples.solar_radio_chart_spider import SolarRadioChartSpider


class SolarRadioSweetRhythmsChartSpider(SolarRadioChartSpider):
    """Class to implement Solar Radio Sweet Rhythms Chart Scrapy spider."""
    name: str = "SolarRadioSweetRhythmsChartSpider"
    start_urls: List[str] = [
        "http://solarradio.com/sweet-rhythms-chart-2/",
    ]
