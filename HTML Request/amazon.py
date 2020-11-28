from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import argparse

my_parser=argparse.ArgumentParser(description="Return Amazon Deals")
my_parser.add_argument("searchterm",metavar="searchterm",type=str,help="The item to be searched for. Use + for spaces.")
args=my_parser.parse_args()
searchterm=args.searchterm

s=HTMLSession()

dealslist=[]


url=f"https://www.amazon.co.uk/s?k={searchterm}&i=black-friday"

def getdata(url):
    r=s.get(url)
    r.html.render(timeout=20,sleep=2)
    soup=BeautifulSoup(r.html.html,"html.parser")
    return soup

def getdeals(soup):
    products=soup.find_all('div',{'data-component-type':'s-search-result'})
    #print(products)
    for item in products:
        #title = item.find("a",{"class":"a-link-normal a-text-normal"}).text.strip()
        short_title = item.find("a",{"class":"a-link-normal a-text-normal"}).text.strip()[:25]
        link=item.find("a",{"class":"a-link-normal a-text-normal"})["href"]
        try:
            saleprice=float(item.find_all("span",class_="a-offscreen")[0].text.replace("£","").replace(",","").strip())
            oldprice = float(item.find_all("span",class_="a-offscreen")[1].text.replace("£","").replace(",","").strip())
        except:
            saleprice=None
            oldprice = None
        try:
            reviews=item.find("span",class_="a-size-base").text.strip()
        except:
            reviews=0

        saleitem={

                #"title" :title,
                "short_title" :short_title,
                "link" :link,
                "saleprice" :saleprice,
                "oldprice" :oldprice,
                "reviews" :reviews
        }
        dealslist.append(saleitem)
    return

def getnextpage(soup):
    pages=soup.find("ul",{"class":"a-pagination"})
    if not pages.find("li",class_="a-disabled a-last"):
        url="https://www.amazon.co.uk" + str(pages.find("li",class_="a-last").find("a")["href"])
        return url
    else:
        return

while True:
    soup=getdata(url)
    getdeals(soup)
    url=getnextpage(soup)
    if not url:
        break
    else:
        print(url)
        print(len(dealslist))

df=pd.DataFrame(dealslist)
df["percentoff"]=100-((df.saleprice/df.oldprice)*100)
df=df.sort_values(by=["percentoff"],ascending=False)
df.to_csv(searchterm + "-amazon.csv", index=False)
print("fin")
s.close()