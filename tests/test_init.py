
# нужно проверять и для зарегистрированных и для незарегистрированных пользователей
def test_homepage(client):
    response = client.get('/')
    assert '<h2> Зарегистрируйтесь чтобы начать пользоваться приложением</h2>'.encode('UTF-8') in response.data


