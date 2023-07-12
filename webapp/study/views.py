from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import current_user, login_required
from sqlalchemy.exc import OperationalError

from webapp.deck.forms import DeckForm
from webapp.study.forms import StudyForm

from webapp.model import db

from webapp.card.models import Card
from webapp.deck.models import Deck


from webapp.config import OPERATIONALERROR_TEXT
import random

blueprint = Blueprint('study', __name__, url_prefix='/decks')


@blueprint.route("/deck/study/<int:deck_id>", methods=["GET"])
@login_required
def deck_study(deck_id):
    try:
        deck = db.session.scalars(db.select(Deck).filter_by(id=deck_id)).first()
        if deck.user_id == current_user.id:
            card_with_max_weights = db.session.scalars(db.select(Card).filter_by(deck_id=deck_id).filter_by(user_id=current_user.id).order_by(-Card.weights).limit(5)).all()
            random_card = card_with_max_weights[random.randint(0, len(card_with_max_weights)-1)]
            study_form = StudyForm(cad_id=random_card.id)

            return render_template("deck/study/study_deck.html", card=random_card, study_form=study_form)

    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT


@blueprint.route("/study/<int:deck_id>", methods=["POST"])
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

                return redirect(url_for("study.deck_study", deck_id=deck_id))
        return study_form.card_id.data

    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT
