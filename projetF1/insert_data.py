from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['monprojetDB']
collection = db['courses']

# Données à insérer
data = [
    {"position": "1", "driver": "Max Verstappen", "team": "Red Bull Racing", "time": "1:32:00"},
    {"position": "2", "driver": "Lewis Hamilton", "team": "Mercedes", "time": "1:32:30"},
    {"position": "3", "driver": "Charles Leclerc", "team": "Ferrari", "time": "1:33:00"}
]

# Insertion des données
collection.insert_many(data)
print("Données insérées avec succès !")
