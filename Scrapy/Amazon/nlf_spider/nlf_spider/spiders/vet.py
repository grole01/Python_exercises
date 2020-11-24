import scrapy


class VetSpider(scrapy.Spider):
    name = 'vet'

    start_urls = ['http://www.findalocalvet.com/']

    def parse(self, response):
        for sity in response.css("#SideByCity .itemresult a::attr(href)").getall():
            link=response.urljoin(sity)
            yield scrapy.Request(link,callback=self.parse_sity)

    def parse_sity(self,response):
        for adress in response.css(".org::attr(href)").getall():
            link=response.urljoin(adress)
            yield scrapy.Request(link,callback=self.parse_clinic)
        next_link=response.css("a.dataheader:contains('Next')::attr(href)").get()
        if next_link:
            absolute_next_link=response.urljoin(next_link)
            yield scrapy.Request(absolute_next_link,callback=self.parse_sity)

    def parse_clinic(self,response):
        yield {
            "Name":response.css('#MainProfile > div.Results-Header > h1::text').get(),
            "Sity": response.css('.locality::text').get(),
            "State": response.css('.region::text').get(),
            "Phone": response.css('.Phone::text').get(),
            "Link": response.url

                }
