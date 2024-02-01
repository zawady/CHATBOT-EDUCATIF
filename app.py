import os
import pandas as pd
from flask import Flask, render_template, request

# Charger votre DataFrame depuis le fichier CSV ou tout autre moyen que vous utilisez
df = pd.read_csv('test.csv')

def getResponse(msg):
    # Convertir l'entrée de l'utilisateur en minuscules pour la correspondance insensible à la casse
    user_input_lower = msg.lower()

    # Rechercher une correspondance dans le modèle (utilisez la colonne 'Contenu' comme questions)
    matching_row = df[df['Contenu'].str.lower() == user_input_lower]

    if not matching_row.empty:
        # Récupérer la réponse correspondante (utilisez la colonne 'Réponse')
        reply = matching_row.iloc[0]['Réponse']
        return reply
    else:
        return "Je ne comprends pas cette question."


app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    print(f"User Text: {userText}")
    
    try:
        response = getResponse(userText)
        print(f"Chatbot Response: {response}")
        return response
    except Exception as e:
        print(f"Error: {e}")
        return "Error processing the request"

if __name__ == "__main__":
    app.run()
