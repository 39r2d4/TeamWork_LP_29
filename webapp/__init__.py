from flask import Flask, render_template, flash, url_for, redirect
from flask_login import LoginManager, current_user, login_user, logout_user
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
        if current_user.is_authenticated:
            return(redirect(url_for("index")))
        login_form = LoginForm()
        return render_template("login.html", form=login_form)


    app.route("/logout")
    def logout():
        logout_user()
        flash("Вы вышли из системы")
        return url_for("index")

    return app
