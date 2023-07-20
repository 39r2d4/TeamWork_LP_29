def test_loginpage(client):
    response = client.get('/users/login')
    assert '> Зарегистрироваться </a>'.encode('UTF-8') in response.data


def test_signuppage(client):
    response = client.get('/users/signup')
    assert '''<label for="password2">Повторите пароль</label>'''.encode('UTF-8') in response.data