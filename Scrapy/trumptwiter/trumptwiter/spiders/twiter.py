# -*- coding: utf-8 -*-
import scrapy
import json


class TwiterSpider(scrapy.Spider):
    name = 'twiter'
    allowed_domains = ['t']
    start_urls = ['http://d5nxcu7vtzvay.cloudfront.net/data/realdonaldtrump/2013.json']

    def parse(self, response):
        jsonresponse = json.loads(response.body)
        for tweet in jsonresponse:
            yield{
                'source' : tweet ['source'],
                'id_str':tweet ['id_str'],
                'text':tweet ['text'] }
