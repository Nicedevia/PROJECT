from cassandra.cluster import Cluster
import csv
import uuid
from datetime import datetime

# Configuration de la connexion
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('cassandra')  # Remplacez 'cassandra' par votre keyspace

# Fonction pour calculer l'année scolaire à partir d'une date
def calculate_annee_scolaire(date):
    year = date.year
    if date.month >= 9:  # L'année scolaire commence en septembre
        return f"{year}-{year + 1}"
    return f"{year - 1}-{year}"

# Chemin vers le fichier CSV contenant les jours fériés
file_path = 'app/donnée/joursf.csv'

# Lecture des données depuis le CSV
with open(file_path, 'r') as file:
    reader = csv.DictReader(file)
    rows = list(reader)

# Préparation et insertion des données
for row in rows:
    # Conversion de la date
    date_debut = datetime.strptime(row['date'], '%d %b %Y')  # Format corrigé
    description = row['holiday']
    evenement_id = uuid.uuid4()
    annee_scolaire = calculate_annee_scolaire(date_debut)
    type_evenement = "jour_ferie"
    zones = "Toutes"  # Zones par défaut pour les jours fériés

    # Insertion dans la table 'jours_feries_vacances'
    query_vacances = """
        INSERT INTO jours_feries_vacances (
            evenement_id, type_evenement, description, date_debut, date_fin, zones, annee_scolaire
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        session.execute(query_vacances, (
            evenement_id, type_evenement, description, date_debut, date_debut, zones, annee_scolaire
        ))
        print(f"Jour férié inséré dans 'jours_feries_vacances' : {description} ({date_debut.strftime('%Y-%m-%d')})")
    except Exception as e:
        print(f"Erreur lors de l'insertion dans 'jours_feries_vacances' de {description} : {e}")

    # Insertion dans la table 'jour_ferie'
    query_ferie = """
        INSERT INTO jour_ferie (
            date, description, zone_1, zone_2, zone_3
        ) VALUES (%s, %s, %s, %s, %s)
    """
    try:
        session.execute(query_ferie, (
            date_debut, description, True, True, True  # True pour indiquer que le jour férié s'applique à toutes les zones
        ))
        print(f"Jour férié inséré dans 'jour_ferie' : {description} ({date_debut.strftime('%Y-%m-%d')})")
    except Exception as e:
        print(f"Erreur lors de l'insertion dans 'jour_ferie' de {description} : {e}")

# Fermeture de la connexion
session.shutdown()
cluster.shutdown()

print("Tous les jours fériés ont été insérés avec succès.")
