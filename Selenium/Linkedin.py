from parsel import Selector
import paramaters
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
#import panda as pd
#from request import PandaRequest as pd

#List=[]

def validate_field(field):
    if field:
        pass
    else:
        field=""
    return  field

#writer=csv.writer(open(paramaters.File_name,"wb"))
#writer.writerow(["Name" ,"Job_title","Scholl","Location","Url"])


#path=(r"C:\pythonProject1\chromedriver")
driver=webdriver.Chrome()#(path)
driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
#driver.page_source

username=driver.find_element_by_xpath('//*[@id="username"]')
username.send_keys(paramaters.user_name)
sleep(0.5)
password=driver.find_element_by_xpath('//*[@id="password"]')
password.send_keys(paramaters.password)
sleep(0.5)
sign_in=driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()
sleep(3)
#driver=webdriver.Chrome()#//*[@id="organic-div"]/form/div[3]/button


driver.get("https://www.google.com/")
sleep(2)
iframe=driver.find_element_by_xpath('//*[@id="cnsw"]/iframe')
driver.switch_to.frame(iframe)
#driver.find_element_by_xpath('//*[@id="introAgreeButton"]/span/span').click()
element=WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="introAgreeButton"]/span/span')))
element.click()
input_btn=driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
input_btn.send_keys(paramaters.search_query)
sleep(0.5)
input_btn.send_keys(Keys.RETURN)
sleep(3)

linked_link=driver.find_elements_by_xpath('//*[@id="rso"]/div/div/div/a')

linked_link=[link.get_attribute('href') for link in linked_link]#
sleep(0.5)

for link in linked_link:
    driver.get(link)
    sleep(3)

    sel = Selector(text=driver.page_source)

    try:
        name = sel.xpath('//*[@id="ember59"]/div[2]/div[2]/div[1]/ul[1]/li[1]/text()').extract_first().strip()

        #src=sel.xpath('//*[@id="react-root"]/section/main/div/div/article/div/div/div/div/a/div/divs').extract()

        job_title = sel.xpath('//*[@id="ember59"]/div[2]/div[2]/div[1]/h2/text()').extract_first().strip()

        scholl = sel.xpath('//*[@id="ember75"]/text()').extract_first().strip()

        location = sel.xpath('//*[@id="ember59"]/div[2]/div[2]/div[1]/ul[2]/li[1]/text()').extract_first().strip()
        ##
        url = driver.current_url
    except:
        pass

    name = validate_field(name)
    job_title = validate_field(job_title)
    scholl = validate_field(scholl)
    location = validate_field(location)
    url = validate_field(url)

    #print('Name:  ' + name),
    #print('Job_title:  ' + job_title),
    #print('Scholl:  ' + scholl),
    #print('Location:  ' + location),
    #print('Url:  ' + url),

    data={

        'Name:  ' + name,
        'Job_title:  ' + job_title,
        'Scholl:  ' + scholl,
        'Location:  ' + location,
        'Url:  ' + url
    }
    print(data)
    #list.append(data)

    ##writer.writerow([
    ##   name.encode("utf-8"),
    ##   job_title.encode("utf-8"),
    ##   scholl.encode("utf-8"),
    ##   location.encode("utf-8"),
    ##   url.encode("utf-8"),
    ##])

#df=pd.DataFrame(list)
#df.to_csv("linked_in.csv", index=False)


driver.quit()