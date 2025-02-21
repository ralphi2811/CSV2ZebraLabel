FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers requirements
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source (exclus l'émulateur)
COPY app app/
COPY run.py .

# Création du dossier instance pour la base de données
RUN mkdir -p instance && chmod 777 instance

# Variables d'environnement
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Exposition du port
EXPOSE 5000

# Commande de démarrage avec Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
