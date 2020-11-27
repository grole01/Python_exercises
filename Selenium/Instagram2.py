from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

#options = Options()
#options.add_argument("start-maximized")
#options.add_argument("disable-infobars")
#options.add_argument("--disable-extensions")
driver = webdriver.Chrome()#(options=options)
driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
sleep(2)
driver.find_element_by_name("username").send_keys("xxxxxxxxxxxxxx")
driver.find_element_by_name("password").send_keys("xxxxxxxxxxxxxx")
driver.find_element_by_tag_name('form').submit()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button'))).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div/div[3]/button[2]'))).click()
