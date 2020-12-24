import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import pandas as pd


holiday_homes=[]

for x in range(1,3):
    url=f"https://www.holidayfrancedirect.co.uk/cottages-holidays/index.htm?board=sc&d=France&people=2&prop_type%5B0%5D=cottagegite&page={x}"

    r=requests.get(url)#+str(x))
    #print(r.status_code)
    soup=bs(r.text,"lxml")

    content=soup.find_all("div",class_="property-grid-item")


    for property in content:
        #print(property.find("div",clas_="col-content"))
        name=property.find('h2').text
        link=property.find("h2").a["href"]
        spec=property.find("p",class_="property-spec").text
        preis=property.find("div",class_="property-pricing").text

        property_info={
            "name" : name,
            "link" : link,
            "spec" : spec,
            "preis" : preis,

        }
        holiday_homes.append(property_info)
        #sleep(1)
    print("Holiday's home found:  ",len(holiday_homes))



df=pd.DataFrame(holiday_homes)
print(df.head())
df.to_excel("cotagges.xlsx")