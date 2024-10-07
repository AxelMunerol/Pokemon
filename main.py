import requests
import random
import combat  # Assurez-vous que la fonction combat est bien définie dans combat.py


def tournoi(participants):
    # Boucle principale pour continuer jusqu'au gagnant final
    while len(participants) > 1:
        winners = []  # Liste pour les gagnants de chaque phase

        # Boucle des combats dans le tour actuel
        while len(participants) > 1:
            # Choisir deux participants pour combattre
            fighter_1 = participants[0]
            fighter_2 = participants[1]

            # Charger les pokémons depuis le dictionnaire 'pokemons'
            pokemon1 = pokemons[f'pokemon_{fighter_1}']
            pokemon2 = pokemons[f'pokemon_{fighter_2}']

            name_f1 = pokemon1["name"].capitalize()
            name_f2 = pokemon2["name"].capitalize()

            # Appeler la fonction de combat
            gagnant, perdant = combat.combat(pokemon1, pokemon2)
            if gagnant["name"] == name_f1:
                winner = fighter_1
            else:
                winner = fighter_2

            # Afficher les résultats
            print(f"Combat : {name_f1} vs {name_f2} -> Gagnant : {gagnant['name'].capitalize()}")
            print('-----------------------------------------')

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
        print("------------------------------------")
        print(f"NOUVEAU TOUR")
        print('-------------------------------------')

    # Affichage du gagnant final
    final_winner = participants[0]
    pokemon_final = pokemons[f'pokemon_{final_winner}']
    name_final = pokemon_final["name"].capitalize()

    print(f"Le grand gagnant est : {name_final}")
    return final_winner


# Code pour télécharger et charger les Pokémon
liste_id = [i for i in range(16)]  # IDs pour 16 pokémons aléatoires
urls = []
plage_1 = list(range(0, 1025))        # de 0 à 1025 inclus
plage_2 = list(range(10001, 10278))    # de 10001 à 10277 inclus
tous_les_numeros = plage_1 + plage_2
numeros_random = random.sample(tous_les_numeros, 16)

# Récupérer les URLs pour les Pokémon aléatoires
for chiffre in numeros_random:
    urls.append(f'https://pokeapi.co/api/v2/pokemon/{chiffre}')

# Dictionnaire pour stocker les Pokémon
pokemons = {}

# Télécharger les données des Pokémon
for index, url in enumerate(urls):
    response = requests.get(url)
    if response.status_code == 200:
        pokemons[f'pokemon_{index}'] = response.json()
    else:
        print(f"Erreur lors de la récupération de {url}: {response.status_code}")

# Lancer le tournoi
tournoi(liste_id)
