# Utilise Python comme image de base
FROM python:3.8-slim

# Configure le répertoire de travail
WORKDIR /app

# Copie uniquement les fichiers nécessaires pour l'installation des dépendances
COPY requirements.txt /app/

# Installer les dépendances en une seule commande
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste des fichiers de l'application dans le conteneur
COPY . /app
COPY wait-for-it.sh /wait-for-it.sh

# Rendre le script d'attente exécutable
RUN chmod +x /wait-for-it.sh

# Commande de démarrage
CMD ["/wait-for-it.sh", "cassandra:9042", "--timeout=1", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
