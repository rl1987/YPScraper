# -*- coding: utf-8 -*-
import scrapy


class YellowSpider(scrapy.Spider):
    name = 'yellow'
    allowed_domains = ['yellowpages.com']
    start_urls = ['http://yellowpages.com/']

    def start_requests(self):
        search_terms = getattr(self, 'search_terms')
        geo_location_terms = getattr(self, 'geo_location_terms')
        
        start_url = 'https://www.yellowpages.com/search?search_terms=' + search_terms + '&geo_location_terms=' + geo_location_terms

        yield scrapy.Request(start_url, callback=self.parse_list)

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

        email = response.xpath('//a[@class="email-business"]/@href').get()
        if email is not None:
            email = email.replace('mailto:','')

        yield {
            'Business name' : response.xpath('//div[@class="sales-info"]/h1/text()').get(),
            'Address': response.xpath('//div[@class="contact"]/h2[@class="address"]/text()').get(),
            'Phone': response.xpath('//div[@class="contact"]/p[@class="phone"]/text()').get(),
            'Email': email,
            'Website URL' : response.xpath('//a[@class="secondary-btn website-link"]/@href').get(),
            'Yellowpages URL' : response.url,
            'Latitude' : response.xpath('//div[@id="bpp-static-map"]/@data-lat').get(),
            'Longitude' : response.xpath('//div[@id="bpp-static-map"]/@data-lng').get(),
        }
