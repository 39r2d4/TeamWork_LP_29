from webapp.user.models import User
from flask_login import login_user


def test_create_card_page(client):
    with client:
        client.post('/users/login', data={"username": 'admin', 'password': '123'})
        response = client.get('/cards/new')
        #assert '<label for="side_1">Лицо</label>'.encode('UTF-8') in response.data
        print(response)
        #assert response.status_code == 302
