from selenium import webdriver

browser=webdriver.Chrome()
browser.get("https://techstepacademy.com/trial-of-the-stones")

stone_imput=browser.find_element_by_xpath('//*[@id="r1Input"]')
stone_imput.send_keys("rock")
answer_buttn=browser.find_element_by_xpath('//*[@id="r1Btn"]').click()

stone_result=browser.find_element_by_xpath('//*[@id="passwordBanner"]/h4').text
secrets_input=browser.find_element_by_xpath('//*[@id="r2Input"]')
secrets_input.send_keys(stone_result)
answer_buttn2=browser.find_element_by_xpath('//*[@id="r2Butn"]').click()

riechest_mercant_name=browser.find_element_by_xpath('//*[@id="block-05ea3afedc551e378bdc"]/div/div[3]/span/b').text

input_for_readle=browser.find_element_by_xpath('//*[@id="r3Input"]').send_keys(riechest_mercant_name)
answer_buttn3=browser.find_element_by_xpath('//*[@id="r3Butn"]').click()


check_answer_text=browser.find_element_by_xpath('//*[@id="trialCompleteBanner"]/h4')
check_answer=browser.find_element_by_xpath('//*[@id="checkButn"]').click()
assert check_answer_text.text=="Trial Complete"