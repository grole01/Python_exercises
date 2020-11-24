from helium import *
from bs4 import BeautifulSoup

url="http://quotes.toscrape.com/js/"

browser=start_chrome(url)#,headless=True)

soup=BeautifulSoup(browser.page_source,"html.parser")

quotes=soup.find_all("div",{"class":"quote"})

for quote in quotes:
    print(quote.find("span",{"class":"text"}).text)

