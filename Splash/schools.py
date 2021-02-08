import requests
from bs4 import BeautifulSoup
from helium import *
from selenium import webdriver
import pandas as pd
from openpyxl.workbook import Workbook
from time import sleep

url="https://directory.ntschools.net/#/schools"
reviewlist=[]

r=requests.get("http://localhost:8050/render.html", params={"url":url,"wait":5})
print(r.status_code)
soup=BeautifulSoup(r.text,"html.parser")
#schools=soup.find_all('//*[@id="search-panel-container"]/div/div/ul/li/a')
schools=soup.find_all("a",{"click.delegate":"schoolDetails(school)"})
print(len(schools))
for i in range(2):#( len(schools):
    start_chrome("https://directory.ntschools.net/#/schools")#,headless=True)
    #go_to("https://directory.ntschools.net/#/schools")
    implicit_wait_secs= 30
    press(PAGE_DOWN)

    schools=find_all(S("#search-panel-container .nav-link"))
    implicit_wait_secs= 30
    click(schools[i])
    #click()
    #for school in schools:
    #    click(school)

    #soup = BeautifulSoup(r.text, "html.parser")
    #schools = soup.find_all("a", {"click.delegate": "schoolDetails(school)"})
    #click("school")
    #url = "https://directory.ntschools.net/#/schools"
    #r=requests.get("http://localhost:8050/render.html", params={"url":url+str(schools),"wait":5})
    #school.select("a",{"click.delegate":"schoolDetails(school)"})[0]

    name=S('h1.mb-1')
    print(name)
    kill_browser()

    #name=school.text.strip()
    #
