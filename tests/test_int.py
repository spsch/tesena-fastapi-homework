import pytest
from fastapi.testclient import TestClient
from app.main import app, db

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    db.clear()
    yield
    db.clear()

def test_crud_lifecycle_integration():
    # 1. CREATE
    create_res = client.post("/items/", json={"name": "Karta 1", "price": 100.0})
    assert create_res.status_code == 201
    created_item = create_res.json()
    item_id = created_item["id"]
    assert created_item["name"] == "Karta 1"

    # 2. READ ONE
    read_res = client.get(f"/items/{item_id}")
    assert read_res.status_code == 200
    assert read_res.json()["id"] == item_id

    # 3. UPDATE
    update_res = client.put(f"/items/{item_id}", json={"price": 150.0})
    assert update_res.status_code == 200
    assert update_res.json()["price"] == 150.0

    # 4. READ ALL
    list_res = client.get("/items/")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    # 5. DELETE
    delete_res = client.delete(f"/items/{item_id}")
    assert delete_res.status_code == 204

    # 6. READ NON-EXISTENT (Verify Delete)
    verify_res = client.get(f"/items/{item_id}")
    assert verify_res.status_code == 404

def test_get_nonexistent_item_returns_404():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}