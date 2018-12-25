#!/bin/sh

source venv/bin/activate
rm chart.json
scrapy runspider chart_spider.py -o chart.json
python3 spotify_add.py