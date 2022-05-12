import time
import sys
import random
#from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import *
import re
import os
import requests
import pandas as pd
import math
from datetime import datetime
import random
import openpyxl
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver
import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from seleniumwire.undetected_chromedriver.v2 import Chrome
from multiprocessing import Process, Value
from multiprocessing import freeze_support
from time import sleep
time_delay = random.uniform(2.75634, 3.5342)


class zillow_scraper:
    FirstLine = True
    # Excel row value
    Rows = 0

    ## Defining options for chrome browser

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    ## ssl certificate error ignore
    options.add_argument("--ignore-certificate-errors")
    ## enable Selenium logging
    #caps = DesiredCapabilities.CHROME
    #caps['goog:loggingPrefs'] = {'performance': 'ALL'}



    def interceptor(request):
        '''
        params = request.params
        params["user-agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        params["accept"] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8'
        params["accept-encoding"] = 'gzip, deflate, br'
        params["accept-language"] = 'en-US,en;q=0.8'
        params["upgrade-insecure-requests"] = '1'
        #del params['Referer']  # Delete the header first
        params["Referer"] = 'https: // www.google.com'
        request.params = params
        '''
        del request.headers['Referer']  # Delete the header first
        request.headers['Referer'] = 'https: // www.google.com'

        """
        del request.headers["user-agent"]  # Delete the header first
        request.headers["user-agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        del request.headers["accept"]
        request.headers["accept"] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8'
        del request.headers["accept-encoding"]
        request.headers["accept-encoding"] = 'gzip, deflate, br'
        del request.headers["accept-language"]
        request.headers["accept-language"] = 'en-US,en;q=0.8'
        del request.headers["upgrade-insecure-requests"]
        request.headers["upgrade-insecure-requests"] = '1'
        """

    # Adding proxy
    #'''
    API_KEY = '2348599934a91db3ea96d44db5d8904a'
    #NUM_RETRIES = 2

    proxy_options = {
        'proxy': {
            'http': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
            'https': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
            'no_proxy': 'localhost,127.0.0.1'
        }
    }
    #'''
    #PROXY = '102.36.134.30:5678'
    #options.add_argument("--proxy-server=%s' % PROXY")
    #options.add_argument("--proxy-server=%s' % seleniumwire_options")
    #browser = webdriver.Chrome(executable_path="chromedriver", options=options)
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)#, seleniumwire_options=proxy_options)#,desired_capabilities=caps,)
    #browser = uc.Chrome(options=options)#,seleniumwire_options=proxy_options)  # ,desired_capabilities=caps,)
    #browser.request_interceptor = interceptor
    #MainUrl = 'https://www.zillow.com/homedetails/5239-E-Abbeyfield-St-Long-Beach-CA-90815/21203457_zpid/'

    # Excel File Name
    FileName = "ScrapedData" + "-" + str(datetime.utcnow().date()) + ".xlsx"
    #FileName = "ScrapedData" + "-" + str(datetime.today().date()) + ".xlsx"
    #FileName = "ScrapedData" + str(random.randint(1, 9789)) + "-" + str(datetime.today().date()) + ".xlsx"
    #FileName = "ScrapedData" + str(random.randint(1, 9789)) + "-" + str(datetime.today().date()) + ".csv"
    # Defining Excel Writer
    ExcelFile = pd.ExcelWriter(FileName)

    def zillow_data(self, url):

        self.browser.get(url)
        sleep(time_delay)

        # extracting phone number and owner name
        try:
            #phone_ownername = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ds-data-view"]/ul/li[3]/div[2]/div/div/div[2]/div[1]/div[3]/div/span[2]/p[1]'))).text
            phone_ownername = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@data-testid="attribution-agent"]'
                                                                                                    or '//*[@id="ds-data-view"]/ul/li[3]/div[2]/div/div/div[2]/div[1]/div[4]/div/span[2]/p[1]'))).text
            # replacing spaces with - so we can use phone no regex properly eg: Property-Owner-(949)-294-2625
            # phone_ownername = repr(phone_ownername)#.replace("-", " "))
            phone_ownername = phone_ownername.replace(" ", ",").split(",")
            print(phone_ownername)
            phone_no = phone_ownername[-1].replace("#","")
            print(phone_no)
            # phone_no = re.compile(r'\([0-9]{3}\)\s[0-9]{3}\s[0-9]{4}$').findall(phone_ownername)[0]
            # phone = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')

            # phone_no = phone.findall(phone_ownername)[1]
            # print(phone_no)
            # striping phone no from Property-Owner-(949)-294-2625 so we can get our ownername
            # phone_ownername = (phone_ownername).replace("-", " ")
            # phone1 = phone.findall(phone_ownername)
            # ownername1 = eval(phone_ownername)
            # phone_no1 = phone.findall(phone_ownername)
            # ownername = phone_ownername.strip(phone_no1)
            ownername1 = phone_ownername[0]  # .replace(",", " ").replace('"','').replace("'","")
            ownername2 = phone_ownername[1]
            ownername = ownername1 + " " + ownername2  # .split(" ")
            print(ownername)
        # if there is indexerror that means phone no number is not present only owner name present
        except IndexError:
            phone_ownername = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ds-data-view"]/ul/li[3]/div[2]/div/div/div[2]/div[1]/div[3]/div/span[2]/p[1]'))).text
            phone_no = ""
            print(phone_no)
            ownername = phone_ownername
        # if non of them are present
        except TimeoutException:
            phone_no = ""
            ownername = ""
            print(ownername)

        # extracting address as in whole eg 5239 E Abbeyfield St, Long Beach, CA 90815
        # then splitting address by comma so we will address like this ['Abbeyfield St','Long Beach','CA 90815']
        # first index will be street second index will be city and the third will be both state and zip code
        try:
            adress = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ds-chip-property-address"]/span[1]' or '//*[@id="home-details-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/h1'or'//*[@id="home-details-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/h1'or'(//h1[@id="ds-chip-property-address"]//span)[3]'or '//*[@id="home-details-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/h1'))).text
            #adress = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="home-details-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/h1/text()[1]')))

            print(adress)
            #adress = adress.split(",")
            street = adress.replace(",", "")
            print(street)
            """
            city = adress[1].strip()
            print(city)
            street = adress[0]
            print(street)
            # for state and zip code we will strip space from corners and split by space so we will get both state and zip on differnt index
            sc = adress[-1].rstrip().lstrip().split(" ")
            #state= adress[-1]
            state = sc[0]
            print(state)
            zip1 = sc[-1]
            print(zip1)
            buy_zestimate = ""
            rental_zestimate = ""
            """
            state1 = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ds-chip-property-address"]/span[2]'))).text#/text()[2]
            print(state1)
            state1 = state1.split(",")
            city = state1[0].strip()
            print(city)
            state = state1[1].strip()
            print(state)

        except IndexError:
            adress = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ds-chip-property-address"]/span[1]' or '//*[@id="home-details-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/h1'))).text
            adress = ""
            street = ""
            city = ''
            state = ""

        except:
            adress = ''
            street = ""
            city = ''
            state = ""

        # description
        try:
            description = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ds-data-view"]/ul/li[3]/div[2]/div/div/div[2]/div[1]/div[3]/div[1]/div'
                                                                                                or '//*[@class="ds-overview-section"]//[@class="Text-c11n-8-63-0__sc-aiai24-0 sc-caiLqq gbKiss jhlxJq"]'
                                                                                                or"//div[contains(@class,'Text-c11n-8-63-0__sc-aiai24-0 sc-caiLqq')]"
                                                                                                or "//div[@class='Text-c11n-8-63-0__sc-aiai24-0 sc-ehCJOs gbKiss hWUYuu']"
                                                                                                or '//*[@id="ds-data-view"]/ul/li[3]/div[2]/div/div/div[2]/div[1]/div[2]/div/div'
                                                                                                or "//div[@class='sc-iAKWXU jZFFKP']/div"))).text #.get_attribute('innerHTML')
            print(description)
        except :

            description = ""

        # Main Price
        try:
            price = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="Text-c11n-8-63-0__sc-aiai24-0 hdp__sc-b5iact-0 cfVcI fAzOKk"]/span'))).text
            #price = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ds-container"]/div[4]/div[1]/div/div[1]/div/div/span/span/span'))).text
            print(price)
        except :
            price = ""


        # for time on zillow we get 3 divs with same structure : Time on Zillow 3 days | Views 464 | Saves 9 : we will iterate them and if any of them has Time on Zillow present in
        try:
            timeonzillow = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "(//div[@class='Text-c11n-8-63-0__sc-aiai24-0 kHCdln'])[1]"or'//*[@id="ds-data-view"]/ul/li[3]/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div[2]'))).text
            print(timeonzillow)
            try:
                time_onzillow = WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="ds-data-view"]/ul/li[3]/div[2]/div/div/div[2]/div[1]/div[1]/div[1]')))
                for time in time_onzillow:
                    if "Time on Zillow" in time.text:
                        timeonzillow = time.text.replace("Time on Zillow", "")#.GetAttribute("innerHTML")
                        print(timeonzillow)
            except TimeoutException:
                timeonzillow = ""
        except TimeoutException:
            timeonzillow = ""


        # we will do same thing as above for Type too as we did for Time on Zillow
        try:
            type_zillow = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="ds-status-icon zsg-icon-for-sale"]/span'))).text
            print(type_zillow)
            for type_on in type_zillow:
                if "Type:" in type_on.text:
                    ptype = type_on.text.split("Type:")[-1]
                    print(ptype)
        except TimeoutException:
            pass

        # for zestimage and rent zestimage both html structure is same so we will find both together and will iterate if Rent Zestimate text is present that means is Rest Zestimate
        try:
            zestimate = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ds-home-values"]/div/div/div[1]/div/div/span'))).text
            print(zestimate)
            '''
            for zest in zestimate:
                if "Rent Zestimate" in zest.text:
                    rental_zestimate = zest.text.replace("Rent Zestimate®", "")
                    print(rental_zestimate)
                elif "Zestimate" in zest.text:
                    buy_zestimate = zest.text.replace("Zestimate®", "")
                    print(zestimate)
            '''
        except TimeoutException:
            zestimate =  ""
            #print(buy_zestimate)
        #print(rental_zestimate)

        try:
            rentzestimate = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ds-rental-home-values"]/div/div[1]/div/div/div/span'))).text
            print(rentzestimate)
        except TimeoutException:
            rentzestimate = ""

        # Saving the data to Excel#description #street,city,state,zip1,buy_zestimate, rental_zestimate
        #buy_zestimate,, rentzestimate,zip1,
        self.WriteDataToExcel(url,ownername,phone_no, street, city, state, description, price, timeonzillow, zestimate,rentzestimate)
    #(url,phone_no,street,city,state,zip1,ownername,description,price,timeonzillow,ptype,buy_zestimate,rental_zestimate,ptype,zip1,
    def WriteDataToExcel(self, url,ownername,phone_no, street, city, state, description, price, timeonzillow, zestimate,rentzestimate):
                          #, rentzestimate
        Data_Dict = {
            'URL': url,
            'Owner Name': ownername,
            'Phone Number': phone_no,
            'Address': street,
            'City': city,
            'State': state,
            #'Zip': zip1,
            'Description': description,
            'Price': price,
            'Time on Zillow': timeonzillow,
            #'Type': ptype,
            'Zestimate': zestimate,
            'Rent Zestimate': rentzestimate
        }

        if self.FirstLine == True:
            df = pd.DataFrame([Data_Dict])
            df.to_excel(self.ExcelFile, index=False, sheet_name='Data', header=True, startrow=self.Rows)
            self.Rows = self.ExcelFile.sheets['Data'].max_row
            self.FirstLine = False
        else:
            df = pd.DataFrame([Data_Dict])
            df.to_excel(self.ExcelFile, index=False, sheet_name='Data', header=False, startrow=self.Rows)
            self.Rows = self.ExcelFile.sheets['Data'].max_row

        self.ExcelFile.save()

    def getting_urls(self, url):
        # urls list
        PropertyURLS = []
        print("FileName : " + self.FileName)
        self.browser.get(url)

        # iterate till there is no next page
        while True:
            time.sleep(2)
            # Click on other listing button
            element_1 = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@alt='Switch to Other listings']")))
            #self.browser.execute_script("arguments[0].click();", element_1)
            # Iterate loop 9 times and press PAGEDOWN key on each iterate to get the bottom of the page we could us END button but it will not load the all the properties
            for i in range(30):
                element_1.send_keys(Keys.PAGE_DOWN)
                time.sleep(time_delay)

            time.sleep(2)
            # Getting url for all the article present in the page and then storing them in to  PropertyURLS list
            get_article = WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@class='list-card-link list-card-link-top-margin list-card-img']")))
            for article in get_article:
                print(article.get_attribute('href'))
                PropertyURLS.append(article.get_attribute("href"))
                # We are pressing ENTER key on next button and then we are checking if disabled is the mentioned in the a tag if it's mention that means its last page
            try:
                next_button = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="grid-search-results"]/div[3]/nav/ul/li[5]/a')))
                                                                                                    #"//ul[@class='PaginationList-c11n-8-37-0__sc-14rlw6v-0 hmdLoo']//li[@class='PaginationJumpItem-c11n-8-37-0__sc-18wdg2l-0 eGOQHk']//a[@title='Next page']")))

                if next_button.get_attribute('disabled') == "true":
                    break
                next_button.send_keys(Keys.ENTER)
                sleep(time_delay)
            except:
                pass


        return PropertyURLS

    #def connector(self):
    def connector(self, url):
        time_delay = random.uniform(3.05634, 3.5342)
        #UserInput = str(input("Enter Url: "))
        #print("Scraping data for url : " + str(UserInput))
        # Calling gettingurl function it will scrape all the properties url from search result
        #urls = self.getting_urls(UserInput)
        urls = self.getting_urls(url)
        # log
        print("Total Properties found : ", len(urls))
        i = 0
        for url in urls:
            i += 1
            time.sleep(time_delay)
            print("Property Scraping : " + url)
            # zillow data function will scrape mandatory fields and save it to excel
            self.zillow_data(url)
            time.sleep(5)
            # log
            print("Property Scraped : " + str(i) + " out of " + str(len(urls)) + " remaining urls : " + str(len(urls) - i))

#from multiprocessing import Process, freeze_support
#if __name__ == '__main__':
#    freeze_support()  # needed for Windows
zillow_scraper()
a = zillow_scraper()

#a.zillow_data("https://www.zillow.com/homedetails/576-E-Carlisle-Rd-Westlake-Village-CA-91361/2068546922_zpid/")
a.zillow_data("https://www.zillow.com/homedetails/1243-Landsburn-Cir-Westlake-Village-CA-91361/16490458_zpid/")
#a.zillow_data("https://www.zillow.com/homedetails/724-Valley-Dr-Thousand-Oaks-CA-91362/2075578892_zpid/")
#a.getting_urls('https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-118.87739181518555%2C%22east%22%3A-118.76426696777344%2C%22south%22%3A34.11372323677946%2C%22north%22%3A34.17623419909594%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D')
#a.connector('https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-118.87739181518555%2C%22east%22%3A-118.76426696777344%2C%22south%22%3A34.11372323677946%2C%22north%22%3A34.17623419909594%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D')

