import pandas as pd
import mysql.connector
from mysql.connector import Error

# Connexion à MySQL
try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  
        password='root'  
    )

    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS chatbot")
        cursor.execute("USE chatbot")

        # Création des tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(255),
                description VARCHAR(255)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS formation (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titre VARCHAR(255),
                duree VARCHAR(255),
                id_prof INT,
                FOREIGN KEY (id_prof) REFERENCES profs(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cours (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titre VARCHAR(255),
                id_formation INT,
                FOREIGN KEY (id_formation) REFERENCES formation(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titre VARCHAR(255),
                lien VARCHAR(255),
                id_cours INT,
                FOREIGN KEY (id_cours) REFERENCES cours(id)
            )
        """)

        print("Base de données et tables créées avec succès.")

except Error as e:
    print(f"Erreur lors de la connexion à MySQL: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connexion à MySQL est fermée.")

# Lecture du fichier CSV
df = pd.read_csv('scrapping-4.csv')

