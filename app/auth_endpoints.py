from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
import os
import json
from passlib.context import CryptContext

USERS_FILE = os.path.join("app", "data", "users.json")


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            users = json.load(file)
            print("Données chargées depuis users.json :", users)  # Ajoute ce log
            return users
    return {}



auth_router = APIRouter()

@auth_router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Tentative de connexion : {form_data.username}")
    user = authenticate_user(form_data.username, form_data.password)
    print("toto", user)
    if not user:
        print("Échec de l'authentification")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print("Authentification réussie")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/test")
async def test_route():
    """Route de test pour vérifier si l'authentification est configurée."""
    return {"message": "Authentication route works!"}

@auth_router.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    """Exemple de route protégée."""
    return {"message": f"Bienvenue, {current_user['username']}!"}

# Initialisation des utilisateurs
users_db = load_users()

@auth_router.get("/debug/users")
async def get_all_users():
    return users_db

