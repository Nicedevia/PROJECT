from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import os
import json

# Clé secrète et configuration
SECRET_KEY = "a_very_secure_and_random_secret_key_123456"  # Remplacez par une clé sécurisée
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Définir le chemin du fichier JSON
USERS_FILE = os.path.join("app", "data", "users.json")

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            users = json.load(file)
            print("Données chargées depuis users.json :", users)  # Ajoute ce log
            return users
    return {}

# Initialisation des utilisateurs
users_db = load_users()

# Configuration de PassLib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Vérifier le mot de passe
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    print(f"Tentative d'authentification pour l'utilisateur : {username}")
    user = users_db.get(username)
    if not user:
        print(f"Utilisateur {username} introuvable.")
        return None
    print(f"Utilisateur trouvé : {user}")
    if not verify_password(password, user["hashed_password"]):
        print(f"Le mot de passe pour {username} est incorrect.")
        return None
    print(f"Authentification réussie pour l'utilisateur : {username}")
    return user



# Créer un token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    print(f"Création d'un token avec les données : {to_encode}")  # Ajout de logs
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Obtenir l'utilisateur actuel depuis le token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        user = users_db.get(username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
