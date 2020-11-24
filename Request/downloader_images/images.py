import requests
from bs4 import BeautifulSoup
import os

url="https://hr.airbnb.com/s/Ljubljana--Slovenia/homes?place_id=ChIJ0YaYlvUxZUcRIOw_ghz4AAQ&checkin=2020-11-15&checkout=2020-11-25&adults=2&children=0&landing_page_section=MARQUEE"

def img_donwload(url,folder):
    try:
        os.mkdir(os.path.join(os.getcwd(),folder))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(),folder))
    r =requests.get(url)
    soup=BeautifulSoup(r.text,"lxml")

    images=soup.find_all("img")
    for image in images:
        name=image["alt"]
        link=image["src"]
        with open(name.replace(" ","-").replace("/","").replace("*","-").replace("&","-")+".jpg","wb") as f:
            im=requests.get(link)
            f.write(im.content)
            print("Writing: ",name)

img_donwload(url,"Ljubljana")