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
    assert b'\xd0\x98\xd0\xbc\xd1\x8f \xd0\xbd\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb9 \xd0\xba\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb4\xd1\x8b' in response.data
    auth.logout()
    response = client.get('/decks/new')
    assert response.status_code == 302
    