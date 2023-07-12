from webapp import db, create_app
from webapp.card.models import CardType


if __name__ == "__main__":
    card_types = [{"name": "Основная", "description": "Базовая двусторонняя карточка"},
                  {"name": "С вариантами ответов", "description": "выбрать ответ из предложеных вариантов"},
                  {"name": "Основная (с обратной карточкой)", "description": "создается 2 зеркальных карточки"}]

    app = create_app()

    # c какой-то версии алхимия перестала принимать app в reate_all()
    with app.app_context():
        db.session.bulk_insert_mappings(CardType, card_types, return_defaults=True)
        db.session.commit()
        print(card_types)
