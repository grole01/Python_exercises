from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

#chromeOptions=Options()
#chromeOptions.add_argument("--headless")

driver=webdriver.Chrome()#(options=chromeOptions)
#driver.get("https://www.instagram.com/")
driver.get("https://www.premierleague.com/")

players_el=driver.find_element_by_xpath('/html/body/header/div/nav/ul/li[9]/a').click()

element=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"search-input")))
coocky_acept=driver.find_element_by_xpath('/html/body/section/div/div').click()
#time.sleep(1)
#el.click()
el_search=driver.find_element_by_xpath('//*[@id="search-input"]')
#time.sleep(1)
#el_search.clear()
el_search.send_keys("wayne rooney")
driver.implicitly_wait(2)
click_search=driver.find_element_by_xpath('//*[@id="mainContent"]/div[2]/header/div/div[1]/div/div/div').click()

#el_search.send_keys(Keys.RETURN)
driver.implicitly_wait(3)
#element2=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//img[@data-player="p13017"]')))
click_wayne=driver.find_element_by_xpath('//img[@data-player="p13017"]').click()

page_source_overview=driver.page_source

from bs4 import BeautifulSoup

soup=BeautifulSoup(page_source_overview,"lxml")

title_finder=soup.find_all("span", class_="title")
#title_finder

#print(10*"-"+"These are the latest news headlines about Wayne Rooney"+10*"-"+"/n")

#for title in title_finder:
    #print(title.string)
time.sleep(1)
Wayne_stats=driver.find_element_by_xpath('//*[@id="mainContent"]/div[2]/nav/ul/li[2]/a').click()

page_source_stats=driver.page_source

soup=BeautifulSoup(page_source_stats,"lxml")

stats_finder=soup.find_all("span", class_="allStatContainer")

#print(stats_finder)
print(10*"-"+" Wayne Rooney stats "+10*"-"+"/n")
for stats in stats_finder:
    print(stats['data-stat']+" - "+stats.string)
    #print(stats.string)

