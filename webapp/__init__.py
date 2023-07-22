from flask import Flask, render_template, flash
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from sqlalchemy.exc import OperationalError
from webapp.settings import DATABASE_URI, SECRET_KEY

from webapp.model import db
from webapp.user.models import User

from webapp.config import OPERATIONALERROR_TEXT

from webapp.user.views import blueprint as user_blueprint
from webapp.deck.views import blueprint as deck_blueprint
from webapp.card.views import blueprint as card_blueprint
from webapp.study.views import blueprint as study_blueprint
from webapp.deck.views import create_list_of_decks


def create_app(config_file=None):
    app = Flask(__name__)
    if not config_file:
        app.config.from_pyfile("config.py")
    else:
        app.config.from_pyfile(config_file)    
    

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
                deks_to_template = create_list_of_decks()
                deks_to_template = sorted(deks_to_template, key=lambda x: x["card_count"], reverse=True)
                if len(deks_to_template) > 5:
                    deks_to_template = deks_to_template[:5]
                return render_template("index.html", decks=deks_to_template, page_title='домашняя страница')
            return render_template("index.html")
        except OperationalError:
            flash(OPERATIONALERROR_TEXT)
            return OPERATIONALERROR_TEXT

    return app
