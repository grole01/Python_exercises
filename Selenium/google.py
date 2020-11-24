from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


#

driver=webdriver.Chrome()#(path)

driver.get("https://www.linkedin.com/in/vfigueiro/?originalSubdomain=uk")
driver.get("https://www.google.com/")
sleep(2)
iframe=driver.find_element_by_xpath('//*[@id="cnsw"]/iframe')
driver.switch_to.frame(iframe)
#driver.find_element_by_xpath('//*[@id="introAgreeButton"]/span/span').click()
element=WebDriverWait(driver, 20).until(
   EC.element_to_be_clickable((By.XPATH, '//*[@id="introAgreeButton"]/span/span')))
element.click()
input_btn=driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
input_btn.send_keys('site:uk.linkedin.com/in/ AND "python developer" AND "London" NOT "www')
input_btn.send_keys(Keys.RETURN)

linked_link=driver.find_elements_by_xpath('//*[@id="rso"]/div/div/div/a')

linked_link=[link.get_attribute('href') for link in linked_link]
#for link in linked_link:
#   print(link.get_attribute('href'))
