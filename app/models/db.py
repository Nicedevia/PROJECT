from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de connexion SQLite (modifiable pour PostgreSQL/MySQL si besoin)
DATABASE_URL = "sqlite:///./users.db"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory pour gérer les connexions à la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour la déclaration des modèles
Base = declarative_base()

# Dépendance pour obtenir la session de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
