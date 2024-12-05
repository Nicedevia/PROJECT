from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
import csv
from concurrent.futures import ThreadPoolExecutor
# from utils.uuid_generator import generate_deterministic_uuid  # Importer la fonction
import sys
import os

import uuid
from hashlib import sha256

def generate_deterministic_uuid(latitude, longitude):
    """
    Génère un UUID déterministe basé sur les valeurs de latitude et longitude.
    """
    # Combine latitude et longitude pour créer un hash unique
    hash_input = f"{latitude},{longitude}".encode('utf-8')
    # Crée un UUID à partir du hash SHA256
    return uuid.UUID(sha256(hash_input).hexdigest()[:32])

# Configuration de la connexion
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('cassandra')

# Fonction d'insertion d'un batch avec gestion des erreurs
def insert_batch(rows):
    """
    Insère un lot de données dans la table limitation.
    """
    batch = BatchStatement()
    prepared_stmt = session.prepare("""
        INSERT INTO limitation (capteur_id, latitude, longitude, limitation)
        VALUES (?, ?, ?, ?)
    """)
    for row in rows:
        # Générer un UUID déterministe
        capteur_id = generate_deterministic_uuid(row["Latitude"], row["Longitude"])
        batch.add(prepared_stmt, (
            capteur_id,
            float(row["Latitude"]),
            float(row["Longitude"]),
            int(row["Limitation de Vitesse"])
        ))
    
    try:
        session.execute(batch)
        print(f"Batch de {len(rows)} lignes inséré avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion d'un batch : {e}")

# Chargement des données depuis le CSV
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = file_path = "C:/Users/briac/Desktop/PROJECT/app/donnée/nice_speed_limitssmall.csv"

with open(file_path, 'r') as file:
    reader = csv.DictReader(file)
    rows = list(reader)


# Diviser les données en groupes de 100 lignes par batch
batch_size = 100
batches = [rows[i:i + batch_size] for i in range(0, len(rows), batch_size)]

# Insertion avec exécution parallèle et suivi
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(insert_batch, batches)

# Fermeture de la session et du cluster
session.shutdown()
cluster.shutdown()

print("Insertion terminée pour toutes les données.")
