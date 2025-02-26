import sqlite3
from passlib.context import CryptContext

# Configuration de PassLib pour gérer les mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Nom du fichier de la base de données
DB_FILE = "users.db"

# Fonction pour établir la connexion à SQLite
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")  # Activation des clés étrangères (utile pour d'autres relations)
    return conn

# Création de la table `users` si elle n'existe pas déjà
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Fonction pour hacher un mot de passe
def hash_password(password):
    return pwd_context.hash(password)

# Fonction pour ajouter un utilisateur
def add_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print(f"✅ Utilisateur '{username}' ajouté avec succès.")
    except sqlite3.IntegrityError:
        print(f"⚠️ L'utilisateur '{username}' existe déjà.")
    
    conn.close()

# Fonction pour supprimer un utilisateur
def delete_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    print(f"✅ Utilisateur '{username}' supprimé avec succès.")

# Fonction pour lister tous les utilisateurs
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    
    conn.close()

    if users:
        print("📋 Liste des utilisateurs :")
        for user in users:
            print(f"- {user[0]}")
    else:
        print("⚠️ Aucun utilisateur enregistré.")

# Fonction pour récupérer un utilisateur spécifique
def get_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    conn.close()
    return user

# Fonction principale
if __name__ == "__main__":
    init_db()  # Assurer que la base de données est créée

    print("\n🔹 Gestion des utilisateurs")
    print("1️⃣ Ajouter un utilisateur")
    print("2️⃣ Supprimer un utilisateur")
    print("3️⃣ Lister les utilisateurs")
    choix = input("📌 Faites votre choix : ")

    if choix == "1":
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe : ")
        add_user(username, password)
    elif choix == "2":
        username = input("Nom d'utilisateur à supprimer : ")
        delete_user(username)
    elif choix == "3":
        list_users()
    else:
        print("⚠️ Choix invalide.")
