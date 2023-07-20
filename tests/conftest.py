import pytest
from webapp.user.models import User
from webapp import create_app, db


@pytest.fixture()
def app():
    app = create_app()


    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
