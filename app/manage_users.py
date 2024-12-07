import os
import json
from passlib.context import CryptContext

# Configuration de PassLib pour gérer les mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Définir le chemin du fichier JSON
USERS_FILE = os.path.join("app", "data", "users.json")

def hash_password(password):
    """Hache un mot de passe."""
    return pwd_context.hash(password)

def load_users():
    """Charge les utilisateurs depuis le fichier JSON."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    """Sauvegarde les utilisateurs dans le fichier JSON."""
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Charger les utilisateurs au démarrage
users_db = load_users()

def add_user(username, password):
    """Ajoute un utilisateur."""
    if username in users_db:
        print(f"L'utilisateur '{username}' existe déjà.")
    else:
        users_db[username] = {"username": username, "hashed_password": hash_password(password)}
        save_users(users_db)
        print(f"Utilisateur '{username}' ajouté avec succès.")

def delete_user(username):
    """Supprime un utilisateur."""
    if username in users_db:
        del users_db[username]
        save_users(users_db)
        print(f"Utilisateur '{username}' supprimé avec succès.")
    else:
        print(f"L'utilisateur '{username}' n'existe pas.")

def list_users():
    """Liste tous les utilisateurs."""
    if users_db:
        print("Liste des utilisateurs :")
        for user in users_db.keys():
            print(f"- {user}")
    else:
        print("Aucun utilisateur enregistré.")

if __name__ == "__main__":
    print("Gestion des utilisateurs")
    print("1. Ajouter un utilisateur")
    print("2. Supprimer un utilisateur")
    print("3. Lister les utilisateurs")
    choix = input("Choix : ")

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
        print("Choix invalide.")
