# CHATBOT-PROJECT
=======
# Chatbot avec Flask, GPT-3, MySQL, et HTML

## Description du projet
Ce projet est un chatbot éducatif d'une formation en HTML/CSS, basé sur Flask, qui utilise l'API GPT-3 pour générer des réponses en fonction des intentions détectées. Les données de conversation sont stockées dans une base de données MySQL. L'interface utilisateur est créée en HTML avec des fonctionnalités de chat en temps réel.

## Configuration
API OpenAI
Assurez-vous de remplacer la clé d'API OpenAI par votre propre clé dans le fichier principal app.py ou dans config.py selon vos préferences en matière de sécurité: 

openai.api_key = "Votre_clé_API_OpenAI"


## Base de données MySQL
Modifiez les détails de connexion à la base de données dans le fichier principal app.py : 

db_connection = mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="your_db"
)

## Fichier YAML pour les intentions
Le fichier intent.yaml contient des exemples pour détecter les intentions. Ajoutez des exemples pour d'autres entités selon vos besoins.

## Structure de la base de données
Le script database_setup.py crée une base de données chatbot avec les tables profs, formation, cours, et videos.

## Insertion de données
Le script insert_data.py insère des données depuis un fichier CSV dans la table cours. Modifiez le chemin du fichier CSV selon vos besoins.

## Interface utilisateur HTML
Le fichier templates/index.html contient l'interface utilisateur du chatbot.

## Exécution du projet
Installez les dépendances avec pip install Flask pandas mysql-connector-python.
Exécutez python database_setup.py pour créer la base de données et les tables.
Exécutez python insert_data.py pour insérer des données depuis un fichier CSV.
Exécutez python app.py pour démarrer le serveur Flask.
Accédez à l'application dans votre navigateur à l'adresse http://127.0.0.1:5000/.

## Utilisation du chatbot
Entrez vos messages dans la zone de texte.
Appuyez sur "Envoyer".
Le chatbot générera des réponses basées sur les intentions détectées et les exemples fournis.
