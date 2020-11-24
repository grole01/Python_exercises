from requests_html import HTMLSession
#from bs4 import BeautifulSoup
import pandas as pd
from time import sleep



s=HTMLSession()
drinklist=[]

def request(url):
    r=s.get(url)
    r.html.render(timeout=25, sleep=10)
    #print(r.status_code)
    return r.html.xpath('//*[@id="product-items-container"]', first=True)

def parse(products):
    links=products.absolute_links
    for link in links:
        r=s.get(link)
        name=r.html.find("div.product-detail-info-title", first=True).text
        product_subtext = r.html.find("div.product-subtext", first=True).text
        price = r.html.find("span.price", first=True).text
        try:
            rating = r.html.find("span.label-stars", first=True).text
        except:
            rating="None"
        if r.html.find("div.add-to-cart-container"):
            stock="in stock"
        else:
            stock="out of stock"

        drink={
            "name" :name,
            "product_subtext" :product_subtext,
            "price" :price,
            "rating" :rating,
            "stock" :stock,

        }

        drinklist.append(drink)

def output():
    df=pd.DataFrame(drinklist)
    df.to_csv("drinksdemo.csv")
    print("Saved to csv file")



x=17
while True:
    try:
        products = request(f"https://www.beerwulf.com/en-gb/c/beers?catalogCode=Beer_1&routeQuery=beers&page={x}")
        print(f"Getting items from page{x}")
        parse(products)
        print("Total items: ", len(drinklist))
        x=x+1
        sleep(2)
    except:
        print("No more items")
        break
output()