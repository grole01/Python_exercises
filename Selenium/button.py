from selenium import webdriver
from shutil import which

chrome_path = which("chromedriver")

driver = webdriver.Chrome(executable_path=chrome_path)#"./chromedriver.exe")

driver.get("https://techstepacademy.com/training-ground")

input2 =driver.find_element_by_css_selector("#ipt2")
buttn4 =driver.find_element_by_xpath('//*[@id="b4"]')

input2.send_keys("test_text")
buttn4.click()
