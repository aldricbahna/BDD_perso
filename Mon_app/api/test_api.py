import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "Jour semaine": "lundi",
    "Type": "Stage",
    "A l'étranger": "oui",
    "Parents": 0,
    "Eugé": 1,
    "Sport": 0,
    "Ciné": 0,
    "Film": 0,
    "Docu": 0,
    "Restau": 1,
    "Fast food": 0,
    "Café/bar solo": 0,
    "Lecture dehors": 0,
    "Café/bar avec copains": 0,
    "Repas copains": 0,
    "Vois copains": 0,
    "Soirée chill": 0,
    "Soirée": 0,
    "Dodo avec Eugé": 1,
    "Messe": 0,
    "Copains": "",
    "Activité": "",
    "Transport": "",
    "Match de sport": 0,
    "Footing": 0,
    "Somme réseaux": 52,
    "Lecture": 1
}

response = requests.post(url, json=data)
print(response.json())
