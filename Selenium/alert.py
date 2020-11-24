from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from shutil import which

#chrome_options=Options()
#chrome_options.add_argument("--headless")

chrome_path=which("chromedriver")
browser=webdriver.Chrome(executable_path=chrome_path)#,options=chrome_options)
#browser=webdriver.Chrome()

browser.get("https://techstepacademy.com/training-ground")

buttn1=browser.find_element_by_xpath('//*[@id="b1"]').click()

alert=Alert(browser)

alert.dismiss()
