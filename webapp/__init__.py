from flask import Flask, request, render_template, flash, url_for, redirect
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from flask_migrate import Migrate
from sqlalchemy.exc import OperationalError
from webapp.forms import CardForm, DeckForm, LoginForm
from webapp.model import db, User, Deck, Card, CardType


from webapp.config import OPERATIONALERROR_TEXT




def create_app():

    app  = Flask(__name__)
    app.config.from_pyfile("config.py")

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"




    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


    @app.route("/")
    def index():
        try:
            return render_template("index.html", number = 1)
        except(OperationalError):
            flash(OPERATIONALERROR_TEXT)
            return(OPERATIONALERROR_TEXT)

    @app.route("/login", methods=["POST", "GET"])
    def login():
        try:
            if request.method == "GET":
                login_form = LoginForm()
                return render_template("login.html", form=login_form)
            
            elif request.method == "POST": #переделать просто на validate_on_submit()
                login_form = LoginForm()
                if login_form.validate_on_submit():

                    user = User.query.filter_by(username=login_form.username.data).first()
                    if user and user.check_password(login_form.password.data):
                        login_user(user)
                        flash('Успешная авторизация')
                        return redirect(url_for("index"))

                flash("Не правильный логин или пароль")
                return redirect(url_for("login"))

            if current_user.is_authenticated:
                return(redirect(url_for("index")))
            login_form = LoginForm()
            return render_template("login.html", form=login_form)
        except(OperationalError):
            flash(OPERATIONALERROR_TEXT)
            return(OPERATIONALERROR_TEXT)


    @app.route("/logout")
    @login_required
    def logout():
        try:
            logout_user()
            flash("Вы вышли из системы")
            return redirect(url_for("index"))
        except(OperationalError):# не работает на функциях с @login_required
            flash(OPERATIONALERROR_TEXT)
            return(OPERATIONALERROR_TEXT)            


    @app.route("/card/new", methods=["POST", "GET"]) 
    @login_required 
    def create_card():
        try:
            card_form = CardForm()
            if card_form.validate_on_submit():
                   new_card = Card(
                        side_1=card_form.side_1.data,
                        side_2=card_form.side_2.data,
                        deck_id=card_form.deck.data, 
                        is_active=card_form.is_active.data, 
                        tags=card_form.tags.data, 
                        cardtype_id=card_form.type.data,
                        user_id = current_user.id)
                   
                   db.session.add(new_card)
                   db.session.commit()

                   flash(f"Карточка ID: {new_card.id}, сторона_1: {new_card.side_1}  создана")
                   return redirect(url_for("create_card"))
            
            decks = []
            for deck in current_user.deck:
                decks.append((deck.id, deck.name))

            card_types = []
            for card_type in db.session.scalars(db.select(CardType).order_by(CardType.id)).all():   
                card_types.append((card_type.id, card_type.name))
            
            card_form.deck.choices = decks
            card_form.type.choices = card_types
            
            return render_template("card_form.html", card_form = card_form) 
        except(OperationalError):
            flash(OPERATIONALERROR_TEXT)
            return(OPERATIONALERROR_TEXT)


    @app.route("/deck/new", methods=["POST", "GET"])
    @login_required
    def dack_new():
        try:
            deck_form = DeckForm()
            if deck_form.validate_on_submit():
                    new_deck = Deck(name=deck_form.name.data, comment=deck_form.comment.data, user_id=current_user.id)
                    db.session.add(new_deck)
                    db.session.commit()
                    flash(f"Колода {deck_form.name.data} создана")

                 
            return render_template("deck.html", deck_form=deck_form)
        except(OperationalError):
            flash(OPERATIONALERROR_TEXT)
            return(OPERATIONALERROR_TEXT)

    return app
