from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.db import SessionLocal
from app.models import models, schemas
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dépendance pour obtenir la session de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### ✅ Route pour créer un utilisateur
@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Vérifie si l'utilisateur existe déjà
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

### ✅ Route pour récupérer un utilisateur par ID
@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

### ✅ Route pour mettre à jour un utilisateur
@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    db_user.username = user_update.username
    db_user.email = user_update.email
    db_user.is_active = user_update.is_active
    
    db.commit()
    db.refresh(db_user)
    return db_user

### ✅ Route pour supprimer un utilisateur
@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    db.delete(db_user)
    db.commit()
    return {"message": f"Utilisateur {user_id} supprimé avec succès"}

### ✅ Route pour créer un rôle
@router.post("/role/", response_model=schemas.RoleResponse)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    if db.query(models.Role).filter(models.Role.name == role.name).first():
        raise HTTPException(status_code=400, detail="Ce rôle existe déjà")

    new_role = models.Role(name=role.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@router.post("/{user_id}/assign-role/{role_id}", response_model=dict)
def assign_role(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    role = db.query(models.Role).filter(models.Role.id == role_id).first()

    if not user or not role:
        raise HTTPException(status_code=404, detail="Utilisateur ou rôle introuvable")

    if db.query(models.UserRole).filter(models.UserRole.user_id == user_id, models.UserRole.role_id == role_id).first():
        raise HTTPException(status_code=400, detail="L'utilisateur a déjà ce rôle")

    user_role = models.UserRole(user_id=user_id, role_id=role_id)
    db.add(user_role)
    db.commit()
    # Renvoie un dictionnaire contenant les IDs pour que le test puisse les vérifier
    return {"user_id": user_id, "role_id": role_id}


### ✅ Route pour récupérer les rôles d'un utilisateur
@router.get("/{user_id}/roles", response_model=list[schemas.RoleResponse])
def get_user_roles(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    roles = db.query(models.Role).join(models.UserRole).filter(models.UserRole.user_id == user_id).all()
    return roles
