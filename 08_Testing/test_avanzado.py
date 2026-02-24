from fastapi.testclient import TestClient
import pytest
from avanzado import app, MockDatabase, get_db

client= TestClient(app)

#Fixtures
@pytest.fixture
def test_db():
    return MockDatabase()

@pytest.fixture
def client_with_db(test_db):
    async def override_get_db():
        yield test_db
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def sample_item():
    return{
        "id": "test1",
        "name": "Test item",
        "price" : 12.99
    }

def test_read_and_create_item(client_with_db, sample_item):
    client= client_with_db
    response= client.post ("/items/", json=sample_item)
    assert response.status_code == 200
    
    response = client.get(f"/items/{sample_item['id']}")
    assert response.status_code == 200
    assert response.json() == sample_item

def test_create_duplicate_item(client_with_db, sample_item):
    client= client_with_db
    client.post ("/items/", json=sample_item)
    response= client.post ("/items/", json=sample_item)
    assert response.status_code == 409 
    assert response.json() == {
        "detail" : "Item already exist"
    }

def get_not_exist_item(client_with_db):
    client= client_with_db
    response = client.get("/items/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_item_lifecycle(client_with_db, sample_item):
    client= client_with_db
    response= client.post ("/items/", json=sample_item)
    assert response.status_code == 200
    
    response = client.get(f"/items/{sample_item['id']}")
    assert response.status_code==200
    assert response.json()== sample_item
    
    response= client.post ("/items/", json=sample_item)
    assert response.status_code == 409
    
    