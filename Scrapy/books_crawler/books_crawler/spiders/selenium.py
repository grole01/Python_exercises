from selenium import webdriver
from time import sleep
import os

class RunChromeTest():

    def test(self):
        driverlocation=(r'C:\Users\grole\Desktop\scrapy\chromedriver.exe')
        os.environ["webdriver.chrome.driver"]=driverlocation
        driver = webdriver.Chrome(driverlocation)
        driver.get('https://google.com')

ff=RunChromeTest()
ff.test()







#sleep(5)
#driver.close()