def test_decks_view_page(client):
    response = client.get('/decks/view')
    assert b'class="list-group-item list-group-item-action"' in response.data
