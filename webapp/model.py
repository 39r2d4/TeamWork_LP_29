from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
 

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "user_teble"
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True)
    username: db.Mapped[str] = db.mapped_column(db.String(64), index=True, unique=True)
    password: db.Mapped[str] = db.mapped_column(db.String(128))
    role: db.Mapped[str] = db.mapped_column(db.String, nullable=False)

    deck: db.Mapped[list["Deck"]] = db.relationship()
    card: db.Mapped[list["Card"]] = db.relationship()


    def __repr__(self):
        return f"User ID: {self.id}, Name: {self.username}"

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Deck(db.Model):
    __tablename__ = "deck_table"
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True)
    name: db.Mapped[str] = db.mapped_column(db.String(64), index=True)
    comment: db.Mapped[str] = db.mapped_column(db.String(128))
    user_id: db.Mapped[int] = db.mapped_column(db.ForeignKey("user_teble.id"), index=True)
    
    user: db.Mapped["User"] = db.relationship(back_populates= "deck")
    card: db.Mapped[list["Card"]] = db.relationship(back_populates="deck")


    def __repr__(self):
        return f"Deck id: {self.id}, name: {self.name}"

class CardType(db.Model):
    __tablename__ = "CardType_table"
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True)
    name: db.Mapped[str] = db.mapped_column(db.String(64), index=True, unique=True)
    description: db.Mapped[str] = db.mapped_column(db.String(128))
    
    card: db.Mapped[list["Card"]] = db.relationship(back_populates="card_type")
    
    def __repr__(self):
        return f"CardType id: {self.id}, name: {self.name}"

class Card(db.Model):
    __tablename__ = "Card_table"
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True)
    side_1: db.Mapped[str] = db.mapped_column(db.String(256))
    side_2: db.Mapped[str] = db.mapped_column(db.String(256))
    deck_id: db.Mapped[int] = db.mapped_column(db.ForeignKey("deck_table.id"), index=True)
    is_active: db.Mapped[bool] = db.mapped_column()
    tags: db.Mapped[str] = db.mapped_column(db.String(256))
    cardtype_id: db.Mapped[int] = db.mapped_column(db.ForeignKey("CardType_table.id"), index=True)
    user_id: db.Mapped[int] = db.mapped_column(db.ForeignKey("user_teble.id"), index=True)
    weights:db.Mapped[int] = db.mapped_column(db.Integer())
    
    card_type: db.Mapped["CardType"] = db.relationship()
    deck: db.Mapped["Deck"] = db.relationship(back_populates="card")
    user: db.Mapped["User"] = db.relationship(back_populates= "card")


    def __repr__(self):
        return f"Card id: {self.id}, side_1: {self.side_1}"
 
