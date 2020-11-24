from selenium import webdriver
#from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import wget
import os
import json
import lxml
from time import sleep


options=Options()

options.add_argument("--headless")

output=[]
driver=webdriver.Chrome(options=options)
driver.get("https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=riot+gear")
sleep(1)
#soup=BeautifulSoup(driver.page_source,"lxml")

driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
sleep(2)
products=driver.find_elements_by_css_selector(".J-offer-wrapper")

for i in products:
    try:
        product_name=i.find_element_by_css_selector("h4").text
    except:
        product_name=None
    try:
        price=i.find_element_by_css_selector(".elements-offer-price-normal__price").text
    except:
        price=None

    try:
        img_div=i.find_element_by_css_selector(".seb-img-switcher__imgs")
        img_url=img_div.get_attribute("data-image")
        img_url="https:" + img_url
        img_url=img_url.replace("_300x300.jpg", "")
        img_url = img_url.replace("_300x300.png", "")
        destination="images/" + img_url.split("/")[-1]
        if os.path.exists(destination) != True:
            wget.download(img_url,destination)

    except:
        img_url=None

    output_item={
        "product_name":product_name,
        "price":price,
        "img_url":img_url

    }

    output.append(output_item)
    #print(price,product_name,img_url)
json.dump(output,open("product.json", "w"),indent=2)


driver.close()

