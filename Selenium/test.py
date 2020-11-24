from selenium import webdriver
from shutil import which

from pages.TrainingGroundPage import TrainingGroundPage
from pages.Trial_page import TrialPage

#chrome_path=which("chromedriver")
driver=webdriver.Chrome()#(executable_path=chrome_path)


trial_page=TrialPage(driver=driver)
trial_page.go()
trial_page.stone_input.input_text("rock")
trial_page.stone_button.click()

#input()


trng_page= TrainingGroundPage(driver=driver)
trng_page.go()

trng_page.Button1.click()
#input()
driver.quit()

