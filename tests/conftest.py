from create_content import card_types
from create_admin import create_admin
import pytest
from webapp.card.models import Card, CardType
from webapp.user.models import User

from webapp import create_app, db




@pytest.fixture()
def app():
    app = create_app(base_URI="sqlite://", secret_key="one2344123")
    app.config.update({"TESTING": True,
                       "WTF_CSRF_ENABLED": False})
    with app.app_context():
        db.create_all()
        db.session.bulk_insert_mappings(CardType, card_types, return_defaults=True)
        db.session.commit()
    create_admin("admin", "123", "example@example.com")

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