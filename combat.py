# import json
# import requests
# url1 = 'https://pokeapi.co/api/v2/pokemon/weedle'
# url2 = 'https://pokeapi.co/api/v2/pokemon/squirtle'
# response1 = requests.get(url1)
# response2 = requests.get(url2)
#
# # Si la requête réussit
# if response1.status_code == 200:
#     # Convertir la réponse JSON en dictionnaire Python
#     weedle = response1.json()
# if response1.status_code == 200:
#     # Convertir la réponse JSON en dictionnaire Python
#     squirtle = response2.json()
def get_stat(pokemon, stat_name):
    # Parcours les stats et retourne la stat demandée (base_stat) du Pokémon
    for stat in pokemon['stats']:
        if stat['stat']['name'] == stat_name:
            return stat['base_stat']
    return None  # Si la stat n'est pas trouvée, retourne None

def combat(f1,f2):
    fighter1 = {'name': f1["name"], 'hp' : get_stat(f1,'hp'),'attack': get_stat(f1,'attack'), 'speed': get_stat(f1,'speed')}
    fighter2 = {'name': f2["name"], 'hp': get_stat(f2, 'hp'), 'attack': get_stat(f2, 'attack'), 'speed' : get_stat(f2,'speed')}

    if fighter1['speed'] < fighter2['speed']:
        attaquant, defenseur = fighter1, fighter2
    elif fighter1['speed'] == fighter2['speed']:
        attaquant, defenseur = random.choice([(fighter1, fighter2), (fighter2, fighter1)])
    else:
        attaquant, defenseur = fighter2, fighter1
    print(f"Le combat commence! {attaquant['name']} attaque en premier!")

    while defenseur['hp'] > 0:
        attaquant, defenseur = defenseur, attaquant
        print(f"{attaquant['name']} attaque {defenseur['name']} avec une force de {attaquant['attack']}")
        defenseur['hp'] -= attaquant['attack']
        if defenseur['hp'] < 0:
            defenseur['hp'] = 0
            break
        print(f"La vie de {defenseur['name']} est maintenant {defenseur['hp']}")
        # Inverser les rôles


    print(f"{defenseur['name']} a été vaincu! {attaquant['name']} est le gagnant!")

    return attaquant, defenseur
