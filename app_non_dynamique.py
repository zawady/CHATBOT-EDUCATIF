from flask import Flask, request, jsonify, render_template
import openai
import mysql.connector
import yaml

app = Flask(__name__, static_url_path='/static')

openai.api_key = "To4JGGzfA3pHywZgnRvlT3BlbkFJItt7ppuXZBHWeSjuKimw"

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="chatbot"
)

with open('intent.yaml', 'r') as file:
    intent_data = yaml.safe_load(file)

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']
    response = get_gpt3_response(user_message)
    return jsonify({'response': response})

def get_gpt3_response(question):
    # Vérifiez d'abord dans la base de données pour une réponse prédéfinie
    cursor = db_connection.cursor()
    query = "SELECT answer FROM faq WHERE question LIKE %s"
    cursor.execute(query, (question,))
    db_response = cursor.fetchone()
    cursor.close()

    if db_response:
        return db_response[0]  # Retourne la réponse prédéfinie

    # Si pas de réponse prédéfinie, utilisez GPT-3
    detected_intent = detect_intent(question)
    examples = intent_data.get(detected_intent, {}).get('examples', '')
    prompt = f"Examples: {examples}\nUser Input: {question}\n"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50
    )
    text_response = response.choices[0].text.strip()
    save_conversation(question, text_response)
    return text_response


def detect_intent(question):
    for intent, data in intent_data.items():
        if question.lower() in [example.lower() for example in data.get('examples', [])]:
            return intent
    return "default"

def save_conversation(question, response):
    cursor = db_connection.cursor()
    sql_query = "INSERT INTO conversations (question, response) VALUES (%s, %s)"
    cursor.execute(sql_query, (question, response))
    db_connection.commit()
    cursor.close()

if __name__ == '__main__':
    app.run(debug=True)
