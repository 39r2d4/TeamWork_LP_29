from webapp.model import db


class Deck(db.Model):
    __tablename__ = "deck_table"
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True)
    name: db.Mapped[str] = db.mapped_column(db.String(128), index=True)

    comment: db.Mapped[str] = db.mapped_column(db.String(128), nullable=True, default='')
    user_id: db.Mapped[int] = db.mapped_column(db.ForeignKey("user_teble.id"), index=True)

    user: db.Mapped["User"] = db.relationship(back_populates="deck")
    card: db.Mapped[list["Card"]] = db.relationship(back_populates="deck",
                                                    cascade='all, delete')

    def __repr__(self):
        return f"Deck id: {self.id}, name: {self.name}"
