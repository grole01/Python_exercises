from selenium.webdriver.common.by import By
from .BaseElement import BaseElement
from pages.basic_page import BasePage
from .Locater import Locator

class TrialPage(BasePage):
    url = "https://techstepacademy.com/trial-of-the-stones"

    @property
    def stone_input(self):
        locator = Locator(By.ID, "r1Input")
        return BaseElement(self.driver,
                           locator=locator)

    @property
    def stone_button(self):
        locator = Locator(By.ID, "r1Btn")
        return BaseElement(self.driver,
                           locator=locator)

    @property
    def secret_input(self):
        locator = Lokator(By.ID, "r2Input")
        return BaseElement(self.driver,
                           locator=locator)

    @property
    def secret_button(self):
        locator = Locator(By.ID, "r2Butn")
        return BaseElement(self.driver,
                           locator=locator)
