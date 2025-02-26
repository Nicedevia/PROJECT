from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base  # Assure-toi que 'User' est bien déclaré ici

# 📌 Forcer l'utilisation de `users.db`
DATABASE_URL = "sqlite:///users.db"

# Création de l'engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Créer toutes les tables dans la base de données"""
    print("🚀 Initialisation de la base de données...")
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données et tables créées avec succès !")

if __name__ == "__main__":
    init_db()
