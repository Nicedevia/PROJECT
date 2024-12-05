from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_create_limitation():
    capteur_id = str(uuid.uuid4())
    response = client.post("/limitation/", json={
        "capteur_id": capteur_id,
        "limitation": 120.0
    })
    assert response.status_code == 200

def test_get_limitation():
    capteur_id = str(uuid.uuid4())
    client.post("/limitation/", json={
        "capteur_id": capteur_id,
        "limitation": 120.0
    })
    response = client.get(f"/limitation/{capteur_id}")
    assert response.status_code == 200
    assert response.json() == {
        "capteur_id": capteur_id,
        "limitation": 120.0
    }

def test_update_limitation():
    capteur_id = str(uuid.uuid4())
    client.post("/limitation/", json={
        "capteur_id": capteur_id,
        "limitation": 120.0
    })
    response = client.put(f"/limitation/{capteur_id}", json={
        "limitation": 100.0  # Assurez-vous que ce nom correspond au modèle
    })
    assert response.status_code == 200



def test_delete_limitation():
    capteur_id = str(uuid.uuid4())
    client.post("/limitation/", json={
        "capteur_id": capteur_id,
        "limitation": 120.0
    })
    response = client.delete(f"/limitation/{capteur_id}")
    assert response.status_code == 200
