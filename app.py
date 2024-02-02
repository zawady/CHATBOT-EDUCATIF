import openai
import yaml
import mysql.connector
from flask import Flask, request, render_template

app = Flask(__name__)

#clé OpenAI
openai.api_key = "To4JGGzfA3pHywZgnRvlT3BlbkFJItt7ppuXZBHWeSjuKimw"


#connexion à la base
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="chatbot"
)


# Chargement des intentions depuis notre fichier intent
with open('intent.yaml', 'r') as intent_file:
    intent_data = yaml.safe_load(intent_file)


# On enregistre les conversation dans la base
def save_conversation(question, reponse, utilisateur_id):
    cursor = db_connection.cursor()
    sql_query = "INSERT INTO conversations (question, reponse, utilisateur_id) VALUES (%s, %s, %s)"
    cursor.execute(sql_query, (question, reponse, utilisateur_id))
    db_connection.commit()
    cursor.close()

# On utilise gpt3 pour obtenir une réponse 
def get_gpt3_response(question):
    detected_intent = detect_intent(question)

    examples = ""
    if detected_intent in intent_data:
        examples = intent_data[detected_intent]['examples']

#baser sur les examples de nos intents
    prompt = f"Examples: {examples}\nUser Input: {question}\n"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50
    )

    reponse = response.choices[0].text.strip()

   
    save_conversation(question, reponse, utilisateur_id=1)  

    return reponse

# On détecte l'intention 
def detect_intent(question):
    for intent, data in intent_data.items():
        examples = data.get('examples', [])
        for example in examples:
            if example in question:
                return intent

    # Si aucune correspondance n'est trouvée, on retourne une intention par défaut
    return "Default"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    question = request.form.get('user_input')
    response = get_gpt3_response(question)
    save_conversation(question, response, utilisateur_id=1)
    return response

if __name__ == '__main__':
    app.run(debug=True)
