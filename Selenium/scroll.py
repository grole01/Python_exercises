from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

driver =webdriver.Chrome()
driver.get("https://instagram.com/celmirashop/")


semua_url_lengkap = []
semua_url_post = []
nomor=1
for i in range():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(nomor)
    nomor+=1
    #mendapatkan list tiap cards update status
    article = driver.find_element_by_tag_name("article")
    list_cards = article.find_elements_by_tag_name("a")

    for item in list_cards:

        url_lengkap=item.get_attribute("href")
        semua_url_lengkap.append(url_lengkap)

        segmen = url_lengkap.rsplit('/', 2)
        semua_url_post.append(segmen[1])


print(len(semua_url_post))
print(semua_url_post)