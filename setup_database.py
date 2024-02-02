import mysql.connector
from mysql.connector import Error
import pandas as pd

# Définition de la fonction create_connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='root',
            database='chat',
            charset='utf8mb4'
        )
        print("Connection to MySQL DB successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def execute_query(connection, query):
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

def insert_data(df, conn):
    if conn is not None:
        for _, row in df.iterrows():
            with conn.cursor(buffered=True) as cursor:
                # Récupération de id_cours
                cursor.execute("SELECT id_cours FROM Cours WHERE titre_du_cours = %s", (row['Titre du cours'],))
                results = cursor.fetchall()
                if results:
                    id_cours = results[0][0]
                else:
                    continue  # Passer à l'itération suivante si aucun cours n'est trouvé
                
                # Récupération de id_professeur
                cursor.execute("SELECT id_professeur FROM Professeurs WHERE nom_du_professeur = %s", (row['Nom du professeur'],))
                results = cursor.fetchall()
                if results:
                    id_professeur = results[0][0]
                else:
                    continue  # Passer à l'itération suivante si aucun professeur n'est trouvé
                
                # Insertion des données dans la table Sections
                section_query = """
                INSERT INTO Sections (titre_de_la_section, contenu, titre_de_la_vidéo, source, id_cours, id_professeur) 
                VALUES (%s, %s, %s, %s, %s, %s);
                """
                cursor.execute(section_query, (row['Titre de la section'], row['Contenu'], row['Titre de la vidéo'], row['Source'], id_cours, id_professeur))
                conn.commit()
        print("Data inserted into Sections table successfully")
    else:
        print("Failed to insert data into Sections table due to DB connection issue")

if __name__ == "__main__":
    conn = create_connection()  # Établissement de la connexion
    df = pd.read_csv('scrapping-3.csv')  # Chargement des données depuis un fichier CSV
    insert_data(df, conn)  # Insertion des données dans la base de données
