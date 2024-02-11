import pandas as pd
import mysql.connector
from mysql.connector import Error

# Lecture du fichier CSV
df = pd.read_csv('scrapping-4.csv')

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

        # Préparation des données pour insertion
        # Supposons que votre CSV a les colonnes nécessaires pour remplir les tables
        # Vous devrez adapter cette partie en fonction de votre schéma de base de données et de la structure du CSV

        # Insertion dans la table profs
        profs_data = df[['Nom du professeur', 'Description du professeur']].drop_duplicates()
        for index, row in profs_data.iterrows():
            cursor.execute("INSERT INTO profs (nom, description) VALUES (%s, %s)", (row['Nom du professeur'], row['Description du professeur']))
            connection.commit()

        # Pour chaque insertion, récupérer l'ID généré pour utilisation ultérieure
        # Exemple simple d'insertion dans la table formation, ajustez selon votre schéma
        # Notez que cet exemple ne gère pas les relations entre les tables, vous devrez adapter votre code pour gérer ces relations

        # Supposons que chaque ligne du CSV correspond à une formation distincte
        # Cette partie est fortement simplifiée, vous aurez besoin d'adapter la logique en fonction de vos données et relations
        for index, row in df.iterrows():
            # Supposons que le prof a déjà été inséré et que nous avons son ID (vous aurez besoin d'une logique pour récupérer cet ID)
            prof_id = 1  # Exemple statique, remplacez par la logique appropriée pour récupérer l'ID réel
            cursor.execute("INSERT INTO formation (titre, duree, id_prof) VALUES (%s, %s, %s)", (row['Titre du cours'], row['Durée du cours'], prof_id))
            connection.commit()

        # Insérer des données dans les autres tables en suivant une logique similaire

        print("Données insérées avec succès.")

except Error as e:
    print(f"Erreur lors de la connexion à MySQL ou lors de l'insertion des données: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connexion à MySQL fermée.")
