from datetime import datetime, timedelta
from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import current_user, login_required
from sqlalchemy.exc import OperationalError

from webapp.deck.forms import DeckForm
from webapp.study.forms import StudyForm

from webapp.model import db

from webapp.card.models import Card
from webapp.deck.models import Deck
from sqlalchemy import func

from webapp.config import OPERATIONALERROR_TEXT
import random

blueprint = Blueprint('study', __name__, url_prefix='/decks')


def algorithm(user_grade, successfully_count, weights, inter_repetition_interval):
    if user_grade >= 1:
        if successfully_count == 0:
            inter_repetition_interval = 1
        elif successfully_count == 1 and user_grade == 2:
            inter_repetition_interval = 6
        elif successfully_count == 1 and user_grade == 1:
            inter_repetition_interval = 3
        else:
            inter_repetition_interval += round(inter_repetition_interval + weights)
        successfully_count += 1

    else:
        successfully_count = 0
        inter_repetition_interval = 0

    weights += (0.1 - (5 - user_grade) * (0.08 + (5 - user_grade) * 0.02))
    if weights < 1.3:
        weights = 1.3
         
    return successfully_count, weights, inter_repetition_interval





@blueprint.route("/study/<int:deck_id>", methods=["GET"])   
@login_required
def deck_study(deck_id):
    try:
        deck = db.session.scalars(db.select(Deck).filter_by(id=deck_id)).first()
        if deck.user_id == current_user.id:
            cards_for_repeat = db.session.scalars(db.select(Card).filter_by(deck_id=deck_id).filter_by(user_id=current_user.id).filter(func.DATE(Card.next_repetition) <= func.current_date())).all()
            if len(cards_for_repeat) == 0:
                flash("Нет карт для повторения")
                return redirect(url_for("deck.decks_view"))

            random_card = cards_for_repeat[random.randint(0, len(cards_for_repeat)-1)]
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
                if study_form.hurd_button.data:
                    user_grade = 0 
                elif study_form.norm_button.data:
                    user_grade = 1
                elif study_form.easy_button.data:
                    user_grade = 2

                card_id=study_form.cad_id.data
                user_id=current_user.id
                card = db.session.scalars(db.select(Card).filter_by(id=card_id).filter_by(user_id=user_id)).first()

                successfully_count = card.successfully_count
                weights = card.weights
                inter_repetition_interval = card.inter_repetition_interval
                
                successfully_count, weights, inter_repetition_interval = algorithm(user_grade, successfully_count, weights, inter_repetition_interval)
                card.successfully_count = successfully_count
                card.weights = weights
                card.inter_repetition_interval = inter_repetition_interval
                now = datetime.utcnow().date()
                card.last_repetition = now
                card.next_repetition = now + timedelta(inter_repetition_interval)
                db.session.add(card)
                db.session.commit()

                return redirect(url_for("study.deck_study", deck_id=deck_id))
        return study_form.card_id.data

    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT
