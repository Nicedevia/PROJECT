from cassandra.cluster import Cluster

# Configuration de la connexion
CASSANDRA_HOST = '127.0.0.1'
CASSANDRA_PORT = 9042
KEYSPACE = 'cassandra'

# Connexion à Cassandra
cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
session = cluster.connect(KEYSPACE)

# Liste des tables à vider
tables_to_truncate = ['limitation', 'vitesse', 'jour_ferie', 'meteo', 'jours_feries_vacances']

for table in tables_to_truncate:
    try:
        session.execute(f"TRUNCATE {table};")
        print(f"Table '{table}' tronquée avec succès.")
    except Exception as e:
        print(f"Erreur en tronquant la table '{table}': {e}")

# Fermeture de la connexion
session.shutdown()
cluster.shutdown()
