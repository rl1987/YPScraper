# -*- coding: utf-8 -*-
import scrapy


class YellowSpider(scrapy.Spider):
    name = 'yellow'
    allowed_domains = ['yellowpages.com']
    start_urls = ['http://yellowpages.com/']

    def start_requests(self):
        urls = [
            'https://www.yellowpages.com/search?search_terms=Casinos&geo_location_terms=Las+Vegas%2C+NV'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        #print('parse_list')

        for company_link in response.xpath('//a[@class="business-name"]/@href').getall():
            company_url = 'https://yellowpages.com' + company_link
            yield scrapy.Request(company_url, callback=self.parse_company_page)

        next_page_link = response.xpath('//a[@class="next ajax-page"]/@href').get()
        if next_page_link is not None:
            next_page_url = 'https://yellowpages.com' + next_page_link
            yield scrapy.Request(next_page_url, callback=self.parse_list)

    def parse_company_page(self, response):
        #print('parse_company_page')
        pass
