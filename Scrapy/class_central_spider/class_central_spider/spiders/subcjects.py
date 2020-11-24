# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class SubcjectsSpider(scrapy.Spider):
    name = 'subjects'
    start_urls = ['https://www.classcentral.com/subjects']

    def __init__(self,subject):
        self.subject=subject

    def parse(self, response):
        if self.subject:
            subject_url=response.xpath('//*[contains(@title,"'+ self.subject +'")]/@href').extract_first()
            yield Request(response.urljoin(subject_url), callback=self.parse_subject)
        else:
            self.logger.info("Scrapy all subjects.")
            subjects=response.xpath("//*[@class='border-box align-middle color-charcoal hover-no-underline']/@href").extract()
            for subject in subjects:
                yield Request(response.urljoin(subject),callback=self.parse_subject)

    def parse_subject(self,response):
        subject_name=response.xpath("//*[@id='page-subject']/div[1]/div/header/div[1]/div[1]/div[1]/div[2]/h1/text()").extract_first()
        courses=response.xpath('//*[@class="color-charcoal block line-tight course-name"]')


        for l in courses:

            course_name=l.xpath(".//@title").extract_first()
            course_url=l.xpath(".//@href").extract_first()
            absolute_course_name=response.urljoin(course_url)
            yield{
                'subject_name':subject_name,
                'course_name':course_name,
                'absolute_course_name':absolute_course_name
            }
        next_page=response.xpath('/html/head/link[2]/@href').extract_first()
        absolute_next_page=response.urljoin(next_page)
        yield Request(absolute_next_page, callback=self.parse)

