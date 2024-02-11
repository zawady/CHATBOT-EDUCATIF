from base64 import decode
from flask import Flask, request, render_template, jsonify,redirect, url_for
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from flask_cors import CORS
import pandas as pd
import re
import yaml

app = Flask(__name__)
CORS(app)


# Initialisation du tokenizer et du modèle GPT-2
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

tokenizer.pad_token = tokenizer.eos_token

# Lecture du fichier CSV et nettoyage des données
data = pd.read_csv('scrapping_données.csv')  # Assurez-vous que le chemin est correct
data_clean = data.copy()    
data_clean = data_clean.fillna('')  # Remplace les NaN par des chaînes vides pour éviter les erreurs

# Chargement des intentions
with open('intent.yaml', 'r') as file:
    intents = yaml.safe_load(file)

#@app.route('/')
#def login():
    # Affiche le formulaire de connexion
    ##return render_template('index.html')

#@app.route('/login', methods=['POST'])
#def handle_login():
        #return redirect(url_for('chatbot.py'))


@app.route('/')
def home():
    return render_template('chatbot.html')  # Assurez-vous que ce fichier se trouve dans le dossier "templates"

@app.route('/chat', methods=['POST'])
def chat():
    # Vérification que le corps de la requête contient 'user_message'
    user_message = request.json.get('user_message')
    if not user_message:
        return jsonify({'response': 'Le message utilisateur est manquant.'}), 400
    try:
        intent = detect_intent(user_message)
        response = generate_response_based_on_intent(intent, data_clean, user_message) if intent else "Désolé, je ne comprends pas votre question."
        return jsonify({'response': response})
    except Exception as e:
        # Gestion des exceptions lors du traitement de la requête
        return jsonify({'response': f'Erreur lors du traitement de la requête: {str(e)}'}), 500

# Fonction pour détecter l'intention
def detect_intent(user_question):
    for intent in intents:
        if re.search(intent['regex'], user_question, re.IGNORECASE):
            return intent
    return None

# Fonction pour générer une réponse basée sur l'intention et les données
def generate_response_based_on_intent(intent, data, user_question):
    relevant_data = ""
    prompt = f""

    # Construction du prompt en fonction de l'intention détectée
    if "Vidéo|tutoriel|leçons" in intent['regex']:
        relevant_data = ' '.join(data['Source'].dropna().tolist())
    elif "Titre du cours|sujet|thème" in intent['regex']:
        relevant_data = ' '.join(set(data['Titre du cours'].dropna().tolist()))
    elif "Durée|temps|long" in intent['regex']:
        relevant_data = data['Durée du cours'].iloc[0]  # Assumons que c'est un texte direct
    elif "Professeur|enseignant|formateur|profs" in intent['regex']:
        relevant_data = ' '.join(set(data['Nom du professeur'].dropna().tolist()))
    elif "Description des enseignants|description" in intent['regex']:
        relevant_data = ' '.join(data['Description du professeur'].dropna().tolist())
    elif "Contenu du cours|objectif|Compètences visées" in intent['regex']:
        relevant_data = ' '.join(data['Contenu'].dropna().tolist())
    elif "Titre section|cours enseignés" in intent['regex']:
       # Extraction du titre de la section de la question
        title_of_interest = extract_section_title(user_question)
        # Recherche du contenu basé sur le titre extrait
        return search_content_by_title(title_of_interest)
    elif "Résumé" in intent['regex']:
        relevant_data = ' '.join(data[['Titre de la section', 'Contenu']].apply(lambda x: ': '.join(x), axis=1).dropna().tolist())

    # Traitement spécifique pour l'intention "Vidéo|tutoriel|leçons"
    if "Vidéo|tutoriel|leçons" in intent['regex']:
       urls = re.findall(r'https?://[^\s]+', relevant_data)
       # Transformer chaque URL en un lien HTML
       links = [f'<a href="{url}">{url}</a>' for url in urls]    
       # Retourner les liens
       return links

    if not relevant_data:
        relevant_data = "Informations non disponibles."
    print(relevant_data)
    prompt += relevant_data
    return prompt

def extract_section_title(question):
    # Définition des motifs de recherche pour extraire le titre de la section
    patterns = [
        r"objectifs de (.+)",
        r"contenu de (.+)",
        r"en savoir plus sur (.+)",
        r"informations sur (.+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, question, re.IGNORECASE)
        if match:
            # Retourner le premier groupe capturé qui devrait représenter le titre de la section
            return match.group(1).strip()
    
    # Si aucun motif n'est trouvé, retourner une chaîne vide ou un indicateur spécifique
    return ""  # Vous pouvez choisir de retourner None ou une indication 

def search_content_by_title(title):
    relevant_data = data_clean[data_clean['Titre de la section'].str.contains(title, case=False, na=False)]
    if relevant_data.empty:
        return "Aucune information trouvée pour cette section."
    else:
        return '\n\n'.join(f"Section: {row['Titre de la section']}\nContenu: {row['Contenu']}" for index, row in relevant_data.iterrows())
   
if __name__ == '__main__':
    app.run(debug=True)
