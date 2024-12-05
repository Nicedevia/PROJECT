from cassandra.cluster import Cluster
import uuid
from datetime import datetime, timedelta
import random

# Configuration de la connexion à Cassandra
cluster = Cluster(['127.0.0.1'], port=9042)  # Remplacez l'adresse IP si nécessaire
session = cluster.connect('cassandra')  # Remplacez 'cassandra' par votre keyspace

# Fonction pour générer une date aléatoire entre deux dates
def random_date(start, end):
    """
    Génère une date aléatoire entre deux dates spécifiées.
    """
    delta = end - start
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86400 - 1)  # Nombre de secondes dans une journée
    return start + timedelta(days=random_days, seconds=random_seconds)

# Générer des données aléatoires pour 10 enregistrements
start_date = datetime(2024, 1, 1)  # Date de début
end_date = datetime(2024, 12, 31)  # Date de fin

for _ in range(10):
    capteur_id = uuid.uuid4()  # Génération d'un UUID aléatoire
    date = random_date(start_date, end_date)  # Date aléatoire
    vitesse = round(random.uniform(30.0, 130.0), 1)  # Vitesse aléatoire entre 30.0 et 130.0 km/h

    # Requête d'insertion
    query = """
        INSERT INTO vitesse (capteur_id, date, vitesse)
        VALUES (%s, %s, %s)
    """
    try:
        session.execute(query, (capteur_id, date, vitesse))
        print(f"Enregistrement inséré : capteur_id={capteur_id}, date={date}, vitesse={vitesse}")
    except Exception as e:
        print(f"Erreur lors de l'insertion : {e}")

# Fermeture de la session et du cluster
session.shutdown()
cluster.shutdown()

print("Insertion aléatoire terminée pour la table 'vitesse'.")
