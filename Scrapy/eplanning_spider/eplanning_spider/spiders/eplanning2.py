   # -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest

class EplanningSpider(scrapy.Spider):
    name = 'eplanning2'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://www.eplanning.ie/']

    def parse(self, response):
        urls=response.xpath("//a/@href").extract()
        for url in urls:
            if url =='#':
                pass
            else:
                yield Request(url,callback=self.parse_application)

    def parse_application(self,response):
        app_url= response.css("div.container.body-content:nth-child(3) div.container:nth-child(3) div.row div.col-xs-6:nth-child(2) div:nth-child(4) > a:nth-child(2)::attr(href)").get()
        yield Request(response.urljoin(app_url),callback=self.parse_form)

    def parse_form(self,response):
        yield FormRequest.from_response(response, formdata={"RdoTimeLimit": "42"},
                                        dont_filter=True,
                                        formxpath="(//div[@class='container body-content']//form)",
                                        callback=self.parse_page)

    def parse_page(self,response):
        #url_numbers=response.xpath("/html/body/div[2]/div/table/tbody/tr/td/a/@href").extract()
        url_numbers=response.xpath("//td/a/@href").extract()
        for url in url_numbers:
            absolute_url=response.urljoin(url)
            yield Request(absolute_url,callback=self.parse_items)

        next_page=response.xpath("//li[@class='PagedList-skipToNext']//a[contains(text(),'»')]/@href").get()
        if next_page:
            yield response.follow(next_page,callback=self.parse_page)

    def parse_items(self,response):
        agent_btn=response.xpath('//*[@class="btn btn-primary"]/@style').extract_first()
        if 'display: inline;  visibility: visible;' in agent_btn:
            Name=response.xpath("//tr[th='Name :']/td/text()").extract()

            address1=response.xpath("//tr[th='Address :']/td/text()").extract()
            address2=response.xpath("//tr[th='Address :']/following-sibling::tr/td/text()").extract()[:3]
            Address = address1 + address2
            Phone = response.xpath("//tr[th='Phone :']/td/text()").extract()
            Email = response.xpath("//tr[th='e-mail :']/td/text()").extract()
            link=response.url

            yield {
                "Name" : Name,
                "Address" : Address,
                "Phone" : Phone,
                "Email" : Email,
                "link" : link

            }

        else:
            self.logger.info("Agent button not found on the page")
