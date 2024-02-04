from transformers import TapexTokenizer, BartForConditionalGeneration
import pandas as pd
import re
import yaml

# Initialisation du tokenizer et du modèle TAPEx
tokenizer = TapexTokenizer.from_pretrained("microsoft/tapex-large-finetuned-wtq")
model = BartForConditionalGeneration.from_pretrained("microsoft/tapex-large-finetuned-wtq")

# Lecture du fichier CSV et nettoyage des données
data = pd.read_csv('scrapping_traité.csv')  # Vérifiez le chemin
data_clean = data[['Titre de la section', 'Contenu', 'Nom du professeur', 'Titre du cours', 'Titre de la vidéo', 'Durée du cours','Description du professeur', 'Source']].copy()
data_clean['Contenu'] = data_clean['Contenu'].str.strip()
data_clean['Titre de la section'] = data_clean['Titre de la section'].str.strip()

# Structuration des données pour TAPEx
columns = ['Titre de la section', 'Contenu', 'Nom du professeur', 'Titre du cours']
table_example = data_clean[columns]

# Chargement des intentions
with open('intent.yaml', 'r') as file:
    intents = yaml.safe_load(file)

# Demande d'input utilisateur pour la question
user_question = input("Veuillez poser votre question : ")

# Détection de l'intention
detected_intent = None
for intent in intents:
    if re.search(intent['regex'], user_question, re.IGNORECASE):
        detected_intent = intent['regex']
        break

# Fonction pour générer une réponse basée sur l'intention et les données
def generate_response(intent, table):
    # Formulation de la requête basée sur l'intention détectée
    query = "Informations non disponibles."  # Fallback par défaut
    if intent == 'Durée':
        query = "Quelle est la durée de ce cours ?"
    elif intent == 'Prérequis':
        query = "Quels sont les prérequis pour ce cours ?"
    elif intent == 'Professeurs':
        query = "Qui sont les instructeurs ou professeurs de cette formation?"
    
    # Encoder la requête et le tableau pour le modèle TAPEx
    encoding = tokenizer(table=table, query=query, return_tensors="pt", truncation=True, padding="max_length", max_new_tokens=512)
    
    # Générer la réponse avec le modèle
    outputs = model.generate(**encoding)
    
    # Décoder les sorties pour obtenir la réponse textuelle
    response = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    
    return response[0]

# Exemple d'utilisation
if detected_intent:
    print(f"Intention détectée : {detected_intent}")
    response = generate_response(detected_intent, table_example)
    print(response)
else:
    print("Aucune intention correspondante trouvée.")
