import scrapy
from .config import API
from scraper_api import ScraperAPIClient
client = ScraperAPIClient(API)


class ApiSpider(scrapy.Spider):
    name = 'api2'

    def start_requests(self):
        for i in range(5):
            #yield scrapy.Request(url="http://httpbin.org/ip?i="+str(i))
            yield scrapy.Request(client.scrapyGet(url='http://httpbin.org/ip?i='+str(i)),self.parse)


    def parse(self, response):
        print(response.text)
