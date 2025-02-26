import pytest
from sqlalchemy.orm import Session
from app.models.db import SessionLocal
from app.models.models import User

@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    """Réinitialiser la table `users` avant chaque test."""
    db: Session = SessionLocal()
    try:
        db.query(User).delete()  # Supprime tous les utilisateurs
        db.commit()
    finally:
        db.close()
