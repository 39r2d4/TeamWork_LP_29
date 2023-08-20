from create_content import card_types, decks
import pytest
from webapp.card.models import Card, CardType
from webapp.deck.models import Deck
from webapp.user.models import User

from webapp import create_app, db

def create_admin(user_name: str, password: str, email: str) -> None:
    # c какой-то версии алхимия перестала принимать app в create_all() 
    if User.query.filter(User.username == user_name).count():
        print("Пользователь с таким именем существует!")
        return

    new_user = User(username=user_name, role="Admin", email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    print(f"Создан пользователь с ID {new_user.id}")


@pytest.fixture()
def app():
    app = create_app("test_config.py")
    app.config.update({"TESTING": True,
                       "WTF_CSRF_ENABLED": False})

    with app.app_context():
        db.create_all()

        create_admin("admin", "123", "example@example.com")
        create_admin("admin2", "122", "example2@example.com")

        db.session.bulk_insert_mappings(CardType, card_types, return_defaults=True)
        db.session.commit()
        db.session.bulk_insert_mappings(Deck, decks, return_defaults=True)
        db.session.commit()



    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

#пример из доки
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="admin", password="123"):
        return self._client.post(
            "/users/login",
            data={"username": username, "password": password, "button": "Войти"}
        )

    def logout(self):
        return self._client.get('users/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
# конец примера из доки