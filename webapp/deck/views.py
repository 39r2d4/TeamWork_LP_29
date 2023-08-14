from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import current_user, login_required
from sqlalchemy.exc import OperationalError

from webapp.deck.forms import DeckForm, DeckDeleteForm
from webapp.study.forms import StudyForm

from webapp.model import db
from webapp.card.models import Card
from webapp.deck.models import Deck


from webapp.config import OPERATIONALERROR_TEXT

blueprint = Blueprint('deck', __name__, url_prefix='/decks')


def create_list_of_decks():
    deks_to_template = []
    for deck in current_user.deck:
        deck_dickt = dict()
        deck_dickt["id"] = deck.id
        deck_dickt["name"] = deck.name
        deck_dickt["comment"] = deck.comment
        deck_dickt["card_count"] = len(deck.card)
        deks_to_template.append(deck_dickt)
    return deks_to_template


def delete_deck(deck):
    try:
        if deck and deck.user.id == current_user.id:
            db.session.delete(deck)
            db.session.commit()
            print("колода удалена")
        else:
            flash("Это не ваша карточка")
    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT


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

        return render_template("deck/add_new_deck.html", deck_form=deck_form, page_title='создание колоды')

    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT


@blueprint.route("/view")
@login_required
def decks_view():
    try:
        return render_template("deck/decks_view.html", decks=create_list_of_decks(), page_title='колоды')

    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT


@blueprint.route("/view/<int:deck_id>", methods=["POST", "GET"])
@login_required
def deck_view(deck_id):
    try:
        deck = db.session.scalars(db.select(Deck).filter_by(id=deck_id)).first()
        if deck.user_id == current_user.id:
            # пока без пагинации
            deck_form = DeckDeleteForm()
            if deck_form.validate_on_submit():
                if deck_form.delete_button.data:
                    delete_deck(deck)
                    flash("Колода удалена")
                    return redirect(url_for("deck.decks_view"))
            return render_template("deck/deck_with_cards.html", deck=deck, deck_form=deck_form, page_title=f'{deck.name}')
        flash("Это не ваша колода")

        return redirect(url_for("deck.decks_view"))

    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT
