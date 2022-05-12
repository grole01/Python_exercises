import seleniumwire.undetected_chromedriver as uc
from seleniumwire import webdriver
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False


if __name__ == '__main__':
    API_KEY = '2348599934a91db3ea96d44db5d8904a'

    seleniumwire_options = {
            'proxy': {
                'http': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
                'https': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
    driver = uc.Chrome(options=chrome_options, seleniumwire_options=seleniumwire_options)

    driver.get('https://api.myip.com/')
    time.sleep(10)
    driver.close()