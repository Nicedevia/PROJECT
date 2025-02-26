import pandas as pd

df = pd.read_csv(r'C:\Users\briac\Desktop\project finnal\part1\datag\data_vacances\fr-en-calendrier-scolaire.csv', delimiter=';')

df_filtered = df[df['annee_scolaire'].isin(['2024-2025', '2025'])]

df_filtered = df_filtered.sort_values(by='annee_scolaire', ascending=False)
df_unique = df_filtered.drop_duplicates(subset=['Zones', 'Description'], keep='first')

columns_to_keep = ['Description', 'Date de début', 'Date de fin', 'Zones', 'annee_scolaire']
df_cleaned = df_unique[columns_to_keep]

df_cleaned = df_cleaned.fillna('Non renseigné')

df_cleaned['Date de début'] = pd.to_datetime(df_cleaned['Date de début'], errors='coerce')
df_cleaned['Date de fin'] = pd.to_datetime(df_cleaned['Date de fin'], errors='coerce')

df_cleaned.to_csv(r'C:\Users\briac\Desktop\project finnal\part1\datag\data_vacances\fr-en-calendrier-scolaire-filtrer.csv', index=False, sep=';')

print("Les données ont été filtrées, nettoyées et sauvegardées avec succès.")
