import scrapy
from ..items import AmazonTutorialItem


class AmazonSpiderSpider(scrapy.Spider):
    name = 'spider'
    start_urls = ['https://www.amazon.com/s?bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&fst=as%3Aoff&qid=1593602843&rnid=1250225011&ref=lp_283155_nr_p_n_publication_date_0']

    def parse(self, response):

        items=AmazonTutorialItem()
        product_name =response.css('.a-color-base.a-text-normal').css("::text").extract()
        product_author =response.css('.sg-col-12-of-28 .a-size-base+ .a-size-base').css("::text").extract()
        product_price =response.css('.a-spacing-top-small .a-price-fraction , .a-spacing-top-small .a-price-whole').css("::text").extract()
        product_imagelink =response.css('.s-image::attr(src)').extract()

        items['product_name']=product_name
        items['product_author']=product_author
        items['product_price']=product_price
        items['product_imagelink']=product_imagelink

        yield items

        next_page=response.xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div[17]/span/div/div/ul/li[7]/a/@href').extract_first()
        if next_page:
            yield response.follow(next_page,callback=self.parse)

