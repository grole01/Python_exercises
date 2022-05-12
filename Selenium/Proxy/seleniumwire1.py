from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import seleniumwire.undetected_chromedriver as uc
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--no-sandbox')
#options.add_argument('--start-maximized')
#options.add_argument('--start-fullscreen')
options.add_argument('--single-process')
options.add_argument('--disable-dev-shm-usage')
#options.add_argument("--incognito")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("disable-infobars")
#helperSpoofer = Spoofer()
#options.add_argument('user-agent={}'.format(helperSpoofer.userAgent))

API_KEY = '2348599934a91db3ea96d44db5d8904a'

proxy_options = {
    'proxy': {
        'http': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
        'no_proxy': 'localhost,127.0.0.1'
    }
}

driver = webdriver.Chrome(ChromeDriverManager().install(),
                            options=options,seleniumwire_options=proxy_options)

driver.get('http://whatismyipaddress.com')
#driver.get("https://ifconfig.me/")

time.sleep(15)

#driver.quit()
