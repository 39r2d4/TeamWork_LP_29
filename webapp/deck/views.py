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

blueprint = Blueprint('deck', __name__, url_prefix='/decks')


@blueprint.route("/deck/new", methods=["POST", "GET"])
@login_required
def deck_new():
    try:
        deck_form = DeckForm()
        if deck_form.validate_on_submit():
            # Добавить проверку на дубль названия колоды(!!!)
            new_deck = Deck(name=deck_form.name.data, comment=deck_form.comment.data, user_id=current_user.id)
            db.session.add(new_deck)
            db.session.commit()
            flash(f"Колода {deck_form.name.data} создана")

        return render_template("deck/add_new_deck.html", deck_form=deck_form)

    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT


@blueprint.route("/deck/view")
@login_required
def decks_view():
    try:
        deks_to_teamplate = []
        for deck in current_user.deck:
            deck_dickt = dict()
            deck_dickt["id"] = deck.id
            deck_dickt["name"] = deck.name
            deck_dickt["comment"] = deck.comment
            deck_dickt["card_count"] = len(deck.card)
            deks_to_teamplate.append(deck_dickt)

        return render_template("deck/decks_view.html", decks=deks_to_teamplate)

    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT


@blueprint.route("/deck/view/<int:deck_id>")
@login_required
def deck_view(deck_id):
    try:
        deck = db.session.scalars(db.select(Deck).filter_by(id=deck_id)).first()
        if deck.user_id == current_user.id:
            # пока без пагинации
            return render_template("deck/deck_with_cards.html", deck=deck)
        flash("Это не ваша колода")

        return redirect(url_for("decks_view"))

    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT


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


@blueprint.route("/deck/study/<int:deck_id>", methods=["POST"])
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

                return redirect(url_for("deck_study", deck_id=deck_id))
        return study_form.card_id.data

    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT
