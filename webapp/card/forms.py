from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired


class CardType(FlaskForm):
    name = StringField("Название типа карточки")
    description = StringField("Описание")


class BaseCardForm(FlaskForm):
    side_1 = TextAreaField("Лицо", validators=[DataRequired()], render_kw={"class": "form-control"})
    side_2 = TextAreaField("Оборот", validators=[DataRequired()], render_kw={"class": "form-control"})
    is_active = BooleanField("Карточка активна", render_kw={"class": "form-check-input", "type": "checkbox"})
    tags = StringField("Ключевые слова", validators=[DataRequired()], render_kw={"class": "form-control"})
    type = SelectField("Тип", choices=[], coerce=int, render_kw={"class": "form-control"}, validate_choice=False)  # !!!
    button = SubmitField("Сохранить", render_kw={"class": "btn btn-primary"})


class NewCardForm(BaseCardForm):
    deck = SelectField("Колода", choices=[], coerce=int, render_kw={"class": "form-control"}, validate_choice=False)  # передавать в форму список колод на выбор