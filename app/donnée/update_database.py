from cassandra.cluster import Cluster
import os

# Configuration de la connexion à Cassandra
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "127.0.0.1")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", 9042))
KEYSPACE = "cassandra"  # Remplacez par le nom de votre keyspace

# Connexion à Cassandra
cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
session = cluster.connect()

# Sélectionner le keyspace
session.set_keyspace(KEYSPACE)

# Modifier ou créer la table `limitation` avec les nouvelles colonnes
session.execute("""
    CREATE TABLE IF NOT EXISTS limitation (
        capteur_id uuid PRIMARY KEY,
        latitude float,
        longitude float,
        limitation float
    )
""")

print("La table `limitation` a été créée ou mise à jour avec succès.")
