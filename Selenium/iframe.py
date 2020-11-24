from selenium import webdriver

browser=webdriver.Chrome()
browser.get("https://techstepacademy.com/iframe-training")

iframe=browser.find_element_by_xpath('//*[@id="block-yui_3_17_2_1_1564338258424_5429"]/div/iframe')

browser.switch_to.frame(iframe)

select_text=browser.find_element_by_xpath('//*[@id="block-ec928cee802cf918d26c"]/div/p')
select_text.text