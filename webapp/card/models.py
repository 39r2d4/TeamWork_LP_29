from webapp.model import db
from datetime import datetime


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
    side_2: db.Mapped[str] = db.mapped_column(db.String(2048))
    deck_id: db.Mapped[int] = db.mapped_column(db.ForeignKey("deck_table.id"), index=True)
    is_active: db.Mapped[bool] = db.mapped_column()
    tags: db.Mapped[str] = db.mapped_column(db.String(256))
    cardtype_id: db.Mapped[int] = db.mapped_column(db.ForeignKey("CardType_table.id"), index=True)
    user_id: db.Mapped[int] = db.mapped_column(db.ForeignKey("user_teble.id"), index=True)

    weights: db.Mapped[float] = db.mapped_column(db.Float())
    successfully_count: db.Mapped[int] = db.mapped_column(db.Integer(), nullable=True, default=0)
    last_repetition: db.Mapped[datetime] = db.mapped_column(db.DateTime(), nullable=True, default=0)
    next_repetition: db.Mapped[datetime] = db.mapped_column(db.DateTime(), nullable=True, default=0)
    inter_repetition_interval: db.Mapped[int] = db.mapped_column(db.Integer(), nullable=True, default=0)

    card_type: db.Mapped["CardType"] = db.relationship()
    deck: db.Mapped["Deck"] = db.relationship(back_populates="card")
    user: db.Mapped["User"] = db.relationship(back_populates="card")

    def __repr__(self):
        return f"Card id: {self.id}, side_1: {self.side_1}, weights: {self.weights}\n"
