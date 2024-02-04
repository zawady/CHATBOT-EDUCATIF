#TTEEEESSSSSTTTTTT
from transformers import TapexTokenizer, BartForConditionalGeneration
import pandas as pd
import numpy as np

# Étape 1 : Lire le fichier CSV
data = pd.read_csv('scrapping_traité.csv')

# Étape 2 : Nettoyage des données
data_clean = data[['Titre de la section', 'Contenu', 'Nom du professeur', 'Description du professeur', 'Titre du cours']].copy()
data_clean['Contenu'] = data_clean['Contenu'].str.strip()  # Nettoyage du contenu
data_clean['Titre de la section'] = data_clean['Titre de la section'].str.strip()  # Nettoyage du titre de la section

# Étape 3 : Structuration des données pour TAPEx
columns = ['Titre de la section', 'Contenu', 'Nom du professeur', 'Titre du cours']
table_example = data_clean[columns].head()

# Initialisation du tokenizer et du modèle TAPEx
tokenizer = TapexTokenizer.from_pretrained("microsoft/tapex-large-finetuned-wtq")
model = BartForConditionalGeneration.from_pretrained("microsoft/tapex-large-finetuned-wtq")

# Définition de max_length
max_length = 512  

# Préparation de la table et de la requête pour TAPEx
query = "Quelles sont les étapes recommandées dans le contenu pour suivre ce cours ?"

# Assurez-vous que `table_example` est un DataFrame
encoding = tokenizer(table=table_example, query=query, return_tensors="pt", truncation=True, padding="max_length", max_length=max_length)

# Génération de la réponse
outputs = model.generate(**encoding)

# Décodez les sorties
decoded_outputs = tokenizer.batch_decode(outputs, skip_special_tokens=True)
print(decoded_outputs)
