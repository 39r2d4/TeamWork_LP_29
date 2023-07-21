from flask import session

def test_create_card_page(client, auth):
    with client:
        auth.login()
        response = client.get('/cards/new')
        print(response)
        assert '<label for="side_1">Лицо</label>'.encode('UTF-8') in response.data
        assert response.status_code == 200


    
    