from webapp import db, create_app
from webapp.card.models import CardType

card_types = [{"name": "Основная", "description": "Базовая двусторонняя карточка"},
                {"name": "С вариантами ответов", "description": "выбрать ответ из предложеных вариантов"},
                {"name": "Основная (с обратной карточкой)", "description": "создается 2 зеркальных карточки"}]

decks = [{"name": "Колода1", "comment": "Комментарий к колоде1", "user_id": 1},
         {"name": "Колода2", "comment": "Комментарий к колоде2", "user_id": 1},
         {"name": "Колода3", "comment": "Комментарий к колоде3", "user_id": 1},
         {"name": "Deck4", "comment": "Комментарий к колоде4", "user_id": 1},
         {"name": "Колода5 и длинное название колоды", "comment": "Комментарий к колоде5", "user_id": 1},
         {"name": "6", "comment": "К6", "user_id": 1},
         {"name": "Колода7", "comment": "Комментарий к колоде7", "user_id": 1},
         {"name": "Колода8", "comment": "Комментарий к колоде8", "user_id": 1},
         {"name": "Колода1", "comment": "Комментарий к колоде1", "user_id": 2},
         {"name": "Колода2_пользователь2", "comment": "Комментарий к колоде2", "user_id": 2},
         {"name": "Колода3", "comment": "Комментарий к колоде3", "user_id": 2}]



if __name__ == "__main__":

    app = create_app()

    # c какой-то версии алхимия перестала принимать app в reate_all()
    with app.app_context():
        db.session.bulk_insert_mappings(CardType, card_types, return_defaults=True)
        db.session.commit()
        print(card_types)
