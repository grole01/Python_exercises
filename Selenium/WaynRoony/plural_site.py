from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

#chromeOptions=Options()
#chromeOptions.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install())#, options=options)
#driver.get("https://www.instagram.com/")
driver.get("https://www.premierleague.com/")

#coocky_acept=driver.find_element_by_xpath('//*[@class="_2hTJ5th4dIYlveipSEMYHH BfdVlAo_cgSVjDUegen0F js-accept-all-close"]').click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
'//*[@class="_2hTJ5th4dIYlveipSEMYHH BfdVlAo_cgSVjDUegen0F js-accept-all-close"]'))).click()

players_el=driver.find_element_by_xpath('//*[@id="mainNav"]/div[2]/div/div').click()

#element=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"search-input")))

#time.sleep(1)
#el.click()
el_search=driver.find_element_by_xpath('//*[@id="searchPremierLeagueInput"]')
time.sleep(1)
#el_search.clear()
el_search.send_keys("Harry Kane")
driver.implicitly_wait(2)
click_search=driver.find_element_by_xpath('//*[@id="searchPremierLeagueInput"]').click()

el_search.send_keys(Keys.RETURN)
driver.implicitly_wait(3)
#element2=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//img[@data-player="p13017"]')))
#click_wayne=driver.find_element_by_xpath('//*[@id="searchPremierLeagueInput"]').click()

page_source_overview=driver.page_source

from bs4 import BeautifulSoup

soup=BeautifulSoup(page_source_overview,"lxml")

title_finder=soup.find_all("span", class_="title")
#title_finder

print(10*"-"+"These are the latest news headlines about Harry Kane"+10*"-"+"/n")

for title in title_finder:
    print(title.string)
time.sleep(1)

player_stats=driver.find_element_by_xpath('/html/body/footer/div[2]/div/div[3]/ul/li[2]/a/span').click()
time.sleep(1)
Harry_Kane=driver.find_element_by_xpath('//*[@id="mainContent"]/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[2]/a/strong').click()
time.sleep(1)
Harry_Kane_stats=driver.find_element_by_xpath('//*[@id="mainContent"]/div[2]/nav/ul/li[2]/a').click()
time.sleep(1)

page_source_stats=driver.page_source

soup=BeautifulSoup(page_source_stats,"lxml")

stats_finder=soup.find_all("span", class_="allStatContainer")

#print(stats_finder)
print(10*"-"+" Wayne Rooney stats "+10*"-"+"/n")
for stats in stats_finder:
    print(stats['data-stat']+" - "+stats.string)
    print(stats.string)

driver.close()