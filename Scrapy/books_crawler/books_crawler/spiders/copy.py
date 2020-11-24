# -*- coding: utf-8 -*-
#import os
#import glo
import scrapy#
from scrapy.http import Request
from scrapy.loader import ItemLoader
from books_crawler.items import BooksCrawlerItem

#def product_info(response,value):
    #return response.xpath('//th[text()="'+ value +'"]/following-sibling::td/text()').extract_first()



class BookSpider(scrapy.Spider):
    name = 'copy'#
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]
    #def __init__(self, category):
       #self.start_urls = [category]
    def parse(self, response):
        books = response.xpath("//h3/a/@href").extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request (absolute_url, callback=self.parse_book)
         #next_page = response.xpath('//a[text()="next"]/@href').extract_first()
        #absolute_next_page=response.urljoin(next_page)
        #yield Request(absolute_next_page)

    def parse_book(self,response):
        l = ItemLoader(item=BooksCrawlerItem(), response=response)
        title=response.css("h1::text").extract_first()
        price=response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/p[1]/text()').extract_first()
        image_urls= response.xpath('//*[@id="product_gallery"]/div/div/div/img/@src').extract_first()
        image_urls=image_urls.replace('../..','http://books.toscrape.com/')
        #rating=response.xpath('//*[contains(@class,"star-rating")]/@class').extract_first()
        #rating=rating.replace('star-rating','Three')
        #description=response.xpath('//*[@id="content_inner"]/article/p/text()').extract_first()
        #product descreption
        #UPC=product_info(response,'UPC')
        #product_type = product_info(response, 'Product Type')
        #product_without_tax = product_info(response, 'Price (excl. tax)'
	#)
        #product_with_tax = product_info(response, 'Price (incl. tax)')
        #tax = product_info(response, 'Tax')
        #availability = product_info(response, 'Availability')
        #namber_of_reviews = product_info(response, 'Number of reviews')
        l.ad_value("title", title)
        l.ad_value("price", price)
        l.ad_value("image_urls", image_urls)

        return l.load_item()

        #yield {
        #        'title': title,
        #        'price':price,
        #        'image_url':image_url,
                #'rating':rating,
                #'description':description,

                #'UPC' : UPC,
                #'product_type' : product_type,
                #'Product_without_tax' : product_without_tax,
                #'product_with_tax' : product_with_tax,
                #'tax' : tax,
                #'availability' : availability,
                #'namber_of_reviews' : namber_of_reviews

        #}

    #def close(self, reason):
        #csv_file = max(glob.iglob("*.csv"), key=os.path.getctime)
        #os.rename(csv_file, "foobar.csv")



