from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class DeckForm(FlaskForm):
    name = StringField("Название колоды", validators=[DataRequired()], render_kw={"class": "form-control"})
    comment = StringField("Комментарий колоды", render_kw={"class": "form-control"})
    button = SubmitField("Сохранить", render_kw={"class": "btn btn-primary"})


class DeckDeleteForm(FlaskForm):
    delete_button = SubmitField("Удалить в любом случае", render_kw={"class": "btn btn-danger", "data-bs-dismiss": "modal"})
    
