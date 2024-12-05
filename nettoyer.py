from cassandra.cluster import Cluster

# Connexion à la base de données Cassandra
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('cassandra')  # Remplacez 'cassandra' par votre keyspace si nécessaire

# Liste des tables que vous souhaitez vider
tables_to_truncate = ['limitation', 'vitesse', 'jour_ferie', 'meteo']

# Exécution de la commande TRUNCATE pour chaque table
for table in tables_to_truncate:
    session.execute(f"TRUNCATE {table}")
    print(f"La table '{table}' a été vidée avec succès.")

print("Toutes les tables ont été vidées.")

