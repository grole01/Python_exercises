# -*- coding: utf-8 -*-
import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains=["www.worldometers.info"]
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries=response.xpath("//td/a")
        for country in countries:
            name=country.xpath(".//text()").extract_first()
            link=country.xpath(".//@href").extract_first()

            #sabsolute_link=response.urljoin(link)

            yield response.follow(url=link,callback=self.parse_country,meta={"country_name":name})
            #yield scrapy.Request(url=absolute_link,callback=self.parse_country)

    def parse_country(self,response):
        name=response.request.meta["country_name"]
        #rows=response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        rows=response.xpath("//table[1]/tbody/tr")
        for row in rows:
            year=row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            yield{


                "country_name":name,
                "year":year,
                "population":population
                }


