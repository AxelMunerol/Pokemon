import json
import requests

url = "https://pokeapi.co/api/v2/pokemon/charizard"
response = requests.get(url)

if response.status_code == 200:
    # Convertir la réponse JSON en dictionnaire Python
    charizard = response.json()
url2= 'https://pokeapi.co/api/v2/pokemon/magikarp'
response2 = requests.get(url2)
if response.status_code == 200:
    # Convertir la réponse JSON en dictionnaire Python
    magikarp = response2.json()

def combat(f1,f2):
    fighter1 = {'name': f1["name"]}
    print(fighter1["name"])

combat(charizard,magikarp)