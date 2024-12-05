#!/bin/bash

echo "=============================="
echo "   DÉMARRAGE DU SCRIPT"
echo "=============================="

# Étape 1 : Arrêter les services Docker Compose
echo ">>> Arrêt des services Docker Compose..."
docker-compose down

# Étape 2 : Démarrer les services Docker Compose
echo ">>> Démarrage des services Docker Compose..."
docker-compose up -d

# Étape 3 : Attente de la disponibilité de Cassandra
echo ">>> Attente de la disponibilité de Cassandra..."
while ! docker exec project-cassandra-1 cqlsh -e "DESCRIBE KEYSPACES" &> /dev/null; do
    echo "Cassandra n'est pas encore prêt. Nouvelle tentative dans 5 secondes..."
    sleep 5
done
echo ">>> Cassandra est prêt."

# Étape 4 : Vérification et création du keyspace
echo ">>> Vérification et création du keyspace 'cassandra' si nécessaire..."
docker exec -i project-cassandra-1 cqlsh <<EOF
CREATE KEYSPACE IF NOT EXISTS cassandra WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 };
DESCRIBE KEYSPACES;
EOF

# Étape 5 : Exécuter truncate_tables.py
echo ">>> Exécution du script truncate_tables.py..."
if python truncate_tables.py; then
    echo ">>> Script truncate_tables.py exécuté avec succès."
else
    echo ">>> Erreur lors de l'exécution du script truncate_tables.py."
    exit 1
fi

# Étape 6 : Nettoyer et vérifier les données
echo ">>> Nettoyage et vérification des données avec net_et_veri_donnee.py..."
if python net_et_veri_donnee.py; then
    echo ">>> Données nettoyées et vérifiées avec succès."
else
    echo ">>> Erreur lors de l'exécution de net_et_veri_donnee.py."
    exit 1
fi

# Étape 7 : Exécuter create_tables.py
echo ">>> Création des tables avec create_tables.py..."
if python create_tables.py; then
    echo ">>> Tables créées avec succès."
else
    echo ">>> Erreur lors de l'exécution de create_tables.py."
    exit 1
fi

# Étape 8 : Vérifier la structure des tables
echo ">>> Vérification de la structure des tables avec view_all_tables_schematic.py..."
if python view_all_tables_schematic.py; then
    echo ">>> Structure des tables vérifiée avec succès."
else
    echo ">>> Erreur lors de l'exécution de view_all_tables_schematic.py."
    exit 1
fi

# Étape 9 : Remplir les tables avec run_insertions.py
echo ">>> Insertion des données dans les tables avec run_insertions.py..."
if python run_all_insertions.py; then
    echo ">>> Données insérées avec succès."
else
    echo ">>> Erreur lors de l'exécution de run_insertions.py."
    exit 1
fi

# Étape 10 : Vérifier la structure des tables après insertion
echo ">>> Vérification de la structure des tables après insertion avec view_all_tables_schematic.py..."
if python view_all_tables_schematic.py; then
    echo ">>> Structure des tables après insertion vérifiée avec succès."
else
    echo ">>> Erreur lors de l'exécution de view_all_tables_schematic.py après insertion."
    exit 1
fi

# Étape 11 : Lancer les tests
echo ">>> Lancement des tests avec pytest (sans warnings)..."
if pytest --disable-warnings; then
    echo ">>> Tous les tests ont réussi."
else
    echo ">>> Échec de certains tests. Veuillez vérifier les logs de pytest."
    exit 1
fi

# Étape 12 : Démarrage de l'API FastAPI
echo ">>> Démarrage de l'API FastAPI..."
if uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload & then
    echo ">>> API FastAPI démarrée avec succès."
else
    echo ">>> Erreur lors du démarrage de l'API FastAPI."
    exit 1
fi

echo "=============================="
echo "   FIN DU SCRIPT"
echo "=============================="
