#from requests_html import HTMLSession
#from bs4 import BeautifulSoup
from time import sleep
from helium import*


start_chrome("https://directory.ntschools.net/#/schools",headless=True)
get_driver()
implicit_wait_secs=()

scroll_down()
#press(PAGE_DOWN)
implicit_wait_secs=()

#schools=find_all(S('//*[@id="search-panel-container"]/div/div/ul/li/a'))
schools=find_all(S("#search-panel-container .nav-link"))
#wait_until(schools.egsist)
#click(S('"a", {"click.delegate": "schoolDetails(school)"}'))

implicit_wait_secs=()
#sleep(30)
print(len(schools))
'''
for school in range(2):#range(len(schools)):#

        #click(S('//*[@id="search-panel-container"]/div/div/ul/li/a'))
        schools = find_all(S("#search-panel-container .nav-link"))
        implicit_wait_secs = 30
        #for school in schools:
        #       click(school)
        click(schools[school])

        x=S('h1.mb-1')

        print(x.web_element.text)
        kill_browser()

'''