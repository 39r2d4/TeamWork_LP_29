def test_decks_view_page(client, auth):
    auth.login()
    response = client.get('/decks/view')
    assert response.status_code == 200
    assert b'class="list-group-item list-group-item-action"' in response.data
    
    auth.logout()
    response = client.get('/decks/view')
    assert response.status_code == 302


def test_decks_add_new_deck_page(client, auth):
    auth.login()
    response = client.get('decks/new')
    assert response.status_code == 200
    #Имя новой колоды:
    assert '<span>Имя новой колоды:</span>'.encode('UTF-8')  in response.data
    auth.logout()
    response = client.get('/decks/new')
    assert response.status_code == 302
    