import os

# Configuration des variables d'environnement avec valeurs par défaut
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "127.0.0.1")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", 9042))  # Conversion explicite en entier
KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "cassandra")  # Assurez-vous que le keyspace est correct
