import pandas as pd
import os

def nettoyer_et_verifier_donnees_meteo(file_path):
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} n'existe pas.")
        return False

    try:
        # Charger les données
        df = pd.read_csv(file_path)

        # Vérifier les colonnes attendues
        colonnes_attendues = [
            'time', 'temp_c', 'condition', 'wind_kph', 'wind_dir', 'pressure_mb',
            'precip_mm', 'snow_cm', 'humidity', 'cloud', 'feelslike_c', 'windchill_c',
            'heatindex_c', 'dewpoint_c', 'will_it_rain', 'chance_of_rain', 
            'will_it_snow', 'chance_of_snow', 'gust_kph', 'uv', 'vis_km'
        ]
        if list(df.columns) != colonnes_attendues:
            print("Colonnes inattendues trouvées !")
            print("Colonnes présentes :", list(df.columns))
            print("Colonnes attendues :", colonnes_attendues)
            return False

        # Vérification des données
        lignes_invalides = []
        for index, row in df.iterrows():
            try:
                # Vérifier le format de la colonne 'time' (reste au format 'YYYY-MM-DD HH:MM')
                pd.to_datetime(row["time"], format='%Y-%m-%d %H:%M', errors='raise')

                # Vérifier que les autres colonnes sont correctement formatées
                float(row["temp_c"])
                float(row["wind_kph"])
                float(row["pressure_mb"])
                float(row["precip_mm"])
                float(row["snow_cm"])
                int(row["humidity"])
                int(row["cloud"])
                float(row["feelslike_c"])
                float(row["windchill_c"])
                float(row["heatindex_c"])
                float(row["dewpoint_c"])
                int(row["will_it_rain"])
                int(row["chance_of_rain"])
                int(row["will_it_snow"])
                int(row["chance_of_snow"])
                float(row["gust_kph"])
                float(row["uv"])
                float(row["vis_km"])

            except Exception as e:
                lignes_invalides.append((index, row.to_dict(), str(e)))

        # Supprimer les lignes invalides
        if lignes_invalides:
            print("Lignes invalides détectées et supprimées :")
            for ligne in lignes_invalides:
                print(f"Ligne {ligne[0]} : {ligne[1]} - Erreur : {ligne[2]}")
            df = df.drop([ligne[0] for ligne in lignes_invalides])

        # Sauvegarder les données nettoyées
        cleaned_file_path = file_path.replace('.csv', '_cleaned.csv')
        df.to_csv(cleaned_file_path, index=False)
        print(f"Les données nettoyées ont été sauvegardées dans : {cleaned_file_path}")
        return True

    except Exception as e:
        print(f"Erreur lors du nettoyage et de la vérification : {e}")
        return False

# Utilisation
file_path = r'C:\Users\briac\Desktop\PROJECT\app\donnée\meteodata.csv'
nettoyer_et_verifier_donnees_meteo(file_path)
