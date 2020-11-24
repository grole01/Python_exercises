from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import alert_is_present
from selenium.webdriver.support.select import Select
browser1=webdriver.Chrome()


browser1.execute_script('window.open("https://techstepacademy.com/training-ground","_blank");')
browser1.execute_script('window.open("https://www.index.hr/","_blank");')
#browser2.get("https://www.index.hr/")
