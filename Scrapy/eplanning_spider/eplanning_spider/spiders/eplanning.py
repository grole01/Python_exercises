    # -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest

class EplanningSpider(scrapy.Spider):
    name = 'eplanning'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://www.eplanning.ie/']

    def parse(self, response):
        urls=response.xpath('//a/@href').extract()
        for url in urls:
            if '#' == url:
                pass
            else:
                yield Request(url,callback=self.parse_application)

    def parse_application(self,response):

        app_url =response.xpath('/html/body/div[2]/div/div/div[2]/div[1]/a/@href').extract_first()
        yield Request(response.urljoin(app_url), callback=self.parse_form)

    def parse_form(self,response):
        yield FormRequest.from_response(response,
                                        formdata={
                                            "RdoTimeLimit": "42"},
                                            dont_filter=True,
                                            formxpath='(//*[@id="listing-search"])',
                                            callback=(self.parse_pages)
                                        )
    def parse_pages(self,response):
        application_urls=response.xpath("//td/a/@href").extract()
        for url in application_urls:
            url=response.urljoin(url)
            yield Request(url,callback=self.parse_items)

        next_page_url=response.xpath('/html/body/div[2]/div/div[2]/ul/li[12]/a/@href').extract_first()
        absolute_next_page_url=response.urljoin(next_page_url)
        yield Request(absolute_next_page_url,callback=self.parse_pages)

    def parse_items(self,response):
        #pass
        agent_btn = response.xpath('//*[@value="Agents"]/@style').extract_first()
        if 'display: inline;  visibility: visible;' in agent_btn:
            name=response.xpath('//tr[th="Name :"]/td/text()').extract_first()
            address1=response.xpath('//tr[th="Address :"]/td/text()').extract()
            address2=response.xpath('//tr[th="Address :"]/following-sibling::tr/td/text()').extract()[:2]

            address = address1 + address2
            mail=response.xpath('//tr[th="e-mail :"]/td/a/text()').extract_first()

            url = response.url

            yield  {
                'name' : name,
                'address' : address,
                'mail' : mail,
                'url' : url

            }



        else:
            self.logger.info('Agent button not found on page')




