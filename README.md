
# Chatbot Conversational basé sur OpenAI et Streamlit

Ce projet est un chatbot conversationnel qui utilise l'API OpenAI pour répondre aux questions à partir d'un fichier CSV téléchargé. Il est développé avec Streamlit, une bibliothèque Python pour créer des applications web interactives avec un minimum d'effort.

## Fonctionnalités

- Prend en charge le chargement de données à partir d'un fichier CSV.
- Utilise les embeddings OpenAI pour traiter les questions.
- Implémente un modèle de chaîne de conversation pour des réponses interactives.
- Affiche l'historique des conversations dans une interface utilisateur intuitive.

## Configuration

1. **Clé API OpenAI :** Vous devrez obtenir une clé API valide depuis le [site web d'OpenAI](https://openai.com/) et l'insérer dans le champ prévu à cet effet dans l'interface.
2. **Fichier CSV :** Téléchargez un fichier CSV contenant les données sur lesquelles vous souhaitez baser les réponses du chatbot.

## Installation

1. Assurez-vous d'avoir Python installé sur votre système.
2. Clonez ce dépôt sur votre machine locale.
3. Installez les dépendances requises en exécutant `pip install -r requirements.txt`.

## Utilisation

1. Exécutez l'application en exécutant `streamlit run app.py` dans votre terminal.
2. Dans l'interface, ajoutez votre clé API OpenAI et téléchargez un fichier CSV contenant vos données.
3. Posez vos questions dans le champ de saisie et appuyez sur le bouton "Envoyer" pour obtenir des réponses du chatbot.
4. L'historique de la conversation sera affiché dans la partie inférieure de l'interface.

## Remarques

- Assurez-vous que les données du fichier CSV sont correctement formatées pour être traitées par le chatbot.
- L'utilisation de l'API OpenAI peut être soumise à des limites et des politiques d'utilisation, veuillez consulter la documentation officielle pour plus d'informations.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une pull request ou à signaler des problèmes.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
