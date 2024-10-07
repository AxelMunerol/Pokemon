
#import combat
import requests
import random
import json
def tournoi(participants):
    # Boucle principale pour continuer jusqu'au gagnant final
    while len(participants) > 1:
        winners = []  # Liste pour les gagnants de chaque phase

        # Boucle des combats dans le tour actuel
        while len(participants) > 1:
            # Choisir deux participants pour combattre
            fighter_1 = participants[0]
            fighter_2 = participants[1]

            f1 = pokemons[f'pokemon_{fighter_1}']
            name_f1 = f1["name"].capitalize()

            f2 = pokemons[f'pokemon_{fighter_2}']
            name_f2 = f2["name"].capitalize()


            # Choisir aléatoirement le gagnant du combat
            winner = random.choice([fighter_1, fighter_2])
            data_winner = pokemons[f'pokemon_{winner}']
            name_winner = data_winner["name"].capitalize()
            print(f"Combat : {name_f1} vs {name_f2} -> Gagnant : {name_winner}")

            # Ajouter le gagnant à la liste des gagnants
            winners.append(winner)

            # Supprimer les combattants de la liste
            participants = participants[2:]

        # Si un participant n'a pas eu de pair, il est qualifié automatiquement
        if len(participants) == 1:
            lone_participant = participants.pop()
            winners.append(lone_participant)
            print(f"{lone_participant} est qualifié automatiquement.")

        # Les gagnants deviennent les nouveaux participants
        participants = winners
        print(f"nouveau tour")

    # Affichage du gagnant final
    final_winner = participants[0]
    f1 = pokemons[f'pokemon_{final_winner}']
    name_f1 = f1["name"].capitalize()

    print(f"Le grand gagnant est : {name_f1}")
    return final_winner

liste_chiffre_tournoi = []
urls =[]
liste_id = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

url = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"
response = requests.get(url)

# Si la requête réussit
if response.status_code == 200:
    # Convertir la réponse JSON en dictionnaire Python
    data = response.json()

    # Récupérer uniquement le champ 'results'
    results = data.get('results', None)
else:
    print(f"Erreur lors de la requête: {response.status_code}")


plage_1 = list(range(0, 1025))        # de 0 à 1025 inclus
plage_2 = list(range(10001, 10278))    # de 1001 à 10277 inclus
tous_les_numeros = plage_1 + plage_2
numeros_random = random.sample(tous_les_numeros, 16)

for chiffre in numeros_random:
    urls.append(f'https://pokeapi.co/api/v2/pokemon/{chiffre}')

pokemons = {}

for index, url in enumerate(urls):
    response = requests.get(url)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Enregistrer la réponse dans le dictionnaire avec une clé unique
        pokemons[f'pokemon_{index}'] = response.json()
    else:
        print(f"Erreur lors de la récupération de {url}: {response.status_code}")

random.shuffle(liste_id)



tournoi(liste_id)
#combat.coucou()

