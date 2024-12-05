from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_jour_ferie():
    response = client.post("/jour_ferie/", json={
        "date": "2023-12-25T00:00:00",
        "description": "Noël",
        "zone_1": True,
        "zone_2": False,
        "zone_3": True
    })
    assert response.status_code == 200

def test_get_jour_ferie():
    # Assurez-vous que le jour férié est créé pour pouvoir le récupérer
    client.post("/jour_ferie/", json={
        "date": "2023-12-25T00:00:00",
        "description": "Noël",
        "zone_1": True,
        "zone_2": False,
        "zone_3": True
    })
    response = client.get("/jour_ferie/2023-12-25T00:00:00")
    assert response.status_code == 200
    assert response.json() == {
        "date": "2023-12-25T00:00:00",
        "description": "Noël",
        "zone_1": True,
        "zone_2": False,
        "zone_3": True
    }

def test_update_jour_ferie():
    client.post("/jour_ferie/", json={
        "date": "2023-12-25T00:00:00",
        "description": "Noël",
        "zone_1": True,
        "zone_2": False,
        "zone_3": True
    })
    response = client.put("/jour_ferie/2023-12-25T00:00:00", json={
        "date": "2023-12-25T00:00:00",
        "description": "Fête de Noël",
        "zone_1": False,
        "zone_2": True,
        "zone_3": True
    })
    assert response.status_code == 200

def test_delete_jour_ferie():
    client.post("/jour_ferie/", json={
        "date": "2023-12-25T00:00:00",
        "description": "Noël",
        "zone_1": True,
        "zone_2": False,
        "zone_3": True
    })
    response = client.delete("/jour_ferie/2023-12-25T00:00:00")
    assert response.status_code == 200


