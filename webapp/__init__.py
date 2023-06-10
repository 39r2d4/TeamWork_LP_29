from flask import Flask, request, render_template, flash, url_for, redirect
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from webapp.forms import CardForm, Deck, LoginForm
from webapp.model import db, User


from webapp.mock import m_card_type, m_deck


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
            login_form = LoginForm()
            if login_form.validate_on_submit():
                try:
                    user = User.query.filter_by(username=login_form.username.data).first()
                    if user and user.check_password(login_form.password.data):
                        login_user(user)
                        flash('Успешная авторизация')
                        return redirect(url_for("index"))
                except: #"sqlalchemy.exc.OperationalError" Добавить обработку ошибок алхимии (!!!)
                    flash("БД недоступна, повторите попытку позже")
                    return redirect(url_for("login"))

            flash("Не правильный логин или пароль")
            return redirect(url_for("login"))

        if current_user.is_authenticated:
            return(redirect(url_for("index")))
        login_form = LoginForm()
        return render_template("login.html", form=login_form)


    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Вы вышли из системы")
        return redirect(url_for("index"))
    


    @app.route("/card/new", methods=["POST", "GET"]) 
    @login_required 
    def create_card():
        card_form = CardForm()
        if card_form.validate_on_submit():
                return f" Text side_1: {card_form.side_1.data.split('/n').strip()}, Text side_2: {card_form.side_2.data.split('/n')}, \
                      {card_form.type.data}, Колода: {card_form.deck.data}, тип карточки: {card_form.type.data},"
        
        card_form.deck.choices = m_deck
        card_form.type.choices = m_card_type
        return render_template("card_form.html", card_form = card_form) 


    @app.route("/deck/new", methods=["POST", "GET"])
    @login_required
    def dack_new():
        deck_form = Deck()
        if deck_form.validate_on_submit():
            return f"deck name: {deck_form.name.data}"
        return render_template("deck.html", deck_form=deck_form)







    return app
