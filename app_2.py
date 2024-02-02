import openai
import yaml
import mysql.connector
from flask import Flask, request, render_template

app = Flask(__name__)
# Configuration de l'API OpenAI (utilisez votre propre clé d'API)
openai.api_key = "To4JGGzfA3pHywZgnRvlT3BlbkFJItt7ppuXZBHWeSjuKimw"

# Configuration de la connexion à la base de données SQL (remplacez 'chatbot' par votre chaîne de connexion)
# Configuration de la connexion à la base de données MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="chatbot"
)


# Chargement des intentions depuis le fichier YAML
with open('intent.yaml', 'r') as intent_file:
    intent_data = yaml.safe_load(intent_file)

# Fonction pour enregistrer une conversation dans la base de données
def save_conversation(question, reponse, utilisateur_id):
    cursor = db_connection.cursor()
    sql_query = "INSERT INTO conversations (question, reponse, utilisateur_id) VALUES (%s, %s, %s)"
    cursor.execute(sql_query, (question, reponse, utilisateur_id))
    db_connection.commit()
    cursor.close()

# Fonction pour obtenir une réponse en utilisant GPT-3
def get_gpt3_response(question):
    detected_intent = detect_intent(question)

    # Obtenez les exemples de l'intention détectée
    examples = ""
    if detected_intent in intent_data:
        examples = intent_data[detected_intent]['examples']

    # Utilisez GPT-3 pour générer une réponse basée sur les exemples de l'intention
    prompt = f"Examples: {examples}\nUser Input: {question}\n"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50
    )

    reponse = response.choices[0].text.strip()

    # Enregistrez la conversation dans la base de données
    save_conversation(question, reponse, utilisateur_id=1)  # Vous devrez spécifier un utilisateur_id approprié

    return reponse

# Fonction pour détecter l'intention en fonction de l'entrée utilisateur
def detect_intent(question):
    # Comparez l'entrée utilisateur avec les exemples d'intentions
    for intent, data in intent_data.items():
        examples = data.get('examples', [])
        for example in examples:
            if example in question:
                return intent

    # Si aucune correspondance n'est trouvée, retournez une intention par défaut
    return "Default"

# Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

# Route pour traiter les demandes de l'utilisateur
@app.route('/chat', methods=['POST'])
def chat():
    question = request.form.get('user_input')
    response = get_gpt3_response(question)
    save_conversation(question, response, utilisateur_id=1)
    return response

if __name__ == '__main__':
    app.run(debug=True)
