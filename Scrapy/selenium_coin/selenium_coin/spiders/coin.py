# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from shutil import which


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = ['https://www.livecoin.net/en']


    def __init__(self):
        chrome_options=Options()
        chrome_options.add_argument("--headless")

        chrome_path=which("chromedriver")
        driver=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)

        driver.get("https://www.livecoin.net/en")

        LTC=driver.find_element_by_xpath('//*[@id="marketOverviewContainer"]/section/div/article/div/div[1]/div[5]')
        LTC.click()

        self.html=driver.page_source
        driver.close()


    def parse(self, response):
        res=Selector(text=self.html)
        for currency in res.xpath('//*[contains(@class,"ReactVirtualized__Table__row tableRow___3EtiS")]'):
            yield {
                'currency_pair':currency.xpath(".//div[1]/div/text()").get(),
                'volume(24)': currency.xpath(".//div[2]/span/text()").get()
                }
