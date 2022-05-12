from selenium import webdriver
import time
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--proxy-server=%s' % hostname + ":" + port)
chrome_options.add_argument('--proxy-server=%s' % '108.165.233.66')
driver = webdriver.Chrome(chrome_options=chrome_options)

#driver.get('http://whatismyipaddress.com')
driver.get("https://ifconfig.me/")
time.sleep(10)
driver.quit()