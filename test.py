import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector
import ssl
from flask import Flask, render_template, request


# Désactiver la vérification SSL
ssl._create_default_https_context = ssl._create_unverified_context

# Charger le fichier CSV dans le DataFrame
merged_df_1 = pd.read_csv('scrapping.csv')

# Assurez-vous que nltk est téléchargé
nltk.download('punkt')
nltk.download('stopwords')

# Fonction de prétraitement du texte
def preprocess_text(text):
    words = nltk.word_tokenize(text)
    words = [word for word in words if word.isalnum()]
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in words if word.lower() not in stop_words]
    return ' '.join(words)

# Exemple : Utilisation des colonnes 'Titre du cours', 'Contenu', 'Nom du professeur', et 'Description du professeur'
text_columns = ['Titre du cours', 'Contenu', 'Nom du professeur', 'Description du professeur']

# Remplacez les valeurs nulles ou float par une chaîne vide
merged_df_1[text_columns] = merged_df_1[text_columns].fillna('').astype(str)

# Concaténation des colonnes textuelles en une seule colonne pour simplifier la vectorisation
merged_df_1['Texte_concatene'] = merged_df_1[text_columns].apply(lambda x: ' '.join(x), axis=1)

# Prétraitement des données
merged_df_1['Texte_concatene'] = merged_df_1['Texte_concatene'].apply(preprocess_text)

# Vectorisation TF-IDF
vectorizer = TfidfVectorizer()
vectorized_text = vectorizer.fit_transform(merged_df_1['Texte_concatene'])

# Create a Flask web application
app = Flask(__name__)

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='chat'
)

# Créer un objet curseur pour exécuter des requêtes SQL
cursor = conn.cursor()

# Créer la table s'il n'existe pas
cursor.execute('''CREATE TABLE IF NOT EXISTS conversation_logs
                  (id INT AUTO_INCREMENT PRIMARY KEY,
                   user_input TEXT,
                   chatbot_response TEXT,
                   timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

# Fonction pour obtenir la réponse du chatbot
def get_response(user_input):
    user_input = preprocess_text(user_input)
    user_vector = vectorizer.transform([user_input])
    cosine_similarities = cosine_similarity(user_vector, vectorized_text).flatten()
    max_similarity_index = cosine_similarities.argmax()
    response = merged_df_1.loc[max_similarity_index, 'Réponse']
    return response

# Route to render the HTML template
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle user input and return chatbot response
@app.route('/get_response', methods=['POST'])
def get_chatbot_response():
    user_input = request.form['user_input']
    response = get_response(user_input)
    cursor.execute('INSERT INTO conversation_logs (user_input, chatbot_response) VALUES (%s, %s)', (user_input, response))
    conn.commit()
    return response

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
