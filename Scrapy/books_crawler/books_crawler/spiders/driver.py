from scrapy import Spider



class BooksSpider(Spider):
    name = 'driver'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']



    def parse_page(self, response):
        pass