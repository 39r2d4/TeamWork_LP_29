from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class StudyForm(FlaskForm):
    cad_id = StringField("ID карты", render_kw={"type": "hidden"})
    hurd_button = SubmitField("Снова", render_kw={"class": "btn btn-danger"})
    norm_button = SubmitField("Хорошо", render_kw={"class": "btn btn-warning"})
    easy_button = SubmitField("Легко", render_kw={"class": "btn btn-success"})
