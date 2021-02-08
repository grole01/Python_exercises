import scrapy
from ..items import AmazonTutorialItem
from scraper_api import ScraperAPIClient
client = ScraperAPIClient('2348599934a91db3ea96d44db5d8904a')
result = client.get(url = 'http://httpbin.org/ip').text
print(result);
# Scrapy users can simply replace the urls in their start_urls and parse function
# Note for Scrapy, you should not use DOWNLOAD_DELAY and
# RANDOMIZE_DOWNLOAD_DELAY, these will lower your concurrency and are not
# needed with our API

class ApiSpider(scrapy.Spider):
    name = 'api3'
# ...other scrapy setup code
    start_urls =[client.scrapyGet(url = 'https://www.amazon.com/s?bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&qid=1609842840&rnid=1250225011&ref=lp_1000_nr_p_n_publication_date_0')]
    def parse(self, response):
        items = AmazonTutorialItem()
        product_name = response.xpath('//*[@class="a-size-medium a-color-base a-text-normal"]/text()').extract()
        product_author = response.css('.a-color-secondary .a-size-base.a-link-normal::text').extract()
        product_preis = response.css('.a-spacing-top-small .a-price-whole::text').extract()
        product_imagelink = response.css('.s-image::attr(src)').extract()

        items["product_name"] = product_name
        items["product_author"] = product_author
        items["product_preis"] = product_preis
        items["product_imagelink"] = product_imagelink

        yield items

                # ...your parsing logic here
        #yield scrapy.Request(client.scrapyGet(url = 'http://httpbin.org/ip'), self.parse)