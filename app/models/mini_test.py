from sqlalchemy import create_engine
import os

DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

if os.path.exists("users.db"):
    print("✅ Connexion réussie à SQLite !")
else:
    print("❌ Échec de connexion à SQLite.")
