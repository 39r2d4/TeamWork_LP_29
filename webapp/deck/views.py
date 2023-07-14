from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import current_user, login_required
from sqlalchemy.exc import OperationalError

from webapp.deck.forms import DeckForm
from webapp.study.forms import StudyForm

from webapp.model import db

from webapp.card.models import Card
from webapp.deck.models import Deck


from webapp.config import OPERATIONALERROR_TEXT

blueprint = Blueprint('deck', __name__, url_prefix='/decks')


@blueprint.route("/new", methods=["POST", "GET"])
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


@blueprint.route("/view")
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


@blueprint.route("/view/<int:deck_id>")
@login_required
def deck_view(deck_id):
    try:
        deck = db.session.scalars(db.select(Deck).filter_by(id=deck_id)).first()
        if deck.user_id == current_user.id:
            # пока без пагинации
            return render_template("deck/deck_with_cards.html", deck=deck)
        flash("Это не ваша колода")

        return redirect(url_for("deck.decks_view"))

    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT
