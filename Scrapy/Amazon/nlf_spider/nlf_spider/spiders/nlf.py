import scrapy
from scrapy import Request


class NlfSpider(scrapy.Spider):
    name = 'nlf'
    start_urls = ['https://www.nfl.com/players/']

    def parse(self, response):
        player = response.css('.d3-o-list__link::attr(href)').get()
        link=response.urljoin(player)
        yield Request(link,callback=self.parse_info)


        #all_payers= response.css('.d3-o-list__link::attr(href)').getall()
        #for player in all_payers:
        #    link=response.urljoin(player)
        #    yield Requost(url=link,callback=self.parse_info)

    def parse_info(self,response):
        link_stats=response.css(".active+ li a::attr(href)").get()
        absolute_link=response.urljoin(link_stats)
        yield Request(url=absolute_link, callback=self.parse_stats,dont_filter = True)

    def parse_stats(self,response):
        link_log=response.css("li:nth-child(3) .nfl-o-cta--secondary::attr(href)").get()
        absolute_link = response.urljoin(link_log)
        #year = response.css(".nfl-t-stats__col-12:nth-child(1)::text").getall()
        yield Request(url=absolute_link, callback=self.parse_log)

    def parse_log(self,response):
        player_name=response.css('.nfl-c-player-header__title::text').getall()

        season_period = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "d3-o-section-sub-title", " " ))]')
        for period in season_period:
            period_season=period.xpath('.//text()').extract()
            for season in response.css("table"):
                weeks =season.xpath(".//tr")[1:]
                for week in weeks:
                    week_number=week.xpath(".//td[1]/text()").extract()
                    date_played = week.xpath(".//td[2]/text()").extract()
                    oponent = week.xpath(".//td[3]/text()").extract()
                    result = week.xpath(".//td[4]/text()").extract()
                    ATT = week.xpath(".//td[5]/text()").extract()
                    item ={
                        "player_name":(player_name),
                        #"year":year,
                        "period_season":period_season,
                        "week_number":(week_number),
                        "date_played":(date_played),
                        "oponent":(oponent),
                        "result":(result),
                        "ATT":(ATT)

                    }

                    yield item





