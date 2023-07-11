from flask import Blueprint, request, render_template, flash, url_for, redirect
from flask_login import current_user, login_user, logout_user, login_required
from webapp.user.forms import LoginForm, SignupForm
from webapp.user.models import User
from sqlalchemy.exc import OperationalError
from webapp.model import db
from webapp.config import OPERATIONALERROR_TEXT


blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route("/login", methods=["POST", "GET"])
def login():
    try:
        if request.method == "GET":
            login_form = LoginForm()
            return render_template("/user/login.html", form=login_form)

        elif request.method == "POST":  # переделать просто на validate_on_submit()
            login_form = LoginForm()
            if login_form.validate_on_submit():

                user = User.query.filter_by(username=login_form.username.data).first()
                if user and user.check_password(login_form.password.data):
                    login_user(user)
                    flash('Успешная авторизация')
                    return redirect(url_for("index"))

            flash("Не правильный логин или пароль")
            return redirect(url_for("user.login"))

        if current_user.is_authenticated:
            return redirect(url_for("user.index"))
        login_form = LoginForm()
        return render_template("/user/login.html", form=login_form)

    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT


@blueprint.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("user.index"))
    title = 'Регистрация'
    signup_form = SignupForm()
    return render_template('/user/signup.html', page_title=title, form=signup_form)


@blueprint.route('/process-signup', methods=['POST'])
def process_signup():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        new_user = User(username=signup_form.username.data, email=signup_form.email.data, role='user')
        new_user.set_password(signup_form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Вы успешно зарегистрировались")
        return redirect(url_for('user.login'))

    for error in signup_form.errors:
        match error:
            case "email":
                flash("Введите корректный Email")
            case "password2":
                flash("Пароли не совпадают")
    flash('пожалуйста, исправьте ошибки в форме')

    return redirect(url_for('signup'))


@blueprint.route("/logout")
@login_required
def logout():
    try:
        logout_user()
        flash("Вы вышли из системы")
        return redirect(url_for("user.index"))
    except OperationalError:
        flash(OPERATIONALERROR_TEXT)
        return OPERATIONALERROR_TEXT
