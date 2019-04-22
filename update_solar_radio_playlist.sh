#!/bin/bash
cd /home/scrapy-to-spotify/
source venv/bin/activate
rm solar_radio.json
scrapy runspider spider/solar_radio_spider.py -o solar_radio.json
python3 spotify_add.py solar_radio.json
