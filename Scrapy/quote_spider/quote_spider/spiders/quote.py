# -*- coding: utf-8 -*-
import scrapy
import os
import csv
import glob
from openpyxl import Workbook

class QuoteSpider(scrapy.Spider):
    name = 'quote'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        h1=response.xpath("//h1/a/text()").extract_first()
        tags=response.xpath('//*[@class="tag-item"]/a/text()').extract()

        yield {"h1": h1, "tags": tags}

    def close(self,reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)

        wb=Workbook()
        ws=wb.active

        with open(csv_file,"r")as f:
            for row in csv.reader(f):
                ws.append (row)

        wb.save(csv_file.replace("*.csv","")+".xlsx")


