# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from Demodownloader.items import DemodownloaderItem



class Mp3Spider(scrapy.Spider):
    name = 'mp3'
    #allowed_domains = ['m']
    start_urls = ['http://hcmaslov.d-real.sci-nnov.ru/public/mp3/Metallica/Albums/1996%20-%20Load/']

    def parse(self, response):
        for link in response.xpath("//following::tr[4]/td[2]/a[contains(@href, 'mp3')]"):
            loader=ItemLoader(item=DemodownloaderItem(),selector=link)
            url=response.urljoin(link.xpath(".//@href").get())
            loader.add_value("file_urls",url)
            loader.add_xpath('file_name',".//text()")
            yield loader.load_item()
