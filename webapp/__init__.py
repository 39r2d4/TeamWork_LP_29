from flask import Flask, request, render_template, flash, url_for, redirect
from flask_login import LoginManager, login_user
from webapp.forms import LoginForm
from webapp.model import db, User

def create_app():

    app  = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


    @app.route("/")
    def index():
        return render_template("index.html", number = 5)
    

    @app.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "GET":
            login_form = LoginForm()
            return render_template("login.html", form=login_form)
        elif request.method == "POST":
            form = LoginForm()
            if form.validate_on_submit():
                user = User.query.filter_by(username=form.username.data).first()
                print(user)
                if user and user.check_password(form.password.data):
                    login_user(user)
                    flash('Успешная авторизация')
                    return redirect(url_for("index"))


            flash("Не вернвый логин или пароль")
            return redirect(url_for("login"))


    return app
