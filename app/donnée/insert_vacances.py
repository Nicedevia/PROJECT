from cassandra.cluster import Cluster
import csv
import uuid
from datetime import datetime
from pytz import timezone

# Configuration de la connexion à Cassandra
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('cassandra')

# Préparation de l'insertion avec "type_evenement" par défaut
insert_query = session.prepare("""
    INSERT INTO jours_feries_vacances (evenement_id, description, date_debut, date_fin, zones, annee_scolaire, type_evenement)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""")

# Fonction pour convertir la date en objet datetime
def parse_date(date_str):
    return datetime.fromisoformat(date_str.replace(" ", "T"))

# Lecture du fichier CSV et insertion des données
with open('app/donnée/vacances.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    print("Colonnes trouvées :", reader.fieldnames)

    for row in reader:
        try:
            session.execute(
                insert_query,
                (
                    uuid.uuid4(),
                    row["Description"],
                    parse_date(row["Date de début"]),
                    parse_date(row["Date de fin"]),
                    row["Zones"],
                    row["annee_scolaire"],
                    "vacances"  # Valeur par défaut pour "type_evenement"
                )
            )
        except Exception as e:
            print("Erreur lors de l'insertion :", e)

print("Les données ont été insérées avec succès.")
