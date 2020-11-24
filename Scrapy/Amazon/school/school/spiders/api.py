# -*- coding: utf-8 -*-
import scrapy
import json
from pprint import pprint


class ApiSpider(scrapy.Spider):
    name = 'api'
    #allowed_domains = ['directory.ntschools.net/api/System/GetAllSchools']
    start_urls = ['https://www.monster.com/jobs/search/pagination/q-product-manager-jobs?stpage=1'
                  '&isDynamicPage=false&isMKPagination=true&page=8&total={}'.format(i+1)for i in range(1)]

    def parse(self, response):
        results = json.loads(response.text)
        #school = resp.get("itSchoolCode")
        #pprint(resp)
        #print(response.text)
        for result in results:
            job_id=('JobID')
            next_url='https://job-openings.monster.com/v2/job/pure-json-view?jobid={}'.format (job_id)
            yield response.follow(next_url,callback=self.parse_detail,dont_filter=True)
            print()

    def parse_detail(self,response):
        detail={}
        result = json.loads(response.text)
        detail["description"]=result["jobDescription"]
        detail["job_id"] = result['JobID']
        info=result["summary"] ["info"]
        for i in info:
            i [detail["title"]]=i["text"]

        return detail

