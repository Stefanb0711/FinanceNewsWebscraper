import time

from flask import Flask, render_template, request, redirect, url_for, flash

from flask_wtf import FlaskForm
from selenium.webdriver.common.by import By
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from selenium import webdriver
from selenium.webdriver import Keys
from wtforms.fields.simple import StringField, SubmitField
from flask_bootstrap import Bootstrap5

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from SearchShare import SearchForShare


class AskShareNameForm(FlaskForm):
    share_name = StringField('Aktie', validators=[DataRequired()], render_kw={"class": "form-control", "placeholder": "Enter the stock you want"})
    submit = SubmitField("Search", render_kw={"class": "btn btn-primary"})





app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

bootstrap = Bootstrap5(app)


investopedia_url = "https://www.investopedia.com/search"


articles = {
        "title": [],
        "content" : []
    }


suche_erfolgreich_abgeschlossen = False
share_name = ""

"""@app.route('/', methods=['GET', 'POST'])
def start():
    search_for_share = SearchForShare()

    global articles
    global suche_erfolgreich_abgeschlossen
    global share_name

    suche_erfolgreich_abgeschlossen = False



    form = AskShareNameForm()

    # search_for_share.search(form=form)

    if form.validate_on_submit() or request.method == "POST":

        share_name = form.share_name.data

        share_name = share_name.capitalize()

        while not suche_erfolgreich_abgeschlossen:

            try:


                driver = webdriver.Chrome()
                driver.get(investopedia_url)

                driver.implicitly_wait(10)
                # cookies_popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/button'))

                cookies_popup = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))

                cookies_popup.click()
                cookies_popup.click()

                search_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="search-results__input-wrapper_1-0"]/div/input')))

                # search_input = driver.find_element(By.XPATH, '//*[@id="search-results__input-wrapper_1-0"]/div/input')
                # search_input = driver.find_element(By.XPATH, '//*[@id="search-results__input-wrapper_1-0"]/div/input')

                search_input.send_keys(share_name)
                search_input.send_keys(Keys.ENTER)

                try:
                    cookies_popup = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))
                    cookies_popup.click()
                    cookies_popup.click()
                except:
                    print("Element nicht gefunden")

                articles["title"] = []
                articles["content"] = []

                for _ in range(1, 10):
                    driver.implicitly_wait(1)
                    print(_)
                    article_title = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.ID, f'search-results__title_{_}-0')))

                    # article_title = driver.find_element(By.XPATH, f'//*[@id="search-results__title_{_}-0"]')
                    articles["title"].append(article_title.text)
                    article_title.click()
                    #article_title.click()

                    key_facts = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, f'//*[@id="mntl-sc-block-callout-body_1-0"]')))
                    # key_facts = driver.find_element(By.XPATH, '//*[@id="mntl-sc-block-callout-body_1-0"]')
                    articles['content'].append(key_facts.text)

                    driver.back()

                print(articles)
                suche_erfolgreich_abgeschlossen = True
                driver.quit()

            except:
                print("Suchvorgang konnte nicht beendet werdn. Warten Sie eien Moment")

        return redirect(url_for("start", articles=articles, share_name = share_name))

    return render_template("start.html", form = form, articles = articles, share_name = share_name)

"""


search_for_share = SearchForShare()

@app.route('/', methods=['GET', 'POST'])
def start():
    global search_for_share
    search_for_share.search_successful_completed = False
    form = AskShareNameForm()
    #global search_for_share

    if request.method == "POST" or form.validate_on_submit():
        search_for_share.search(form)
        return redirect(url_for("start", articles=search_for_share.articles, share_name=search_for_share.share_name))

    return render_template("start.html", form = form, articles = search_for_share.articles, share_name = search_for_share.share_name)




if __name__ == '__main__':
    app.run(debug=True, port=5011)
