"""Class to implement Starpoint Radio UK Soul Chart Breakers Scrapy spider."""
from .starpoint_uk_soul_chart_spider import StarpointUKSoulChartSpider


class StarpointUKSoulChartBreakersSpider(
    StarpointUKSoulChartSpider
):
    """Class to implement Starpoint Radio UK Soul Chart Scrapy Breakers spider."""
    name = "StarpointUKSoulChartBreakersSpider"
    start_urls = [
        "http://uksoulchart.com/show_chart_breakers.php",
    ]
    REMOVE_TEXT_BETWEEN_PARENTHESES = True
