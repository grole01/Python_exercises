import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import content


url="https://www.consumerreports.org/cro/a-to-z-index/products/index.htm"
# file_name="consumer_reports.txt"

# user_agent=UserAgent()

# page=requests.get(url#, headers=('user-agent'== user_agent))
# with open(file_name,"w") as file:
# file.write(page.content.decode('ascii', 'ignore')) if type(page.content)==bytes else file.write(page.content)

def read_file():
    file = open("consumer_reports.txt")
    data = file.read()
    file.close()
    return data


soup = BeautifulSoup(read_file(), "lxml")

all_products = soup.find_all("a", class_="products-a-z__results__item")
# print(all_products)
for product in all_products:
    print(product.string.strip()+url + product["href"])
