# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,MapCompose
import os


class DemodownloaderItem(scrapy.Item):

    def remove_extension(value):
        return os.path.split.text(value)[0]


    # define the fields for your item here like:
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_name = scrapy.Field(

        input_processors=MapCompose(remove_extension),
        output_processors=TakeFirst()
    )
