from selenium.webdriver.common.by import By
from .BaseElement import BaseElement
from .basic_page import BasePage
from .Locater import Locator


# driver=webdriver.Chrome()

class TrainingGroundPage(BasePage):

    url="https://techstepacademy.com/training-ground"

    @property
    def Button1(self):
        locator = Locator(by=By.ID, value="b1")
        return BaseElement(self.driver,locator=locator)
