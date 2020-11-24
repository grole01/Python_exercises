import requests
from bs4 import BeautifulSoup
import lxml
from xlsxwriter import Workbook
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import shutil
#import ipython
#import html5lib


class App:

    def __init__(self, username='adujmic1@gmail.com', password="Dujmic18092004", target_username="dataminer2060",
                 path=r"C:\Users\Korisnik\Desktop\Slike",options = Options()):#,#webdriwerwait=WebDriverWait()):

        self.username = username
        self.password = password
        self.target_username = target_username
        self.path = path
        self.options=options
        self.options.add_argument("--disable-notifications")
        #self.options.add_argument('start-maximized')
        #self.options.add_argument("--headless")
        #self.webdriverait=webdriwerwait#
        self.driver = webdriver.Chrome(options=options)
        self.error=False
        self.main_url = "https://www.instagram.com/"
        self.all_images=[]
        self.driver.get(self.main_url)
        sleep(3)
        self.close_coocky()
        self.login()
        if self.error is False:
            self.close_popup()
            self.message()
            self.open_target_profile()
        if self.error is False:
            self.scroll_down()

        if self.error is False:
            if not os.path.exists(path):
                os.mkdir(path)
            self.downloading_images()



        sleep(6)
        self.driver.quit()

    def write_caption_to_exel_file(self,images,caption_path):
        print("writing to exel")
        workbook=Workbook(os.path.join(caption_path,"captions.xslx"))
        worksheet=workbook.add_worksheet()
        row=0
        worksheet.write(row,0,"Image name")
        worksheet.write(row,1,"Caption")
        row+=1
        for index,image in enumerate(images):
            file_name = "image_" + str(index) + ".jpg"

            try:
                caption=image["alt"]
            except KeyError:
                caption="No captions exists"
            worksheet.write(row, 0, file_name)
            worksheet.write(row, 1, caption)
            row += 1
        workbook.close()


    def downloading_captions(self,images):
        captions_folder_path=os.path.join(self.path,"captions")
        if not os.path.exists(captions_folder_path):
            os.mkdir(captions_folder_path)
        self.write_caption_to_exel_file(images,captions_folder_path)
        for index,image in enumerate(images):
            try:
                caption=image["alt"]
            except KeyError:
                caption="No captions exists"
            file_name="captions_"+str(index)+".txt"
            file_path=os.path.join(captions_folder_path,file_name)
            link=image["src"]
            with open(file_path,"wb")as f:
                f.write(str("Link:" +str(link) + "\n" + "caption: " + caption).encode())



    def downloading_images(self):

        self.all_images = set(self.all_images)
        self.downloading_captions(self.all_images)
        print("Length of all images", len(self.all_images))
        #for image in all_img:
        #    image["src"]
        #    url = image["src"]
        #    self.all_images.append(url)
        #    link=set(self.all_images)
            #print(len(link))


        #print(len(set(self.all_images)))
        #print(set(self.all_images))

        for index,image in enumerate(self.all_images):
            file_name="image_"+str(index)+".jpg"
            image_path=os.path.join(self.path, file_name)
            image["src"]
            link = image["src"]
            #self.all_images.append(url)
            #link=set(self.all_images)
            print("Downloading image", index)

            response=requests.get(link,stream=True)
            try:
                with open(image_path,"wb")as file:
                    shutil.copyfileobj(response.raw, file)
            except Exception as e:
                    print(e)#
                    print("Could not download image number", index )
                    print("image link -->",link)

    def scroll_down(self):
        try:
            nb_of_posts=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span')
            nb_of_posts=str(nb_of_posts.text).replace(",","")
            print(nb_of_posts)
    #
            self.nb_of_posts=int(nb_of_posts)
            if self.nb_of_posts > 12:
                nb_of_scrols=int(self.nb_of_posts/12)
                try:
                    for value in range(nb_of_scrols):
                        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                        sleep(2)
                        soup = BeautifulSoup(self.driver.page_source, 'lxml')
                        for image in soup.find_all("img", {"class": "FFVAD"}):
                            self.all_images.append(image)


                except Exception as e:

                    self.error = True
                    print("Some error occurred weil try scrolling down ")
                    print("e")
                    sleep(5)
        except Exception:
            print("Could not find nb_of_post while trying scrolling down")
            self.error = True

    def close_coocky(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[2]/button[1]'))).click()

        except Exception:
            pass

    def login(self,):
        try:
            #user_name_input = self.driver.find_element_by_xpath('//[@id="loginForm"]/div/div[1]/div/label/input')
            user_name_input = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
            try:
                user_name_input.send_keys(self.username)
                password_input = self.driver.find_element_by_name('password')
                password_input.send_keys(self.password)#
                password_input.submit()
            except Exception:
                print("Some exception occurred weil try to find username or password field")
                self.error = True
        except Exception as e:
            self.error = True
            print("unable to find login button")
            pass


    def open_target_profile(self):
        try:
            search_bar=WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')))
            #search_bar=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').click()

            search_bar.send_keys(self.target_username)
            target_profile_url=(self.main_url+self.target_username+"/")
            self.driver.get(target_profile_url)
        except Exception:
            print("Could not find search bar")
            self.error = True

        sleep(3)

    def close_popup(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button'))).click()

        except Exception:
            pass

    def message(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[4]/div/div/div/div[3]/button[2]'))).click()

        except Exception:
            pass

if __name__ == '__main__':
        app = App()

# soup=BeautifulSoup(driver.page_source,"lxml")

# print(soup.prettify())

# search_field=driver.find_element_by_xpath('//*[@id="realbox"]')
# pop_up=driver.find_element_by_xpath('//*[@id="introAgreeButton"]/span/span')
# driver.switch_to(pop_up)
# pop_up.click()
# search_field.send_keys("how to learn webscraping")
# search_field.submit()
# time.sleep(3)

# driver.close()
