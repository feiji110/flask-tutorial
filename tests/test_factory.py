from flaskr import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTIONG': True}).testing

def test_hello(client):
    response = client.get('/helllo')
    assert response.data == b'Hello, World!'
