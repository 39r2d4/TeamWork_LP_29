from flask import Flask, render_template, flash
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from sqlalchemy.exc import OperationalError


from webapp.model import db
from webapp.user.models import User

from webapp.config import OPERATIONALERROR_TEXT

from webapp.user.views import blueprint as user_blueprint
from webapp.deck.views import blueprint as deck_blueprint
from webapp.card.views import blueprint as card_blueprint
from webapp.study.views import blueprint as study_blueprint


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
    app.register_blueprint(study_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    def index():
        try:
            if current_user.is_authenticated:
                deks_to_template = []
                for deck in current_user.deck:
                    deck_dickt = dict()
                    deck_dickt["id"] = deck.id
                    deck_dickt["name"] = deck.name
                    deck_dickt["comment"] = deck.comment
                    deck_dickt["card_count"] = len(deck.card)
                    deks_to_template.append(deck_dickt)
                deks_to_template = sorted(deks_to_template, key=lambda x: x["card_count"], reverse=True)
                if len(deks_to_template) > 5:
                    deks_to_template = deks_to_template[:5]
                return render_template("index.html", decks=deks_to_template)
            return render_template("index.html")
        except OperationalError:
            flash(OPERATIONALERROR_TEXT)
            return OPERATIONALERROR_TEXT

    return app
