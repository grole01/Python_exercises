from requests_html import HTMLSession

url="https://news.google.com/topstories?hl=en-GB&gl=GB&ceid=GB:en"

s=HTMLSession()
r=s.get(url)

r.html.render(timeout=20,sleep=3,scrolldown=0)

articles=r.html.find("article")


news_items=[]
for item in articles:
    try:
        news_list=item.find("h3",first=True)
        news_articl={
            "title":news_list.text,
            "link":news_list.absolute_links}
        news_items.append(news_articl)
    except:
        pass

print(news_items[0])
