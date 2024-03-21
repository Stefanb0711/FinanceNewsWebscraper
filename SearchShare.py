from wtforms.validators import DataRequired
from selenium import webdriver
from selenium.webdriver import Keys
from wtforms.fields.simple import StringField, SubmitField
from flask_bootstrap import Bootstrap5
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class SearchForShare:
    def __init__(self):
        self.investopedia_url = "https://www.investopedia.com/search"
        self.search_successful_completed = False
        self.articles = {
            "title": [],
            "content": []
        }
        self.driver = None
        self.share_name = ""

        #self.driver = webdriver.Chrome()
        #self.driver.get(self.investopedia_url)


    def search(self, form):


        self.share_name = form.share_name.data
        self.share_name = self.share_name.capitalize()

        # cookies_popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/button'))

        while not self.search_successful_completed:

            try:
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                self.driver = webdriver.Chrome(options=chrome_options)
                self.driver.get(self.investopedia_url)
                self.driver.implicitly_wait(10)


                cookies_popup = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))

                cookies_popup.click()
                cookies_popup.click()

                search_input = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="search-results__input-wrapper_1-0"]/div/input')))
                # search_input = self.driver.find_element(By.XPATH, '//*[@id="search-results__input-wrapper_1-0"]/div/input')
                # search_input = driver.find_element(By.XPATH, '//*[@id="search-results__input-wrapper_1-0"]/div/input')

                search_input.send_keys(self.share_name)
                search_input.send_keys(Keys.ENTER)

                try:
                    cookies_popup = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))
                    cookies_popup = self.driver.find_element(By.ID, 'onetrust-accept-btn-handler')
                    cookies_popup.click()
                    cookies_popup.click()
                except:
                    print("Element nicht gefunden")


                self.articles["title"] = []
                self.articles["content"] = []

                for _ in range(1, 10):
                    try:
                        self.driver.implicitly_wait(1)
                        article_title = WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, f'//*[@id="search-results__title_{_}-0"]')))

                        # article_title = driver.find_element(By.XPATH, f'//*[@id="search-results__title_{_}-0"]')
                        self.articles["title"].append(article_title.text)
                        article_title.click()
                        try:
                            key_facts = WebDriverWait(self.driver, 10).until(
                                EC.visibility_of_element_located((By.XPATH, f'//*[@id="mntl-sc-block-callout-body_1-0"]')))
                            # key_facts = driver.find_element(By.XPATH, '//*[@id="mntl-sc-block-callout-body_1-0"]')
                            self.articles['content'].append(key_facts.text)
                            self.driver.back()
                        except:
                            self.driver.back()

                    except:
                        if _ >= 4:
                            self.search_successful_completed = True


                print(self.articles)

                self.search_successful_completed = True
                self.driver.quit()

            except:
                print("Suchvorgang konnte nicht beendet werden. Warten Sie einen Moment")
                self.driver.quit()

