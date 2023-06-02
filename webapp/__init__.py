from flask import Flask, render_template, flash, url_for

from webapp.forms import LoginForm
from webapp.model import db

def create_app():

    app  = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)


    @app.route("/")
    def hello():
        return render_template("index.html", number = 5)
    

    @app.route("/login")
    def login():
        login_form = LoginForm()
        return render_template("login.html", form=login_form)

    return app
