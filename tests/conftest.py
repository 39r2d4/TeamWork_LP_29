import pytest
from webapp.user.models import User
from webapp import create_app, db


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True,
                       # для тестов надо отключать CSRF
                       "WTF_CSRF_ENABLED": False})

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