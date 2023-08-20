from datetime import datetime

from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import current_user, login_required
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from openpyxl import load_workbook, Workbook
from openpyxl.utils.exceptions import InvalidFileException

from zipfile import BadZipFile

from webapp.card.forms import BaseCardForm, CardsFromFile, NewCardForm 
from webapp.model import db
from webapp.card.models import Card, CardType
from webapp.deck.views import create_list_of_decks
from werkzeug.utils import secure_filename

from webapp.config import OPERATIONALERROR_TEXT
blueprint = Blueprint('card', __name__, url_prefix='/cards')


def delete_card(card):
    try:
        if card and card.user.id == current_user.id:
            db.session.delete(card)
            db.session.commit()
        else:
            flash("Это не ваша карточка")
    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT
    

# стоит подумать передавать форму целиком или данные из формы    
def cards_list_from_workbook(workbook, data_from_form):
    now = datetime.now().date()
    cards_list = []

    for row in workbook.rows:
        data_from_row = []
        for cell in row:
            data_from_row.append(cell.value)
        card = {"side_1": data_from_row[0], 
                "side_2": data_from_row[1], 
                "deck_id": data_from_form["deck_id"], 
                "is_active": True, 
                "tags": "card from file",
                "cardtype_id": data_from_form["cardtype_id"], 
                "user_id": current_user.id,
                "weights": 2.5,
                "inter_repetition_interval": 0,
                "successfully_count": 0,
                "last_repetition": now,
                "next_repetition": now
        }
        cards_list.append(card)
    cards_list.pop(0)
    return cards_list



@blueprint.route("/new", methods=["POST", "GET"])
@login_required
def create_card():
    try:
        card_form = NewCardForm()
        cards_from_file = CardsFromFile()

        if card_form.validate_on_submit():
            #вынести в функцию !!!
            now = datetime.now().date()
            new_card = Card(
                side_1=card_form.side_1.data,
                side_2=card_form.side_2.data,
                deck_id=card_form.deck.data,
                is_active=card_form.is_active.data,
                tags=card_form.tags.data,
                cardtype_id=card_form.type.data,
                user_id=current_user.id,
                weights=2.5,
                inter_repetition_interval=0,
                successfully_count=0,
                last_repetition=now,
                next_repetition=now
                )

            db.session.add(new_card)
            db.session.commit()

            flash(f"Карточка ID: {new_card.id}, лицо: {new_card.side_1}  создана")
            return redirect(url_for("card.create_card"))

        decks = []
        for deck in current_user.deck:
            decks.append((deck.id, deck.name))

        card_types = []
        for card_type in db.session.scalars(db.select(CardType).order_by(CardType.id)).all():
            card_types.append((card_type.id, card_type.name))

        card_form.deck.choices = decks
        card_form.type.choices = card_types

        cards_from_file.deck.choices = decks
        cards_from_file.type.choices = card_types


        return render_template("card/add_new_card_form.html", card_form=card_form,  cards_from_file=cards_from_file , page_title='создание карточки')# откуда тут взялось decks=create_list_of_decks()?

    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT


@blueprint.route("/edit/<int:card_id>", methods=["POST", "GET"])
@login_required
def edit_card(card_id):
    try:
        card = db.session.scalars(db.select(Card).filter_by(id=card_id)).first()
        if card and card.user.id == current_user.id:
            card_form = BaseCardForm()
            if card_form.validate_on_submit():
                if card_form.button.data:
                    card.side_1 = card_form.side_1.data
                    card.side_2 = card_form.side_2.data
                    card.is_active = card_form.is_active.data
                    card.tags = card_form.tags.data
                    card.cardtype_id = card_form.type.data

                    db.session.add(card)
                    db.session.commit()
                    flash("Карточка обновлена")

                if card_form.delete_button.data:
                    deck = card.deck
                    delete_card(card)
                    flash("Карточка удалена")
                    return redirect(url_for("deck.deck_view", deck_id=deck.id))
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

            return render_template("card/edit_card_form.html", card_form=card_form, page_title='редактирование карточки')
        flash("Это не ваша карточка")
        return redirect(url_for("index"))

    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT

#Пока пихаем все в одну функцию, потом уже разнести
@blueprint.route("/from_file", methods=["POST"])
@login_required
def load_cards_from_file():
    cards_from_file = CardsFromFile()
    if cards_from_file.validate_on_submit():
        file_name = cards_from_file.file_with_cards.data.filename 

        if file_name.split(".")[-1] in ["xlsx", "xls"]:
            try:
                workbook = load_workbook(filename=cards_from_file.file_with_cards.data)
                ws = workbook.active
                
                date_from_from = {"cardtype_id": cards_from_file.type.data, "deck_id": cards_from_file.deck.data}

                cards_list = cards_list_from_workbook(ws, date_from_from)

                db.session.bulk_insert_mappings(Card, cards_list, return_defaults=True)
                db.session.commit()
                flash("Карточки успешно созданы", "info")

            except(SQLAlchemyError):
                flash("Ошибка записи данных", "error")
            except(BadZipFile, InvalidFileException):
                flash("Ошибка чтения файла", "error")
        else:
            flash("Файл не xls | xlsx", "warning")
    else:
        flash("Ошибка в заполнении формы", "error")    
    return(redirect(url_for("card.create_card")))
