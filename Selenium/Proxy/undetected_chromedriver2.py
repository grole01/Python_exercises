#import undetected_chromedriver.v2 as uc
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import time


if __name__ == '__main__':
    options = uc.ChromeOptions()
    py = "10.103.91.144:8088"

    #options.add_argument('--proxy-server=%s' % py)
    driver = uc.Chrome(options=options)

    driver.get("https://ifconfig.me/")
    #driver.get('http://whatismyipaddress.com')
    #driver.get('https://nowsecure.nl')
    #driver.get('https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-118.87739181518555%2C%22east%22%3A-118.76426696777344%2C%22south%22%3A34.11372323677946%2C%22north%22%3A34.17623419909594%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D')
    time.sleep(15)
    #driver.quit()

