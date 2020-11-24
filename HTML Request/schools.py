#from requests_html import HTMLSession
import pandas as pd
from time import sleep
from requests_html import AsyncHTMLSession
asession = AsyncHTMLSession()

#url="https://directory.ntschools.net/#/schools"
r =await asession.get("https://directory.ntschools.net/#/schools")

#s =HTMLSession()
#r=s.get(url)
r.html.arender(scrolldown=5,timeout=25, sleep=10)
#print(r.status_code)
schools=r.html.xpath('//*[@id="search-panel-container"]/div/div/ul/li/a')
print(schools.absolute_links)
#links=schools.html.absolute_links
#for link in schools:
#    r=s.get(link)
#    print(link)