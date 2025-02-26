from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_create_user():
    """Test la création d'un utilisateur"""
    response = client.post("/users/", json={
        "username": "test_user",
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert "id" in response.json()  # Vérifie que l'ID est renvoyé
    return response.json()["id"]

def test_get_user():
    """Test la récupération d'un utilisateur"""
    user_id = test_create_user()
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"
    assert response.json()["email"] == "test@example.com"

def test_update_user():
    """Test la mise à jour d'un utilisateur"""
    user_id = test_create_user()
    response = client.put(f"/users/{user_id}", json={
        "username": "updated_user",
        "email": "updated@example.com",
        "password": "newpassword"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "updated_user"
    assert response.json()["email"] == "updated@example.com"

def test_delete_user():
    """Test la suppression d'un utilisateur"""
    user_id = test_create_user()  # Création d'un utilisateur test
    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 200  # Vérifie que la requête est bien acceptée

    # Vérifie que le message contient bien "Utilisateur supprimé avec succès"
    expected_message = "Utilisateur supprimé avec succès"
    actual_message = response.json()["message"]

    assert "Utilisateur" in actual_message and "supprimé avec succès" in actual_message, f"Message reçu : {actual_message}"

import uuid

def test_create_role():
    """Test la création d'un rôle"""
    unique_role_name = "Admin_" + uuid.uuid4().hex[:8]
    response = client.post("/users/role/", json={"name": unique_role_name})
    assert response.status_code == 200
    assert "id" in response.json()
    return response.json()["id"]


def test_assign_role():
    """Test l'assignation d'un rôle à un utilisateur"""
    user_id = test_create_user()
    role_id = test_create_role()  # Utilise un rôle unique

    response = client.post(f"/users/{user_id}/assign-role/{role_id}")
    assert response.status_code == 200
    # On peut vérifier que la réponse contient les IDs
    data = response.json()
    assert data["user_id"] == user_id
    assert data["role_id"] == role_id

def test_get_user_roles():
    """Test la récupération des rôles d'un utilisateur"""
    user_id = test_create_user()
    role_id = test_create_role()
    client.post(f"/users/{user_id}/assign-role/{role_id}")

    response = client.get(f"/users/{user_id}/roles")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(role["id"] == role_id for role in response.json())
