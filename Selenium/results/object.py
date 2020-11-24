

class TrainingGroundPage:

    def __init__(self,driver):
        self.driver=driver
        self.url="https://techstepacademy.com/training-ground"

    def go(self):
        self.driver.get(self.url)

    def type_into_input(self,text):
        inpt=self.driver.find_element_by_xpath('//*[@id="ipt1"]')
        inpt.clear()
        inpt.send_keys(text)
        return None

    def get_input_text(self):
        inpt = self.driver.find_element_by_xpath('//*[@id="ipt1"]')
        elem_text=inpt.get_attribute('value')
        return elem_text

    def button1(self):
        buttn1=self.driver.find_element_by_xpath('//*[@id="b1"]')
        buttn1.click()
        return None


from selenium import webdriver

driver=webdriver.Chrome()

test_value= "It worked"

trng_page=TrainingGroundPage(driver=driver)

trng_page.go()
trng_page.type_into_input(test_value)
trng_page.button1()
txt_from_input=trng_page.get_input_text()
assert txt_from_input==test_value
print("Test passed")
assert trng_page.button1.text=="Button1"
driver.quit()