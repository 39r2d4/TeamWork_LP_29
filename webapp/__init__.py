from flask import Flask, request, render_template, flash, url_for, redirect
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from flask_migrate import Migrate
from sqlalchemy.exc import OperationalError

from webapp.forms import BaseCardForm, DeckForm, LoginForm, NewCardForm, StudyForm
from webapp.model import db, User, Deck, Card, CardType

from webapp.config import OPERATIONALERROR_TEXT

from webapp.mock import m_card_type, m_deck
import random


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
        except(OperationalError):
            flash(OPERATIONALERROR_TEXT)
            return(OPERATIONALERROR_TEXT)            


    @app.route("/card/new", methods=["POST", "GET"]) 
    @login_required 
    def create_card():
        try:
            card_form = NewCardForm()
            if card_form.validate_on_submit():
                   new_card = Card(
                        side_1=card_form.side_1.data,
                        side_2=card_form.side_2.data,
                        deck_id=card_form.deck.data, 
                        is_active=card_form.is_active.data, 
                        tags=card_form.tags.data, 
                        cardtype_id=card_form.type.data,
                        user_id = current_user.id,
                        weights = 500)
                   
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
            
            return render_template("/card/add_new_card_form.html", card_form = card_form) 

        except(OperationalError):
            flash(OPERATIONALERROR_TEXT)
            return(OPERATIONALERROR_TEXT)
        

    @app.route("/card/edit/<int:card_id>", methods=["POST", "GET"])
    @login_required
    def edit_card(card_id):
        try:
            card = db.session.scalars(db.select(Card).filter_by(id=card_id)).first()
            if card and card.user.id == current_user.id:
                card_form = BaseCardForm()
                if card_form.validate_on_submit():
                    card.side_1 = card_form.side_1.data
                    card.side_2 = card_form.side_2.data
                    card.is_active = card_form.is_active.data 
                    card.tags = card_form.tags.data
                    card.cardtype_id = card_form.type.data

                    db.session.add(card)
                    db.session.commit()
                    flash("Карточка обновлена")

                card_types = []
                # не придумал ничего, кроме как передать в список текущий
                # тип карточки первым в список. возможно у SelectField
                # есть что0то типа значения по умолчанию
                current_card_type = (card.card_type.id, card.card_type.name)
                card_types.append(current_card_type)
                for card_type in db.session.scalars(db.select(CardType).order_by(CardType.id)).all():   
                    if current_card_type[0] != card_type.id:
                        card_types.append((card_type.id, card_type.name))

                card_form.side_1.data = card.side_1
                card_form.side_2.data = card.side_2
                card_form.is_active.data = card.is_active
                card_form.tags.data = card.tags
                card_form.type.choices = card_types
                return render_template("card/edit_card_form.html", card_form=card_form )

            flash("Это не ваша карточка")
            return  redirect(url_for("index"))
    
        except(OperationalError):
            flash(OPERATIONALERROR_TEXT)
            return(OPERATIONALERROR_TEXT)


    @app.route("/deck/new", methods=["POST", "GET"])
    @login_required
    def deck_new():
        try:
            deck_form = DeckForm()
            if deck_form.validate_on_submit():
                    #Добавить проверку на дубль названия колоды(!!!)
                    new_deck = Deck(name=deck_form.name.data, comment=deck_form.comment.data, user_id=current_user.id)
                    db.session.add(new_deck)
                    db.session.commit()
                    flash(f"Колода {deck_form.name.data} создана")

                 
            return render_template("deck/add_new_deck.html", deck_form=deck_form)

        except(OperationalError):
            flash(OPERATIONALERROR_TEXT)
            return(OPERATIONALERROR_TEXT)


    @app.route("/deck/view")
    @login_required
    def decks_view():
        try:
            deks_to_teamplate = []
            for deck in current_user.deck:
                deck_dickt = {}
                deck_dickt["id"] = deck.id
                deck_dickt["name"] = deck.name
                deck_dickt["comment"] = deck.comment
                deck_dickt["card_count"] = len(deck.card)
                deks_to_teamplate.append(deck_dickt)

            return render_template("deck/decks_view.html", decks=deks_to_teamplate) 
    
        except(OperationalError):
            flash(OPERATIONALERROR_TEXT)
            return(OPERATIONALERROR_TEXT)


    @app.route("/deck/view/<int:deck_id>")
    @login_required
    def deck_view(deck_id):
        try:
            deck = db.session.scalars(db.select(Deck).filter_by(id=deck_id)).first()
            if deck.user_id == current_user.id:
                #пока без пагинации
                return render_template("deck/deck_with_cards.html", deck=deck)
            flash("Это не ваша колода")
            return(redirect(url_for("decks_view")))
        except(OperationalError):
            flash(OPERATIONALERROR_TEXT)
            return(OPERATIONALERROR_TEXT)
        

    @app.route("/deck/study/<int:deck_id>", methods=["GET"])
    @login_required
    def deck_study(deck_id):
        try:
            deck = db.session.scalars(db.select(Deck).filter_by(id=deck_id)).first()
            if deck.user_id == current_user.id:
                card_with_max_weights = db.session.scalars(db.select(Card).filter_by(deck_id=deck_id).filter_by(user_id=current_user.id).order_by(-Card.weights).limit(5)).all()
                random_card = card_with_max_weights[random.randint(0, len(card_with_max_weights)-1)]
                study_form = StudyForm(cad_id=random_card.id)
                return render_template("deck/study/study_deck.html", card=random_card, study_form=study_form)
        except(OperationalError):
            flash(OPERATIONALERROR_TEXT)
            return(OPERATIONALERROR_TEXT)


    @app.route("/deck/study/<int:deck_id>", methods=["POST"])
    @login_required
    def deck_study_post(deck_id):
        try:
            study_form = StudyForm()
            deck = db.session.scalars(db.select(Deck).filter_by(id=deck_id)).first()
            if deck.user_id == current_user.id:
                if study_form.validate_on_submit():
                    card = db.session.scalars(db.select(Card).filter_by(id=study_form.cad_id.data).filter_by(user_id=current_user.id)).first()
                    if study_form.hurd_button.data:
                        card.weights += 5
                    elif study_form.norm_button.data:
                        card.weights -= 1
                    elif study_form.easy_button.data:
                        card.weights -= 2
                    db.session.add(card)
                    db.session.commit()
                    return redirect(url_for("deck_study", deck_id=deck_id ))
            return study_form.card_id.data
        except(OperationalError):
            flash(OPERATIONALERROR_TEXT)
            return(OPERATIONALERROR_TEXT)



    return app
