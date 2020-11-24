# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'

    start_urls = ['https://newyork.craigslist.org/d/jobs/search/jjj']

    def parse(self, response, listing=None):
        listings = response.xpath('//li[@class="result-row"]')
        for listing in listings:
            date = listing.xpath('.//*[@class="result-date"]/@datetime').extract_first()
            link = listing.xpath('.//*[@class="result-title hdrlnk"]/@href').extract_first()
            text = listing.xpath('.//*[@class="result-title hdrlnk"]/text()').extract_first()

            yield scrapy.Request(link, callback = self.parse_listing, meta={
                "date" : date,
                "link" : link,
                "text" : text
            })

        next_page = response.xpath('//a[text()="next > "]/@href').extract_first()
        next_page_url=response.urljoin(next_page)
        if next_page_url:
            yield scrapy.Request(next_page_url, callback = self.parse)

    def parse_listing(self,response):
        date = response.meta["date"]
        link = response.meta["link"]
        text = response.meta["text"]

        compensation = response.xpath("/html/body/section/section/section/div[1]/p/span[1]/b/text()").extract_first()
        type = response.xpath("/html/body/section/section/section/div[1]/p/span[2]/b/text()").extract_first()
        image = response.xpath('//*[@id="1_image_ibhfqE63EK2"]/img/@src').extract_first()
        adress = response.xpath('//*[@id="postingbody"]/text()[2]').extract_first()

        yield {
            "date" : date,
            "link" : link,
            "text" : text,
            "compensation" : compensation,
            "type" : type,
            "image" : image,
            "adress" : adress

        }