import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url="https://codingbat.com/java"
page=requests.get(url,headers={"user-agent":"UserAgent"})

soup=BeautifulSoup(page.content,"lxml")
base_url="https://codingbat.com"

divs=soup.find_all("div", class_="summ")
#for div in divs:
    #print(base_url+div.a["href"])

links=[base_url+div.a["href"]for div in divs]
#print(links)
for link in links:
    inner_page=requests.get(link,headers={"user-agent":"UserAgent"})
    inner_soup=BeautifulSoup(inner_page.content,"lxml")
    div=inner_soup.find("div", class_="tabc")
    #for td in div.table.find_all("td"):
        #print(base_url+td.a["href"])
    question_links=[base_url+td.a["href"]for td in div.table.find_all("td")]
    for question_link in question_links:
        final_page=requests.get(question_link)
        final_soup=BeautifulSoup(final_page.content,"lxml")

        inndent_div=final_soup.find("div", class_="indent")

        problem_statement=inndent_div.table.div.string

        siblings_of_problem_statement=inndent_div.table.div.next_siblings
        #siblings_of_problem_statement=final_soup.find("body > div.tabc > div > div > table > tbody > tr > td: nth - child(1) > div")

        #for sibling in siblings_of_problem_statement:
        #    if sibling.string is not None:
        #        print(sibling)
        examples=[sibling for sibling in siblings_of_problem_statement if sibling.string is not None]

        print(problem_statement)
        for example in examples:
            print(example)

        break
    break


