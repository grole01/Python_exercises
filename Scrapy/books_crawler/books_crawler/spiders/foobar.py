# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from books_crawler.items import BooksCrawlerItem

class FoobarSpider(scrapy.Spider):

    name = 'foobar'
    allowed_domains = ["books.toscrape.com"]
    start_urls = ['http://books.toscrape.com/']


    def parse(self, response):
        books = response.xpath("//h3/a/@href").extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback = self.parse_book)

        #next_page = response.xpath('//a[text()="next"]/@href').extract_first()
        #absolute_next_page=response.urljoin(next_page)
        #yield Request(absolute_next_page)

    def parse_book(self, response):
        #l = ItemLoader(item=BooksCrawlerItem(), response=response)
        title = response.css("h1::text").extract_first()
        price = response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/p[1]/text()').extract_first()
        image_urls = response.xpath('//*[@id="product_gallery"]/div/div/div/img/@src').extract_first()
        image_urls = image_urls.replace('../..','http://books.toscrape.com/')


        #l.ad_value("title", title)
        #l.ad_value("price", price)
        #l.ad_value("image_urls", image_urls)

        #return l.load_item()
        yield   {
                'title': title,
                'price': price,
                'image_urls': image_urls}