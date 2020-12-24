from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

#driver = webdriver.Chrome(ChromeDriverManager().install())

url="https://directory.ntschools.net/#/schools"

browser=webdriver.Chrome()
browser.get(url)
sleep(1)

browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
sleep(2)

links=browser.find_elements_by_xpath('//*[@id="search-panel-container"]/div/div/ul/li/a')
print("Number of schools: ",len(links))

results=[]
for i in range(2):#len(links)):
    links =WebDriverWait(browser, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="search-panel-container"]/div/div/ul/li/a')))
    links[i].click()

    sleep(2)
    #soup = BeautifulSoup(browser.page_source, "html.parser")
    details={
        "Name":browser.find_element_by_xpath('//*[@id="main-content"]/div/div[1]/div/div/div/h1').text,
        "Physical_Address":browser.find_element_by_xpath('//*[@id="main-content"]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]').text,
        "Postal_Address":browser.find_element_by_xpath('//*[@id="main-content"]/div/div[2]/div/div[1]/div[2]/div[2]/div[2]').text,
        "Phone" : browser.find_element_by_xpath('//*[@id="main-content"]/div/div[2]/div/div[1]/div[2]/div[3]/div[1]/div/div[2]/a').text
        }
    results.append(details)
    #print(results)
    browser.back()
df=pd.DataFrame(results)
print(df)

browser.quit()

with open("schools_data.csv","w",newline="",encoding="utf-8")as f:
    writer=csv.DictWriter(f,fieldnames=["Name","Physical_Address","Postal_Address","Phone"])
    writer.writeheader()
    writer.writerows(results)