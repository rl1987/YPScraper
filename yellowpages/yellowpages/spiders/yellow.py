# -*- coding: utf-8 -*-
import scrapy


class YellowSpider(scrapy.Spider):
    name = 'yellow'
    allowed_domains = ['yellowpages.com']
    start_urls = ['http://yellowpages.com/']

    def parse(self, response):
        pass
