from requests_html import HTMLSession
import pandas as pd
import wget

s=HTMLSession()

url="https://www.youtube.com/channel/UC8tgRQ7DOzAbn9L7zDL8mLg"
r=s.get(url)

r.html.render(timeout=15, sleep=10,keep_page=True,scrolldown=1)

videos=r.html.find("#video-title")
path="images/"
video_link=[]
for item in videos:
    link=item.absolute_links
    video={
        "title": item.text,
        "link":link
        }
    #print(video)
    video_link.append(video)
#wget.download(link,path )
df=pd.DataFrame(video_link)
print(df)