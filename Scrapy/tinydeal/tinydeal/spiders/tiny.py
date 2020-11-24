# -*- coding: utf-8 -*-
import scrapy


class TinySpider(scrapy.Spider):
    name = 'tiny'
    allowed_domains = ['www.tinydeal.com']
    #start_urls = ['https://www.tinydeal.com/specials.html']

    def start_requests(self):
        yield scrapy.Request(url='https://www.tinydeal.com/specials.html',
                             callback=self.parse,
                             headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

                             })

    def parse(self, response):
        for product in response.xpath('//*[@class="p_box_wrapper"]'):
            yield{

                'title':response.xpath(".//a[@class='p_box_title']/text()").get(),
                'url' : response.urljoin(response.xpath(".//a[@class='p_box_title']/@href").get()),
                'discounted_price':response.xpath(".//span[@class='productSpecialPrice fl']/text()").get(),
                'original_price' : response.xpath(".//span[@class='normalprice fl']/text()").get(),
                'User-Agent':response.request.headers['User-Agent']
            }

        #next_page=response.xpath('//*[@id="pageDiv1"]/a[6]/@href').get()
        next_page=response.xpath('//*[@class="nextPage"]/@href').get()
        if next_page:
            yield scrapy.Request(next_page,
                                 callback=self.parse,
                                 headers={
                                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            }
            )

''