def test_create_card_page(client, auth):
    with client:
        auth.login()
        response = client.get('/cards/new')
        print(response)
        assert response.status_code == 200
        assert '<label for="side_1">Лицо</label>'.encode('UTF-8') in response.data

        auth.logout()
        response = client.get('/cards/new')
        assert response.status_code == 302
