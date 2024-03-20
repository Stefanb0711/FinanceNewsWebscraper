from wtforms.validators import DataRequired
from selenium import webdriver
from selenium.webdriver import Keys
from wtforms.fields.simple import StringField, SubmitField
from flask_bootstrap import Bootstrap5
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchForShare:
    def __init__(self):
        self.investopedia_url = "https://www.investopedia.com/search"
        self.search_successful_completed = False
        self.articles = {
            "title": [],
            "content": []
        }

        self.driver = webdriver.Chrome()


    def search(self, form):
        self.driver.get(self.investopedia_url)

        share_name = form.share_name.data


        self.driver.implicitly_wait(10)
        # cookies_popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/button'))

        cookies_popup = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))

        cookies_popup.click()
        cookies_popup.click()

        search_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="search-results__input-wrapper_1-0"]/div/input')))
        #search_input = self.driver.find_element(By.XPATH, '//*[@id="search-results__input-wrapper_1-0"]/div/input')
        # search_input = driver.find_element(By.XPATH, '//*[@id="search-results__input-wrapper_1-0"]/div/input')

        search_input.send_keys(share_name)
        search_input.send_keys(Keys.ENTER)

        cookies_popup = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))
        cookies_popup = self.driver.find_element(By.ID, 'onetrust-accept-btn-handler')

        cookies_popup.click()

        self.articles["title"] = []
        self.articles["content"] = []

        for _ in range(1, 10):
            article_title = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f'//*[@id="search-results__title_{_}-0"]')))

            # article_title = driver.find_element(By.XPATH, f'//*[@id="search-results__title_{_}-0"]')
            self.articles["title"].append(article_title.text)
            article_title.click()

            key_facts = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f'//*[@id="mntl-sc-block-callout-body_1-0"]')))
            # key_facts = driver.find_element(By.XPATH, '//*[@id="mntl-sc-block-callout-body_1-0"]')
            self.articles['content'].append(key_facts.text)
            self.driver.back()

        print(self.articles)

        self.search_successful_completed = True
