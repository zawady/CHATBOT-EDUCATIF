import pandas as pd
import mysql.connector
from mysql.connector import Error
import re

# Fonction pour se connecter à la base de données MySQL
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='chatbot',
            user='root',
            password='root'
        )
        return connection
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return None

# Fonction pour modifier les tables
def modify_tables(connection):
    try:
        cursor = connection.cursor()

        # Ajouter la colonne 'contenu' à la table 'cours'
        cursor.execute("ALTER TABLE cours ADD COLUMN contenu TEXT")
        print("Colonne 'contenu' ajoutée avec succès à la table 'cours'.")
    except Error as e:
        print(f"Erreur lors de la modification des tables: {e}")

# Fonction pour nettoyer le texte en supprimant les caractères spéciaux et emojis
def clean_text(text):
    # Supprime les emojis et certains caractères spéciaux
    clean = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return clean

# Fonction principale pour insérer des données
def insert_data_from_csv(chemin_csv):
    df = pd.read_csv(chemin_csv)
    connection = connect_to_mysql()
    if connection is not None:
        modify_tables(connection)
        cursor = connection.cursor()
        for index, row in df.iterrows():
            # Nettoie le contenu pour supprimer les caractères spéciaux et les emojis
            contenu_clean = clean_text(row['Contenu'])
            # Insérer dans 'cours', incluant le 'contenu'
            cursor.execute("INSERT INTO cours (titre, id_formation, contenu) VALUES (%s, %s, %s)", (row['Titre de la section'], 1, contenu_clean))  # Remplacez '1' par votre logique pour l'id_formation
            connection.commit()
        print("Données insérées avec succès dans la table 'cours'.")
        cursor.close()
        connection.close()
    else:
        print("Connexion à MySQL échouée.")

# Chemin vers votre fichier CSV
chemin_csv = 'scrapping-4.csv'
insert_data_from_csv(chemin_csv)
