import scrapy

class DemoXHRPostSpider(scrapy.Spider):
    name = "xhr"

    payloud='{"productPageId":1,' \
            '"categoryPageIds":["10534","7378","10532","10469","10465","10471","7376","7364","7373","10888"]}'

    def start_requests(self):
        yield scrapy.Request(url="https://eastasiaeg.com/en/RetrieveProductRibbons",method="POST",
                             body=self.payloud,headers={'content-type':'application/json'})

    def parse(self, response):
        pass