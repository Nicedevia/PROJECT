import pandas as pd
import re
import os

def nettoyer_et_verifier_donnees_limitations(file_path):
    """
    Vérifie et nettoie les données des limitations de vitesse depuis un fichier CSV.

    Args:
        file_path (str): Chemin vers le fichier CSV à vérifier et nettoyer.

    Returns:
        str: Chemin vers le fichier nettoyé.
    """
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} n'existe pas.")
        return None

    try:
        # Charger le fichier CSV
        df = pd.read_csv(file_path, header=0)

        # Vérifier les colonnes attendues
        colonnes_attendues = ['Latitude', 'Longitude', 'Limitation de Vitesse']
        if list(df.columns) != colonnes_attendues:
            print(f"Colonnes attendues : {colonnes_attendues}")
            print(f"Colonnes trouvées : {list(df.columns)}")
            print("Les colonnes du fichier ne correspondent pas au format attendu.")
            return None

        # Nettoyage : Validation des coordonnées et limitation de vitesse
        valid_rows = []
        invalid_rows = []

        for index, row in df.iterrows():
            try:
                latitude = float(row["Latitude"])
                longitude = float(row["Longitude"])
                limitation = re.sub(r"[^\d.]", "", str(row["Limitation de Vitesse"]))

                # Vérifier les limites géographiques et convertir la limitation en entier
                if (-90 <= latitude <= 90) and (-180 <= longitude <= 180):
                    limitation = int(float(limitation))  # Convertir en entier
                    valid_rows.append({"Latitude": latitude, "Longitude": longitude, "Limitation de Vitesse": limitation})
                else:
                    raise ValueError("Coordonnées invalides")
            except Exception as e:
                invalid_rows.append(row)
                print(f"Ligne invalide : {row.to_dict()}, Erreur : {e}")

        # Création de DataFrames pour les lignes valides et invalides
        df_valid = pd.DataFrame(valid_rows)
        df_invalid = pd.DataFrame(invalid_rows)

        # Sauvegarde des données nettoyées
        cleaned_file_path = file_path.replace('.csv', '_cleaned.csv')
        invalid_file_path = file_path.replace('.csv', '_invalid.csv')

        df_valid.to_csv(cleaned_file_path, index=False, sep=";", encoding="utf-8")
        print(f"Fichier nettoyé et sauvegardé avec succès à : {cleaned_file_path}")

        if not df_invalid.empty:
            df_invalid.to_csv(invalid_file_path, index=False, sep=";", encoding="utf-8")
            print(f"Lignes invalides sauvegardées à : {invalid_file_path}")

        return cleaned_file_path

    except Exception as e:
        print(f"Erreur lors du nettoyage et de la vérification des données : {e}")
        return None

# Utilisation
file_path = "C:/Users/briac/Desktop/PROJECT/app/donnée/nice_speed_limits.csv"
nettoyer_et_verifier_donnees_limitations(file_path)
