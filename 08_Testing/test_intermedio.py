from fastapi.testclient import TestClient
from intermedio import app, fake_db, fake_secret_token

client= TestClient(app)

def test_get_user():
    response = client.get("/users/1", headers={"x-token":"misupertoken"})
    assert response.status_code==200
    assert response.json() == {
        "id":"1", "name":"User1","email":"Username1"
    }

def test_get_user_bad_token():
    response= client.get("/users/1", headers= {"x-token":"dejamepasar"})
    assert response.status_code == 400
    assert response.json() == {"detail":"Invalid token"}

def teste_get_not_existent_user():
    response= client.get("/users/5", headers= {"x-token":"misupertoken"})
    assert response.status_code == 404
    assert response.json() == {"detail":"User not found"}

def test_create_user():
    response= client.post(
        "/users/",
        headers= {"x-token":"misupertoken"},
        json={"id":"3", "name": "name3", "email": "name3"}
    )
    assert response.status_code == 200 
    assert response.json() == {
        "id":"3", "name": "name3", "email": "name3"
    }
def test_create_user_bad_token():
    response= client.post(
        "/users/",
        headers= {"x-token":"dejameentrar"},
        json={"id":"3", "name": "name3", "email": "name3"}
    )
    assert response.status_code == 400 
    assert response.json() == {
        "detail": "Invalid token"
    }

def test_create_exist_user():
    response= client.post(
        "/users/",
        headers= {"x-token":"misupertoken"},
        json={"id":"1", "name": "username1", "email": "username1"}
    )
    assert response.status_code == 409
    assert response.json() == {
        
        "detail": "User already exist"
    }



