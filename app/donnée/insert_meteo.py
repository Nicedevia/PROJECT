from cassandra.cluster import Cluster
import csv
import uuid
from datetime import datetime

# Connexion à Cassandra
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('cassandra')

# Préparer l'insertion
insert_meteo = session.prepare("""
    INSERT INTO meteo (capteur_id, date, precipitation, visibilite)
    VALUES (?, ?, ?, ?)
""")

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M")

# Lire et insérer les données
with open('app/donnée/meteodata.csv', 'r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        try:
            capteur_id = uuid.uuid4()  # ID unique pour chaque entrée
            date = parse_date(row["time"])
            precipitation = float(row["precip_mm"])
            visibilite = float(row["vis_km"])

            session.execute(insert_meteo, (capteur_id, date, precipitation, visibilite))
        
        except Exception as e:
            print(f"Erreur lors de l'insertion : {e}")

print("Les données météo ont été insérées avec succès.")
