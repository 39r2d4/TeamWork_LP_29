def test_create_card_page(client):
    response = client.get('/cards/new')
    assert '<label for="side_1">Лицо</label>'.encode('UTF-8') in response.data