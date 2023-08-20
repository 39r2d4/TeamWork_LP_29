import json

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

# не самый лучший пример теста
def test_crate_edit_delete_card(client, auth):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype}
    
    card_form_create = {"deck": "1", 
                 "side_1": "1",
                 "side_2": "1",
                 "type": "1",
                 "tags": "1",
                 "button": "Сохранить"}
    
    card_form_delete = {"deck": "1", 
                 "side_1": "1",
                 "side_2": "1",
                 "type": "1",
                 "tags": "1",
                 "delete_button": "Удалить"}
    
    auth.login()

    response = client.post("/cards/new", data=json.dumps(card_form_create), headers=headers, follow_redirects=True)

    assert response.status_code == 200
    assert 'Карточка ID: 1, лицо: 1  создана'.encode('UTF-8') in response.data


    response = client.post("/cards/edit/1", data=json.dumps(card_form_create), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert 'Карточка обновлена'.encode('UTF-8') in response.data    

    response = client.get('/cards/edit/1')
    assert response.status_code == 200

    response = client.post("/cards/edit/1", data=json.dumps(card_form_delete), headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert 'Карточка удалена'.encode('UTF-8') in response.data
