#!/usr/bin/env bash

service apache2 start
service mongodb start
cd /app/scrapy_app && scrapyd &
python /app/manage.py runserver 0.0.0.0:8000 

tail -f /dev/null