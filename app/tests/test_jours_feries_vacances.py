from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_create_vacance():
    response = client.post("/jours_feries_vacances/", json={
        "evenement_id": str(uuid.uuid4()),  # Assurez-vous que cet ID est bien un UUID
        "description": "Vacances d'Été",
        "date_debut": "2025-07-05T00:00:00",
        "date_fin": "2025-09-01T00:00:00",
        "zones": "Zone A",
        "annee_scolaire": "2024-2025",
        "type_evenement": "vacances"
    })
    assert response.status_code == 200

def test_get_vacance():
    evenement_id = str(uuid.uuid4())
    post_response = client.post("/jours_feries_vacances/", json={
        "evenement_id": evenement_id,
        "description": "Vacances de Printemps",
        "date_debut": "2025-04-19T00:00:00",
        "date_fin": "2025-05-05T00:00:00",
        "zones": "Zone A",
        "annee_scolaire": "2024-2025",
        "type_evenement": "vacances"
    })
    assert post_response.status_code == 200  # Vérifiez que la création fonctionne
    response = client.get(f"/jours_feries_vacances/{evenement_id}")
    assert response.status_code == 200  # Vérifiez que la récupération fonctionne
    assert response.json()["description"] == "Vacances de Printemps"

def test_update_vacance():
    evenement_id = str(uuid.uuid4())
    client.post("/jours_feries_vacances/", json={
        "evenement_id": evenement_id,
        "description": "Vacances d'Hiver",
        "date_debut": "2025-02-15T00:00:00",
        "date_fin": "2025-02-28T00:00:00",
        "zones": "Zone B",
        "annee_scolaire": "2024-2025",
        "type_evenement": "vacances"
    })
    response = client.put(f"/jours_feries_vacances/{evenement_id}", json={
        "description": "Vacances de Février",
        "date_debut": "2025-02-16T00:00:00",
        "date_fin": "2025-02-27T00:00:00",
        "zones": "Zone B",
        "annee_scolaire": "2024-2025",
        "type_evenement": "vacances"
    })
    assert response.status_code == 200

def test_delete_vacance():
    evenement_id = str(uuid.uuid4())
    client.post("/jours_feries_vacances/", json={
        "evenement_id": evenement_id,
        "description": "Vacances de Noël",
        "date_debut": "2025-12-20T00:00:00",
        "date_fin": "2026-01-05T00:00:00",
        "zones": "Zone C",
        "annee_scolaire": "2025-2026",
        "type_evenement": "vacances"
    })
    response = client.delete(f"/jours_feries_vacances/{evenement_id}")
    assert response.status_code == 200
