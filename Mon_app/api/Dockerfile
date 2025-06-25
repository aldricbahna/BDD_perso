# Utilise une image Python légère
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers requis dans le conteneur
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exposer le port 5000 (Flask par défaut)
EXPOSE 5000

# Commande de lancement
CMD ["python", "app.py"]
