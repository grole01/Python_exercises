from helium import *
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

#url="https://directory.ntschools.net/#/schools"

#start_chrome("https://store.steampowered.com/search/?filter=topsellers")
driver=start_chrome("https://directory.ntschools.net/#/schools")
press(PAGE_DOWN)
html=driver.page_source
#print(driver.status_code)
print(html)
#soup=BeautifulSoup(driver.page_source,"lxml")
#sleep(5)

#links=soup.find("h1",class_="text-center")
#sleep(5)
#print(links)



#links=find_all(S('//*[@id="search-panel-container"]/div/div/ul/li/a'))
#links=find_all(S(".nav-item"))
#wait_until(ListItem,30,1)


#games=[item.web_element.text for item in links]
#print(games)

#for link in links:
#    print(link)
    #browser = start_chrome(link)

    #soup = BeautifulSoup(browser.page_source, "lxml")

kill_browser()

