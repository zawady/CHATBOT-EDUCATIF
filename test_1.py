#TTEEEESSSSSTTTTTT
from transformers import BartForConditionalGeneration, BartTokenizer, TapexTokenizer
import pandas as pd
import re
import yaml

# Initialisation du tokenizer et du modèle TAPEx
tokenizer_tapex = TapexTokenizer.from_pretrained("microsoft/tapex-large-finetuned-wtq")
model_tapex = BartForConditionalGeneration.from_pretrained("microsoft/tapex-large-finetuned-wtq")

# Initialisation du tokenizer et du modèle pour la génération de résumés avec BART
tokenizer_summary = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model_summary = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')


# Lecture du fichier CSV et nettoyage des données
data = pd.read_csv('scrapping.csv')  # Vérifiez le chemin
data_clean = data[['Titre de la section', 'Contenu', 'Nom du professeur', 'Titre du cours', 'Titre de la vidéo', 'Durée du cours','Description du professeur', 'Source']].copy()
data_clean['Contenu'] = data_clean['Contenu'].str.strip()
data_clean['Titre de la section'] = data_clean['Titre de la section'].str.strip()

# Structuration des données pour TAPEx
columns = ['Titre de la section', 'Contenu', 'Nom du professeur', 'Titre du cours', 'Titre de la vidéo', 'Durée du cours','Description du professeur', 'Source']
table_example = data_clean[columns]

# Chargement des intentions
with open('intent.yaml', 'r') as file:
    intents = yaml.safe_load(file)

# Fonction pour générer une réponse basée sur l'intention et les données
def generate_response(intent, table):
 if intent == 'Résumé':
        # Extraire le titre pour la génération de résumé
        title_keyword = user_question.replace('résumé de ', '').strip()
        matched_rows = table[(table['Titre de la section'].str.contains(title_keyword, case=False)) | (table['Titre du cours'].str.contains(title_keyword, case=False))]
        if not matched_rows.empty:
            content_to_summarize = matched_rows.iloc[0]['Contenu']
            inputs = tokenizer_summary(content_to_summarize, return_tensors="pt", max_length=1024, truncation=True)
            summary_ids = model_summary.generate(inputs['input_ids'], max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
            summary = tokenizer_summary.decode(summary_ids[0], skip_special_tokens=True)
            return summary
        else:
            return "Aucun contenu trouvé correspondant à votre demande de résumé."
 else:
    # Pour d'autres intentions, utilisez la logique de génération de réponse basée sur TAPEx
    query = user_question  # Utilisez la question de l'utilisateur comme requête directement
    encoding = tokenizer_tapex(table=table, query=query, return_tensors="pt", truncation=True, padding="max_length", max_new_tokens=512)
    outputs = model_tapex.generate(**encoding)
    response = tokenizer_tapex.batch_decode(outputs, skip_special_tokens=True)
    return response[0]
   

# Boucle principale pour demander une input utilisateur
while True:
    user_question = input("Veuillez poser votre question : ")
    if user_question.lower() == "exit":
        print("Fin de la discussion.")
        break  # Sortie de la boucle si l'utilisateur tape "exit"
    
    detected_intent = None
    for intent in intents:
        if re.search(intent['regex'], user_question, re.IGNORECASE):
            detected_intent = intent['regex']
            break

    if detected_intent:
        print(f"Intention détectée : {detected_intent}")
        response = generate_response(detected_intent, table_example)
        print(response)
    else:
        print("Aucune intention correspondante trouvée. Tapez 'exit' pour quitter.")
