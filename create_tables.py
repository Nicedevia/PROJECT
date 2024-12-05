from cassandra.cluster import Cluster
from cassandra.cluster import NoHostAvailable
import os
import sys

# Configuration des variables d'environnement
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "127.0.0.1")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", 9042))
KEYSPACE = "cassandra"  # Nom du keyspace (modifiez si nécessaire)

# Connexion à Cassandra
try:
    cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
    session = cluster.connect()
    print(f"Connexion réussie à Cassandra sur {CASSANDRA_HOST}:{CASSANDRA_PORT}")
except NoHostAvailable as e:
    print(f"Impossible de se connecter à Cassandra : {e}")
    sys.exit(1)

# Assurer la connexion au keyspace ou le créer s'il n'existe pas
try:
    session.execute(f"CREATE KEYSPACE IF NOT EXISTS {KEYSPACE} "
                    "WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};")
    session.set_keyspace(KEYSPACE)
    print(f"Keyspace '{KEYSPACE}' prêt à l'emploi.")
except Exception as e:
    print(f"Erreur lors de la création du keyspace : {e}")
    sys.exit(1)

# Requêtes de création des tables
tables_creation_queries = [
    """
    CREATE TABLE IF NOT EXISTS vitesse (
        date timestamp,
        capteur_id uuid,
        vitesse float,
        PRIMARY KEY (capteur_id, date)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS jour_ferie (
        date timestamp,
        description text,
        zone_1 boolean,
        zone_2 boolean,
        zone_3 boolean,
        PRIMARY KEY (date)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS limitation (
        capteur_id uuid,
        latitude float,
        longitude float,
        limitation float,
        PRIMARY KEY (capteur_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS meteo (
        date timestamp,
        capteur_id uuid,
        visibilite float,
        precipitation float,
        PRIMARY KEY (capteur_id, date)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS jours_feries_vacances (
        evenement_id uuid PRIMARY KEY,
        type_evenement text,
        description text,
        date_debut timestamp,
        date_fin timestamp,
        zones text,
        annee_scolaire text
    )
    """
]

# Exécution des commandes de création des tables
for query in tables_creation_queries:
    try:
        session.execute(query)
        table_name = query.split()[5]  # Extract table name from the query
        print(f"Table '{table_name}' créée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création de la table : {e}")

# Vérification des tables créées
try:
    rows = session.execute("SELECT table_name FROM system_schema.tables WHERE keyspace_name=%s", (KEYSPACE,))
    print("\n=== Tables disponibles dans le keyspace ===")
    for row in rows:
        print(f"- {row.table_name}")
except Exception as e:
    print(f"Erreur lors de la vérification des tables : {e}")

# Fermeture de la connexion
cluster.shutdown()
print("\nConnexion à Cassandra fermée.")
