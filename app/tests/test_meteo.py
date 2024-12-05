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

import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_update_meteo():
    capteur_id = str(uuid.uuid4())
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Créer une entrée initiale
        post_response = await client.post("/meteo/", json={
            "date": "2023-01-01T00:00:00",
            "capteur_id": capteur_id,
            "visibilite": 75.0,
            "precipitation": 12.5
        })
        assert post_response.status_code == 200  # Vérifiez que l'entrée a été créée

        # Mettre à jour l'entrée
        put_response = await client.put(f"/meteo/{capteur_id}/2023-01-01T00:00:00", json={
            "visibilite": 80.0,
            "precipitation": 10.0
        })
        assert put_response.status_code == 200  # Vérifiez que l'entrée a été mise à jour
        assert put_response.json()["visibilite"] == 80.0
        assert put_response.json()["precipitation"] == 10.0


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
