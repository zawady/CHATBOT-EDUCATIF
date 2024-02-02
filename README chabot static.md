# Chatbot Web avec Flask, GPT-3, et MySQL

## Description du projet
Ce projet consiste en un chatbot web développé avec Flask, intégrant l'API GPT-3 d'OpenAI pour générer des réponses et utilisant une base de données MySQL pour stocker les conversations. 
L'interface utilisateur est créée en HTML et utilise jQuery pour des fonctionnalités interactives.

## Interface Utilisateur HTML (chatbot_static.html)
Le fichier HTML définit l'interface utilisateur du chatbot. Il comprend une section pour afficher les messages, une zone de saisie pour l'utilisateur, et un bouton d'envoi.

  - Header: Contient le titre "Learn IQ" avec une icône.
  - Messages: La section principale où les messages sont affichés dynamiquement.
  - Formulaire de Saisie: Comprend une zone de texte pour l'utilisateur et un bouton d'envoi.
  - Script JavaScript: Gère l'interaction avec l'utilisateur, l'affichage des messages, et l'envoi des messages au serveur.

## Serveur Flask (app.py)
Le script Python utilise Flask pour créer un serveur web. Il communique avec l'API GPT-3 pour les réponses et stocke les conversations dans une base de données MySQL.

Configuration OpenAI: Remplacez la clé d'API OpenAI dans le code.

Configuration MySQL: Spécifiez les détails de connexion à votre base de données MySQL.

Chargement des Intentions: Les intentions sont chargées à partir d'un fichier YAML (intent.yaml).

#### Routes Flask:

"/" : Affiche la page principale (chatbot_static.html).

"/chat" (POST): Reçoit les messages de l'utilisateur, génère des réponses via GPT-3, les stocke dans la base de données, et renvoie la réponse au navigateur.

#### Fonctions principales:

"get_gpt3_response(question)" : Utilise GPT-3 pour générer des réponses en fonction des exemples d'intentions.

"detect_intent(question)" : Détecte l'intention de l'utilisateur en comparant les exemples d'intentions.

"save_conversation(question, response)" : Enregistre la conversation dans la base de données.

## Exécution du Projet
1. Installez les dépendances avec pip install Flask openai mysql-connector-python pandas.

2. Configurez les clés d'API OpenAI dans app.py et les détails de connexion MySQL.

3. Exécutez le script app.py pour démarrer le serveur Flask.

4. Accédez à l'application dans votre navigateur à l'adresse http://127.0.0.1:5000/.

5. Commencez à interagir avec le chatbot en entrant des messages dans la zone de saisie.
