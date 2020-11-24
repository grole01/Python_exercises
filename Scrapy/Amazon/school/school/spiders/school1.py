import scrapy
import json
#import scrapy_user_agents
from scrapy import Request


class School1Spider(scrapy.Spider):
    name = 'school1'
    #allowed_domains = 'directory.ntschools.net/#/schools'
    start_urls = ['https://directory.ntschools.net/#/schools']

    # headers = {
    #    "Accept": "application / json",
    #    "Accept - Encoding": "gzip, deflate,br",
    #    "Accept - Language": "hr - HR,hr; q = 0.9,\ca - ES;q = 0.8, ca;q = 0.7, en - US;q = 0.6, en;q = 0.5",
    #    "Cache - Control": "no - cache",
    #    "connection": "keep - alive",
    #    "Cookie": "BIGipServerdirectory.ntschools.net_443.app~directory.ntschools.net_443_pool = 360972810.20480.0000",
    #    "Host": "directory.ntschools.net",
    #    "Pragma": "no - cache",
    #    "Referer": "https: // directory.ntschools.net /",
    #    "Sec - Fetch - Dest": "empty",
    #    "Sec - Fetch - Mode": "cors",
    #    "Sec - Fetch - Site": "same - origin",
    # "User - Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 83.0 .4103 .116  Safari / 537.36",
    #    "User - Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    #    "X - Requested - With": "Fetch"
    # }
    headers = {
        'Accept': 'application/json',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept - Language': 'hr-HR,hr;q=0.9,en-US;q=0.8,en;q=0.7',
        #"Cache - Control": "no - cache",
        #'Connection': 'keep - alive',
        #'Cookie': 'BIGipServerdirectory.ntschools.net_443.app~directory.ntschools.net_443_pool=360972810.20480.0000',
        #'Host': 'directory.ntschools.net',
        #'Pragma': 'no - cache',
        'Referer': 'https://directory.ntschools.net/',
        #'Sec - Fetch - Dest': 'empty',
        'Sec - Fetch - Mode': 'cors',
        'Sec - Fetch - Site': 'same - origin',
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/84.0.4147.105 Safari/537.36',
        'X - Requested - With': 'Fetch',
    }

    def parse(self, response):
        url = "https://directory.ntschools.net/api/System/GetAllSchools"

        yield scrapy.Request(
            url,
            callback=self.parse_api,
            headers=self.headers,
            dont_filter=True)

    def parse_api(self, response):
        base_url = "https://directory.ntschools.net/api/System/GetSchool?itSchoolCode="
        #row_data = response.body
        #raw_data = response.body.decode("utf-8")
        row_data = json.loads(response.text)
        data = json.loads(row_data)
        for school in data:
            school_code = school['itSchoolCode']
            school_url = base_url+school_code
            yield scrapy.Request(school_url, callback=self.parse_school,
                                 headers=self.headers,dont_filter=True)

    def parse_school(self, response):
        row_data = response.body
        data = json.loads(row_data)

        yield {
            'Name': data['name'],
            'PhysicalAddress': data['physicalAddress']['displayAddress'],
            'PostalAddress': data['postalAddress']['displayAddress'],
            'Mail': data['mail']

        }
