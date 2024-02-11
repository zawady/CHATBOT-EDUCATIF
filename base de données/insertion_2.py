import pandas as pd
import mysql.connector
from mysql.connector import Error

# Chemin vers votre fichier CSV
chemin_csv = 'scrapping-4.csv'

# Lecture du fichier CSV
df = pd.read_csv(chemin_csv)

# Connexion à la base de données MySQL
try:
    connection = mysql.connector.connect(
        host='localhost',
        database='chatbot',
        user='root',
        password='root'
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Insertion des données dans la table cours
        # Remarque : Cela suppose que la formation est déjà insérée et que vous disposez de son ID.
        # Vous devrez adapter cette partie pour gérer correctement les relations.
        for index, row in df.iterrows():
            # Ici, on suppose que l'ID de la formation est récupéré ou connu d'avance. Ceci est un exemple simplifié.
            id_formation = 1  # Exemple statique, remplacez par votre logique pour récupérer l'ID de la formation
            
            # Insertion dans la table cours
            cursor.execute("INSERT INTO cours (titre, id_formation) VALUES (%s, %s)", (row['Titre de la section'], id_formation))
            id_cours = cursor.lastrowid  # Récupération de l'ID du cours inséré

            # Insertion dans la table videos
            cursor.execute("INSERT INTO videos (titre, lien, id_cours) VALUES (%s, %s, %s)", (row['Titre de la vidéo'], row['Source'], id_cours))
            
            connection.commit()

        print("Données insérées avec succès dans les tables cours et videos.")

except Error as e:
    print(f"Erreur lors de la connexion à MySQL ou lors de l'insertion des données: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connexion à MySQL fermée.")
