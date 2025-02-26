from sqlalchemy.orm import Session
from models import Utilisateur, Role
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hachage du mot de passe
def hash_password(password):
    return pwd_context.hash(password)

# Ajouter un utilisateur
def add_user(db: Session, username: str, email: str, password: str, role_id: int):
    user = Utilisateur(
        id=str(uuid.uuid4()),
        username=username,
        email=email,
        password=hash_password(password),
        role_id=role_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Récupérer tous les utilisateurs
def get_users(db: Session):
    return db.query(Utilisateur).all()

# Supprimer un utilisateur
def delete_user(db: Session, username: str):
    user = db.query(Utilisateur).filter(Utilisateur.username == username).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
