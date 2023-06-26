from flask_wtf import FlaskForm
from wtforms import Form, FieldList, StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField("Пароль", validators=[DataRequired()], render_kw={"class": "form-control"})
    button = SubmitField("Войти", render_kw={"class": "btn btn-primary"})


class CardType(FlaskForm):
    name = StringField("Название типа карточки")
    description = StringField("Описание")



class BaseCardForm(FlaskForm): #CardForm(FlaskForm):
    side_1 = TextAreaField("Текст стороны 1", validators=[DataRequired()], render_kw={"class": "form-control"})
    side_2 = TextAreaField("Текст стороны 2", validators=[DataRequired()],render_kw={"class": "form-control"})
    is_active = BooleanField("Карточка активна", render_kw={"class": "form-check-input", "type": "checkbox"})
    tags = StringField("Метка", validators=[DataRequired()],render_kw={"class": "form-control"})
    type = SelectField("Тип карточки",choices=[] , coerce=int, render_kw={"class": "form-control"}, validate_choice=False)#!!!
    button = SubmitField("Сохранить", render_kw={"class": "btn btn-primary"})


class NewCardForm(BaseCardForm):
    deck = SelectField("Колода",choices=[], coerce=int, render_kw={"class": "form-control"}, validate_choice=False) #передавать в форму список колод на выбор


class DeckForm(FlaskForm):
    name = StringField("Название колоды", validators=[DataRequired()], render_kw={"class": "form-control"})
    comment = StringField("Комментарий колоды", render_kw={"class": "form-control"})
    button = SubmitField("Сохранить", render_kw={"class": "btn btn-primary"})


class StudyForm(FlaskForm):
    cad_id = StringField("ID карты", render_kw={"type": "hidden"})
    hurd_button = SubmitField("сложна", render_kw={"class":"btn btn-danger"})
    norm_button = SubmitField("Норм", render_kw={"class":"btn btn-warning"})
    easy_button = SubmitField("лкгко", render_kw={"class":"btn btn-success"})

