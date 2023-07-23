from flask_wtf import FlaskForm, RecaptchaField

from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField("Пароль", validators=[DataRequired()], render_kw={"class": "form-control"})
    button = SubmitField("Войти", render_kw={"class": "btn btn-primary"})


class SignupForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField("Email пользователя", validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField("Пароль", validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField("Повторите пароль", validators=[DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    button = SubmitField("Зарегистрироваться", render_kw={"class": "btn btn-primary"})
    recaptcha = RecaptchaField()
    