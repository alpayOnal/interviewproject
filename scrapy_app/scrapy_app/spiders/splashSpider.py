# -*- coding: utf-8 -*-
import scrapy
from main.models import * 
from scrapy_splash import SplashRequest


class SplashspiderSpider(scrapy.Spider):
    name = 'splashSpider'

    def start_requests(self):
		scrapyItems = ScrapyItem.objects
		for item in scrapyItems:
			for url in item.data:
				yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        pass