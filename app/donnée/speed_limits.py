import csv
import json
import uuid
import re  # Importez la bibliothèque pour utiliser des expressions régulières

# Chemin du fichier CSV en entrée et du fichier JSON en sortie
csv_file_path = 'donnée/nice_speed_limitssmall.csv'
json_file_path = 'donnée/speed_limits.json'

# Fonction pour nettoyer la limitation de vitesse
def parse_speed_limit(limit_str):
    # Utilisez une expression régulière pour extraire les chiffres de la chaîne
    match = re.search(r'\d+', limit_str)
    return int(match.group()) if match else None

# Charger les données depuis le fichier CSV
with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    speed_limits = []

    # Créer un enregistrement JSON avec un UUID pour chaque ligne
    for row in csv_reader:
        limitation = parse_speed_limit(row["Limitation de Vitesse"])
        if limitation is not None:  # Ignorez les lignes sans limitation valide
            speed_limits.append({
                "capteur_id": str(uuid.uuid4()),  # Générer un UUID unique pour chaque capteur
                "latitude": float(row["Latitude"]),
                "longitude": float(row["Longitude"]),
                "limitation": limitation
            })

# Enregistrer les données en JSON
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(speed_limits, json_file, indent=4)

print("Les données ont été converties en JSON avec des UUIDs pour chaque capteur.")
