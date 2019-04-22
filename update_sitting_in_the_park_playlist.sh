#!/bin/bash
cd /home/spotify-solar-radio-chart/
source venv/bin/activate
rm sitting_in_the_park.json
python3 spider/sitting_in_the_park_spider.py sitting_in_the_park.json
python3 spotify_add.py sitting_in_the_park.json
