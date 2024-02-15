from flask import Flask, request, render_template, jsonify, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from flask_cors import CORS
import pandas as pd
import re
import yaml
import os
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get('SECRET_KEY')


db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'root',
    'database': 'chatbot'
}

# Initialisation du tokenizer et du modèle GPT-2
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

tokenizer.pad_token = tokenizer.eos_token

data = pd.read_csv('scrapping_données.csv')
data_clean = data.copy()
data_clean = data_clean.fillna('')

# Chargement des intentions
with open('intent.yaml', 'r') as file:
    intents = yaml.safe_load(file)


# autentification
@app.route('/', methods=['GET', 'POST'])
def auth():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        username = request.form['nom']
        password = request.form['password']

        if "login" in request.form:
            cursor.execute(
                "SELECT * FROM utilisateurs WHERE nom = %s", (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                session['nom'] = username
                session['utilisateur_id'] = user['id']
                return redirect(url_for('home'))
            else:
                flash("Nom d'utilisateur ou mot de passe incorrect", 'danger')

        elif "register" in request.form:
            email = request.form.get('email')
            hashed_password = generate_password_hash(password)
            cursor.execute(
                "SELECT * FROM utilisateurs WHERE nom = %s", (username,))
            if cursor.fetchone():
                flash("Le nom d'utilisateur existe déjà.", 'danger')
            else:
                cursor.execute(
                    "INSERT INTO utilisateurs (nom,email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
                conn.commit()
                flash('Inscription réussie. Veuillez vous connecter.', 'success')
                return redirect(url_for('home'))

    cursor.close()
    conn.close()
    return render_template('index.html')

# template du chatbot


@app.route('/chatbot')
def home():
    user_name = session.get('nom')
    return render_template('chatbot.html', user_name=user_name)


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('user_message')
    if not user_message:
        return jsonify({'response': 'Le message utilisateur est manquant.'}), 400
    try:
        intent = detect_intent(user_message)
        response = generate_response_based_on_intent(
            intent, data_clean, user_message) if intent else "Désolé, je ne comprends pas votre question."
        save_message_to_db(user_message, response)
        return jsonify({'response': response})
    except Exception as e:
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
        relevant_data = data['Durée du cours'].iloc[0]
    elif "Professeur|enseignant|formateur|profs" in intent['regex']:
        relevant_data = ' '.join(
            set(data['Nom du professeur'].dropna().tolist()))
    elif "Description des enseignants|description" in intent['regex']:
        relevant_data = ' '.join(
            data['Description du professeur'].dropna().tolist())
    elif "Contenu du cours|objectif|Compètences visées" in intent['regex']:
        relevant_data = ' '.join(data['Contenu'].dropna().tolist())

    elif "recherche_section|cours_enseignés" in intent['regex']:
        title_of_interest = extract_section_title(user_question)
        return search_content_by_title(title_of_interest)

    elif "Résumé" in intent['regex']:
        relevant_data = ' '.join(data[['Titre de la section', 'Contenu']].apply(
            lambda x: ': '.join(x), axis=1).dropna().tolist())

    elif "resumer" in intent['regex']:
        i = 0
        relevant_data = ' '
        for user_question in data['Titre de la section']:
            if "En résumé" in user_question:
                relevant_data = relevant_data + ' ' + data['Contenu'][i]
            i = i+1

    elif "Bonjour|Hello|Salut|Hi" in intent['regex']:
        return generate_dynamic_greeting()

    # traitement specifique pour les vidéos
    if "Vidéo|tutoriel|leçons" in intent['regex']:
       urls = re.findall(r'https?://[^\s]+', relevant_data)
       links = [f'<a href="{url}">{url}</a>' for url in urls]
       return links

    if not relevant_data:
        relevant_data = "Informations non disponibles."
    print(relevant_data)
    prompt += relevant_data
    return prompt


def generate_dynamic_greeting():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Bonjour ! Comment puis-je vous aider aujourd'hui ?"
    elif 12 <= current_hour < 18:
        greeting = "Bon après-midi ! En quoi puis-je vous être utile ?"
    else:
        greeting = "Bonsoir ! Comment puis-je vous assister ?"
    return greeting


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
            return match.group(1).strip()
    return ""


def search_content_by_title(title):
    relevant_data = data_clean[data_clean['Titre de la section'].str.contains(
        title, case=False, na=False)]

    if relevant_data.empty:
        return "Aucune information trouvée pour cette section."
    else:
        return '\n\n'.join(f"Section: {row['Titre de la section']}\nContenu: {row['Contenu']}" for index, row in relevant_data.iterrows())


def save_message_to_db(user_message, bot_response):
    utilisateur_id = session.get('utilisateur_id')
    if not utilisateur_id:
        print("L'utilisateur n'est pas connecté.")
        return
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO historique (question, reponse, utilisateur_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_message, bot_response, utilisateur_id))
        conn.commit()
    except mysql.connector.Error as error:
        print(f"Echec lors de l'enregistrement de l'historique {error}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)
