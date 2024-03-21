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
