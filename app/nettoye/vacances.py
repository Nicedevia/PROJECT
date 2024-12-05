import pandas as pd

# Chargement des données CSV
df = pd.read_csv(r'C:\Users\briac\Desktop\PROJECT\app\nettoye\fr-en-calendrier-scolaire.csv', delimiter=';')

# Filtrage par année scolaire
df_filtered = df[df['annee_scolaire'].isin(['2024-2025', '2025'])]

# Tri des données par année scolaire
df_filtered = df_filtered.sort_values(by='annee_scolaire', ascending=False)

# Suppression des doublons sur certaines colonnes
df_unique = df_filtered.drop_duplicates(subset=['Zones', 'Description'], keep='first')

# Colonnes à conserver
columns_to_keep = ['Description', 'Date de début', 'Date de fin', 'Zones', 'annee_scolaire']
df_cleaned = df_unique[columns_to_keep]

# Remplacement des valeurs manquantes
df_cleaned = df_cleaned.fillna('Non renseigné')

# Conversion des dates avec gestion explicite des erreurs et fuseaux horaires
df_cleaned['Date de début'] = pd.to_datetime(df_cleaned['Date de début'], errors='coerce', utc=True)
df_cleaned['Date de fin'] = pd.to_datetime(df_cleaned['Date de fin'], errors='coerce', utc=True)

# Exportation des données nettoyées vers un fichier CSV
df_cleaned.to_csv(r'C:\Users\briac\Desktop\PROJECT\app\donnée\vacances.csv', index=False, sep=';')

print("Les données ont été filtrées, nettoyées et sauvegardées avec succès.")
