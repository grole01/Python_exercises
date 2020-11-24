import requests
from bs4 import BeautifulSoup
import csv

def get_page(url):
    response=requests.get(url)
    if not response.ok:
        print("Server responded; ",response.status_code)
    else:
        soup=BeautifulSoup(response.text,"lxml")
    return soup

def get_detail_data(soup):
    try:
        title=soup.find("h1",id="itemTitle").text.replace("\xa0","")
    except:
        title= None
    try:
        try:
            price = soup.find("span",id="prcIsum").text
        #price=soup.find("span", class_="ITALIC").text
        except:
            price = soup.find("span",class_="notranslate").text

    except:
        price=None


    try:
        items_sold=soup.find("a",class_="vi-txt-underline").text.split(" ")[0]
    except:
        items_sold=None

    data={
        "title":title,
        "price":price,
        "items_sold":items_sold
    }
    return data


def get_index_data(soup):
    try:
        links=soup.find_all("a",class_="s-item__link")
    except:
        links=[]
    urls=[item.get("href")for item in links]

    return urls

def write_csv(data,url):

    with open("output.csv","a",encoding="utf-8") as csvfile:
        writer=csv.writer(csvfile)
        row=[data["title"],data["price"],data["items_sold"],url]
        writer.writerow(row)

def main():
    url="https://www.ebay.co.uk/sch/i.html?_nkw=mans+watch&_pgn=1"

    products=get_index_data(get_page(url))

    for link in products:
        data=get_detail_data(get_page(link))
        write_csv(data,link)
        print(data,link)

if __name__=="__main__":
    main()

