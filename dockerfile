FROM python:3.10.5

# Installer Git
RUN apt-get update && apt-get install -y git

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Cloner le dépôt Git dans le conteneur
RUN git clone https://github.com/DevIA05/fertilite.git .

# Installer les dépendances
RUN pip install -r /app/requirements.txt

# # Monter le volume pour le répertoire de travail
VOLUME /app

# # Exposer le port 8501 (port par défaut de Streamlit)
EXPOSE 8501

# # Définir la commande pour exécuter l'application Streamlit
CMD streamlit run /app/app/main.py
