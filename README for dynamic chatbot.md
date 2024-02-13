# CHATBOT-PROJECT
=======
# Chatbot avec Flask, GPT-3, MySQL, et HTML
Ce projet implémente un chatbot éducatif d'une formation en HTML/CSS ( disponible sur OpenClassroom ), en utilisant Flask comme framework backend, intégré avec le modèle de langage GPT-2 pour le traitement du langage naturel et MySQL pour la gestion des données utilisateur. Le chatbot est conçu pour répondre à diverses requêtes basées sur des intentions prédéfinies, facilitant ainsi une interaction naturelle et informative.

## Description

Le chatbot utilise un modèle GPT-2 pré-entraîné pour générer des réponses aux questions des utilisateurs. Les intentions des utilisateurs sont détectées à l'aide d'expressions régulières, permettant une personnalisation et une extension faciles. Le système gère l'authentification des utilisateurs et stocke l'historique des conversations dans une base de données MySQL. Ce projet est idéal pour ceux qui cherchent à développer des applications de chatbot personnalisées avec des capacités de traitement du langage naturel plus ou moins avancées.

## Prérequis

Avant de commencer, assurez-vous que vous avez installé les éléments suivants sur votre système :
- Python 3.8 ou supérieur
- MySQL Server
- Les bibliothèques Python nécessaires listées dans le fichier "requirements.txt"

## Installation

Clonez le dépôt GitHub :
git clone [Nom de ce depot distant]

## Configurez votre environnement Python (FACULTATIF) : 

Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet. Mais c'est facultatif.
-python -m venv myenv ( pour creer l'environnement virtuel)
-source venv/bin/activate ( pour l'activer )
- deactivate ( pour le désactiver )

## Installez les dépendances :

- pip install -r requirements.txt

## Configurez votre base de données MySQL :

- Créez une base de données pour le projet.
- Exécutez les scripts SQL fournis pour créer les tables nécessaires.

## Configurez les variables d'environnement :

-Renommez le fichier .env.example en .env et mettez à jour les valeurs pour correspondre à votre configuration de base de données et à d'autres paramètres secrets.

## Lancez l'application :

-python app.py

## Utilisation
Après avoir lancé l'application, naviguez vers http://localhost:5000 pour accéder à l'interface du chatbot. Vous pouvez vous inscrire comme nouvel utilisateur ou vous connecter avec un compte existant pour commencer à interagir avec le chatbot.
