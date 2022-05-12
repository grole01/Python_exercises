import json
import requests
from bs4 import BeautifulSoup


url = "https://www.zillow.com/homes/for_sale/house,multifamily,townhouse_type/?searchQueryState={%22pagination%22%3A{}%2C%22mapBounds%22%3A{%22west%22%3A-106.97384791227731%2C%22east%22%3A-102.82925562712106%2C%22south%22%3A39.18758562803622%2C%22north%22%3A40.241821806991595}%2C%22customRegionId%22%3A%22fcac4612c1X1-CR9xde3hldsvpa_v24ah%22%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A{%22hoa%22%3A{%22max%22%3A200}%2C%22con%22%3A{%22value%22%3Afalse}%2C%22apa%22%3A{%22value%22%3Afalse}%2C%22sch%22%3A{%22value%22%3Atrue}%2C%22ah%22%3A{%22value%22%3Atrue}%2C%22sort%22%3A{%22value%22%3A%22globalrelevanceex%22}%2C%22land%22%3A{%22value%22%3Afalse}%2C%22schu%22%3A{%22value%22%3Afalse}%2C%22manu%22%3A{%22value%22%3Afalse}%2C%22schr%22%3A{%22value%22%3Afalse}%2C%22apco%22%3A{%22value%22%3Afalse}%2C%22basf%22%3A{%22value%22%3Atrue}%2C%22schc%22%3A{%22value%22%3Afalse}%2C%22schb%22%3A{%22min%22%3A%227%22}}%2C%22isListVisible%22%3Atrue}"
#url = 'https://www.zillow.com/homedetails/1875-Kellerton-Dr-La-Puente-CA-91745/21470628_zpid/'
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")
#soup = BeautifulSoup(response, "html.parser")

data = json.loads(
    #soup.select_one("script[zmm-api-config template hide]")
    #soup.find('script', {'type': 'application/json'})
    #.contents[0]
    soup.find('script').contents[0]
    .strip("!<>-")
)

# uncomment this to print all data:
print(json.dumps(data, indent=4))
'''
for result in data["cat1"]["searchResults"]["listResults"]:
    print(
        "{:<15} {:<50} {:<15}".format(
            result["statusText"], result["address"], result["price"]
        )
    )
'''