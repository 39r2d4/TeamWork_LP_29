from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.model import db


class User(db.Model, UserMixin):
    __tablename__ = "user_teble"
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True)
    username: db.Mapped[str] = db.mapped_column(db.String(64), index=True, unique=True)
    password: db.Mapped[str] = db.mapped_column(db.String(128))
    email: db.Mapped[str] = db.mapped_column(db.String(64), nullable=True)
    role: db.Mapped[str] = db.mapped_column(db.String, nullable=False)

    deck: db.Mapped[list["Deck"]] = db.relationship()
    card: db.Mapped[list["Card"]] = db.relationship()

    def __repr__(self):
        return f"User ID: {self.id}, Name: {self.username}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
