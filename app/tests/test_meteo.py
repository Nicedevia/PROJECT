from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_create_meteo():
    capteur_id = str(uuid.uuid4())
    response = client.post("/meteo/", json={
        "date": "2023-01-01T00:00:00",
        "capteur_id": capteur_id,
        "visibilite": 75.0,
        "precipitation": 12.5
    })
    assert response.status_code == 200

def test_get_meteo():
    capteur_id = str(uuid.uuid4())
    client.post("/meteo/", json={
        "date": "2023-01-01T00:00:00",
        "capteur_id": capteur_id,
        "visibilite": 75.0,
        "precipitation": 12.5
    })
    response = client.get(f"/meteo/{capteur_id}/2023-01-01T00:00:00")
    assert response.status_code == 200
    assert response.json() == {
        "date": "2023-01-01T00:00:00",
        "capteur_id": capteur_id,
        "visibilite": 75.0,
        "precipitation": 12.5
    }

def test_update_meteo():
    capteur_id = str(uuid.uuid4())
    client.post("/meteo/", json={
        "date": "2023-01-01T00:00:00",
        "capteur_id": capteur_id,
        "visibilite": 75.0,
        "precipitation": 12.5
    })
    response = client.put(f"/meteo/{capteur_id}/2023-01-01T00:00:00", json={
        "visibilite": 80.0,
        "precipitation": 10.0
    })
    assert response.status_code == 200



def test_delete_meteo():
    capteur_id = str(uuid.uuid4())
    client.post("/meteo/", json={
        "date": "2023-01-01T00:00:00",
        "capteur_id": capteur_id,
        "visibilite": 75.0,
        "precipitation": 12.5
    })
    response = client.delete(f"/meteo/{capteur_id}/2023-01-01T00:00:00")
    assert response.status_code == 200
