# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from downloader.items import DownloaderItem


class CourseSpider(scrapy.Spider):
    name = 'course'
    #allowed_domains = ['c']
    start_urls = ['https://cdn.coursefreedownload.com/web-scraping-with-python-x-end-to-end-data-science-project-torrent/?file=d2ViLXNjcmFwaW5nLXdpdGgtcHl0aG9uLXgtZW5kLXRvLWVuZC1kYXRhLXNjaWVuY2UtcHJvamVjdC50b3JyZW50&key=NDUwMA%3D%3D']

    def parse(self, response):
        for link in response.xpath("//a[@class='uk-button uk-button-primary uk-button-large']"):
            loader = ItemLoader(item=DownloaderItem(), selector=link)
            url = link.xpath(".//@href").get()
            loader.add_value("file_urls",url)
            #loader.add_xpath('file_name', ".//text()")
            yield loader.load_item()