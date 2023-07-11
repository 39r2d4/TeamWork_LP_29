from webapp import db, create_app
from webapp.card.models import CardType


if __name__ == "__main__":
    card_types = [{"name": "Обачная карточка_fromDB", "description": "Базовая карточка(описание1)"},
                  {"name": "Викторина_fromDB", "description": "выюрать ответ из предложеных вариантов"},
                  {"name": "С обратной по выбору_fromDB", "description": "создается 2 связанных карточки"}]

    app = create_app()

    # c какой-то версии алхимия перестала принимать app в reate_all()
    with app.app_context():
        db.session.bulk_insert_mappings(CardType, card_types, return_defaults=True)
        db.session.commit()
        print(card_types)
