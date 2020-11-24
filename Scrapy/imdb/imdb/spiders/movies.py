# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MoviesSpider(CrawlSpider):
    name = 'movies'
    allowed_domains = ['imdb.com']
    #start_urls = ['https://www.imdb.com/chart/top/']

    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

    def start_requests(self,):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/',headers=
        {
            'User-Agent':self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@class="titleColumn"]/a'), callback='parse_item', follow=True, process_request='set_user_agent'),
    )

    def set_user_agent(self,request):
        request.headers['User-Agent']=self.user_agent
        return request


    def parse_item(self, response):
        yield {
            'title':response.xpath('//*[@class="title_wrapper"]/h1/text()').get(),
            'year': response.xpath('//*[@id="titleYear"]/a/text()').get(),
            'duration': response.xpath('normalize-space(//*[@datetime="PT142M"]/text())').get(),
            'genre': response.css('.subtext a:nth-child(4)::text').get(),
            'rating': response.xpath('//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()').get(),
            'movie_url': response.url,
            'user-agent':response.request.headers['User-Agent']
        }


        #item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        #return item
