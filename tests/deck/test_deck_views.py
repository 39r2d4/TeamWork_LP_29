def test_decks_view_page(client, auth):
    auth.login()
    response = client.get('/decks/view')
    assert response.status_code == 200
    assert b'class="list-group-item list-group-item-action"' in response.data
    
    auth.logout()
    response = client.get('/decks/view')
    assert response.status_code == 302
