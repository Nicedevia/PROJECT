from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_create_vitesse():
    capteur_id = str(uuid.uuid4())
    response = client.post("/vitesse/", json={
        "date": "2023-01-01T00:00:00",
        "capteur_id": capteur_id,
        "vitesse": 50.5
    })
    assert response.status_code == 200

def test_get_vitesse():
    capteur_id = str(uuid.uuid4())
    client.post("/vitesse/", json={
        "date": "2023-01-01T00:00:00",
        "capteur_id": capteur_id,
        "vitesse": 50.5
    })
    response = client.get(f"/vitesse/{capteur_id}/2023-01-01T00:00:00")
    assert response.status_code == 200
    assert response.json() == {
        "date": "2023-01-01T00:00:00",
        "capteur_id": capteur_id,
        "vitesse": 50.5
    }

def test_update_vitesse():
    capteur_id = str(uuid.uuid4())
    client.post("/vitesse/", json={
        "date": "2023-01-01T00:00:00",
        "capteur_id": capteur_id,
        "vitesse": 50.5
    })
    response = client.put(f"/vitesse/{capteur_id}/2023-01-01T00:00:00", json={
        "vitesse": 110.0
    })
    assert response.status_code == 200



def test_delete_vitesse():
    capteur_id = str(uuid.uuid4())
    client.post("/vitesse/", json={
        "date": "2023-01-01T00:00:00",
        "capteur_id": capteur_id,
        "vitesse": 50.5
    })
    response = client.delete(f"/vitesse/{capteur_id}/2023-01-01T00:00:00")
    assert response.status_code == 200
