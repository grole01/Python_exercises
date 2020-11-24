#from selenium import webdriver
import requests
from time import sleep
from bs4 import BeautifulSoup
import lxml
import wget

url="https://www.youtube.com/channel/UC8tgRQ7DOzAbn9L7zDL8mLg"

r=requests.get(url)

sleep(1)
#driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
#sleep(1)


soup=BeautifulSoup(r.text,'lxml')
sleep(1)
#path="images/"
all_video=soup.find_all("a#video-title")
print("Length of all videos", len(all_video))
for video in all_video:
    #url=video.get_attribute("href")
    url = video["href"]
    #wget.download(url, path)
    print(url)#["href"])

#driver.quit()
