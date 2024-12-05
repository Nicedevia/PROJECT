from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
import csv
from concurrent.futures import ThreadPoolExecutor
import os
import uuid
from hashlib import sha256

def generate_deterministic_uuid(latitude, longitude):
    """
    Génère un UUID déterministe basé sur les valeurs de latitude et longitude.
    """
    hash_input = f"{latitude},{longitude}".encode('utf-8')
    return uuid.UUID(sha256(hash_input).hexdigest()[:32])


# Configuration de la connexion
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('cassandra')

# Variables pour compter les lignes
total_lignes = 0
lignes_inserees = 0
lignes_ignores = 0

# Fonction d'insertion d'un batch avec gestion des erreurs
def insert_batch(rows):
    """
    Insère un lot de données dans la table limitation.
    """
    global lignes_inserees, lignes_ignores
    batch = BatchStatement()
    prepared_stmt = session.prepare("""
        INSERT INTO limitation (capteur_id, latitude, longitude, limitation)
        VALUES (?, ?, ?, ?)
    """)
    for row in rows:
        try:
            # Générer un UUID déterministe
            capteur_id = generate_deterministic_uuid(row["Latitude"], row["Longitude"])
            batch.add(prepared_stmt, (
                capteur_id,
                float(row["Latitude"]),
                float(row["Longitude"]),
                int(row["Limitation de Vitesse"])
            ))
        except ValueError as e:
            print(f"Données invalides : {row}, Erreur : {e}")
            lignes_ignores += 1
            continue  # Passer à la prochaine ligne
    
    try:
        session.execute(batch)
        lignes_inserees += len(rows) - lignes_ignores
        print(f"Batch de {len(rows)} lignes inséré avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion d'un batch : {e}")


# Chargement des données depuis le CSV
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = "C:/Users/briac/Desktop/PROJECT/app/donnée/nice_speed_limits_cleaned.csv"

with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    rows = list(reader)
    total_lignes = len(rows)

    # Vérification des colonnes attendues
    colonnes_attendues = ['Latitude', 'Longitude', 'Limitation de Vitesse']
    if list(reader.fieldnames) != colonnes_attendues:
        print(f"Colonnes trouvées : {reader.fieldnames}")
        print("Le fichier CSV ne correspond pas au format attendu.")
        session.shutdown()
        cluster.shutdown()
        exit(1)

# Diviser les données en groupes de 100 lignes par batch
batch_size = 100
batches = [rows[i:i + batch_size] for i in range(0, len(rows), batch_size)]

# Insertion avec exécution parallèle et suivi
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(insert_batch, batches)

# Fermeture de la session et du cluster
session.shutdown()
cluster.shutdown()

# Résumé final
print("\n=== Résumé de l'insertion ===")
print(f"Total de lignes dans le fichier : {total_lignes}")
print(f"Lignes insérées avec succès : {lignes_inserees}")
print(f"Lignes ignorées en raison d'erreurs : {lignes_ignores}")
