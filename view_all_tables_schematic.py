from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from tabulate import tabulate  # Assurez-vous d'installer cette bibliothèque avec `pip install tabulate`

# Paramètres de connexion
CASSANDRA_HOST = '127.0.0.1'  # Remplacez par l'adresse IP de votre serveur Cassandra
CASSANDRA_PORT = 9042         # Port par défaut
KEYSPACE = 'cassandra'      # Remplacez par le nom de votre keyspace

# Connexion à Cassandra
def connect_to_cassandra():
    try:
        cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
        session = cluster.connect(KEYSPACE)
        print(f"Connected to keyspace '{KEYSPACE}' on Cassandra at {CASSANDRA_HOST}:{CASSANDRA_PORT}")
        return cluster, session
    except Exception as e:
        print(f"Erreur lors de la connexion à Cassandra : {e}")
        exit()

# Récupérer et afficher les données de toutes les tables
def display_all_tables_schematic(session):
    try:
        # Récupère les noms de toutes les tables du keyspace
        query = "SELECT table_name FROM system_schema.tables WHERE keyspace_name=%s"
        rows = session.execute(query, [KEYSPACE])
        
        for row in rows:
            table_name = row.table_name
            print(f"\n=== Contenu de la table '{table_name}' ===")
            
            # Récupère les données de la table
            try:
                result = session.execute(f"SELECT * FROM {table_name} LIMIT 10")  # Limite les résultats à 10 lignes
                headers = result.column_names  # Colonnes de la table
                data = [list(row) for row in result]  # Contenu de la table

                # Affichage schématique avec tabulate
                print(tabulate(data, headers=headers, tablefmt="grid"))
            except Exception as e:
                print(f"Erreur lors de la lecture de la table '{table_name}': {e}")
    except Exception as e:
        print(f"Erreur lors de la récupération des tables : {e}")

# Fermer la connexion à Cassandra
def close_connection(cluster):
    cluster.shutdown()
    print("Connexion à Cassandra fermée.")

if __name__ == "__main__":
    cluster, session = connect_to_cassandra()
    display_all_tables_schematic(session)
    close_connection(cluster)
