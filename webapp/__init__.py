from flask import Flask, render_template, flash
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy.exc import OperationalError

from webapp.card.forms import BaseCardForm, NewCardForm
from webapp.deck.forms import DeckForm
from webapp.study.forms import StudyForm

from webapp.model import db
from webapp.card.models import Card, CardType
from webapp.deck.models import Deck
from webapp.user.models import User

from webapp.config import OPERATIONALERROR_TEXT
from webapp.user.views import blueprint as user_blueprint
from webapp.deck.views import blueprint as deck_blueprint
from webapp.card.views import blueprint as card_blueprint


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    app.register_blueprint(user_blueprint)
    app.register_blueprint(deck_blueprint)
    app.register_blueprint(card_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    def index():
        try:
            return render_template("index.html", number=1)
        except OperationalError:
            flash(OPERATIONALERROR_TEXT)
            return OPERATIONALERROR_TEXT

    return app