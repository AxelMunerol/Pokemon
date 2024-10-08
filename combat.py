import random
import requests

def get_type_effectiveness():
    type_effectiveness = {}
    try:
        response = requests.get("https://pokeapi.co/api/v2/type/")
        if response.status_code == 200:
            data = response.json()
            for type_info in data['results']:
                type_id = type_info['url'].split('/')[-2]
                effectiveness_response = requests.get(f"https://pokeapi.co/api/v2/{type_id}/")
                if effectiveness_response.status_code == 200:
                    effectiveness_data = effectiveness_response.json()
                    # Enregistrer les effets de type
                    type_effectiveness[type_info['name']] = {
                        'double_damage_to': {effect['name']: 2 for effect in
                                             effectiveness_data['damage_relations']['double_damage_to']},
                        'half_damage_to': {effect['name']: 0.5 for effect in
                                           effectiveness_data['damage_relations']['half_damage_to']},
                        'no_damage_to': {effect['name']: 0 for effect in
                                         effectiveness_data['damage_relations']['no_damage_to']},
                    }
    except Exception as e:
        print(f"Erreur lors de la récupération des types : {e}")

    return type_effectiveness
print(get_type_effectiveness())
def get_stat(pokemon, stat_name):
    # Parcours les stats et retourne la stat demandée (base_stat) du Pokémon
    for stat in pokemon['stats']:
        if stat['stat']['name'] == stat_name:
            return stat['base_stat']
    return None  # Si la stat n'est pas trouvée, retourne None


def get_move_details(move_url):
    response = requests.get(move_url)
    if response.status_code == 200:
        return response.json()  # Retourne les détails du move sous forme de dictionnaire
    else:
        print(f"Erreur lors de la requête GET vers {move_url}")
        return None


def combat(f1, f2):
    # Choix de 4 attaques
    fighter1_moves = random.sample(f1["moves"], 4)
    fighter2_moves = random.sample(f2["moves"], 4)

    # Cherche des types
    type1_f1 = f1["types"][0]["type"]["name"]
    type2_f1 = f1["types"][1]["type"]["name"] if len(f1["types"]) > 1 else None
    type1_f2 = f2["types"][0]["type"]["name"]
    type2_f2 = f2["types"][1]["type"]["name"] if len(f2["types"]) > 1 else None

    # Préparer les deux combattants avec leurs stats pertinentes
    fighter1 = {
        'name': f1["name"],
        'hp': get_stat(f1, 'hp'),
        'attack_phy': get_stat(f1, 'attack'),
        'attack_spe': get_stat(f1, 'special-attack'),
        'speed': get_stat(f1, 'speed'),
        'defense_phy': get_stat(f1, 'defense'),
        'defense_spe': get_stat(f1, 'special-defense'),  # Utilise f1 au lieu de f2
        'type1': type1_f1,
        'type2': type2_f1,
        'moves': [move["move"]["url"] for move in fighter1_moves]
    }

    fighter2 = {
        'name': f2["name"],
        'hp': get_stat(f2, 'hp'),
        'attack_phy': get_stat(f2, 'attack'),
        'attack_spe': get_stat(f2, 'special-attack'),
        'speed': get_stat(f2, 'speed'),
        'defense_phy': get_stat(f2, 'defense'),
        'defense_spe': get_stat(f2, 'special-defense'),  # Utilise f2 ici
        'type1': type1_f2,
        'type2': type2_f2,
        'moves': [move["move"]["url"] for move in fighter2_moves]
    }

    print(fighter1)
    print(fighter2)


    # Déterminer qui attaque en premier
    if fighter1['speed'] > fighter2['speed']:
        attaquant, defenseur = fighter1, fighter2
    elif fighter1['speed'] == fighter2['speed']:
        attaquant, defenseur = random.choice([(fighter1, fighter2), (fighter2, fighter1)])
    else:
        attaquant, defenseur = fighter2, fighter1

    print(f"Le combat commence! {attaquant['name']} attaque en premier!")
    # Boucle de combat
    while defenseur['hp'] > 0:
        move_url = random.choice(attaquant['moves'])
        move_details = get_move_details(move_url)
        attaquant['attack']=move_details["power"]
        if not isinstance(attaquant['attack'], int):
            attaquant['attack'] = 0  # Remettre à 0 si ce n'est pas un entier
        typeatk = move_details['damage_class']['name']

        if typeatk == 'special':
            defenseur['defense'] = defenseur['defense_spe']
        else:
            defenseur['defense'] = defenseur['defense_phy']


        # Calcule des dégâts
        damage = attaquant['attack'] - defenseur['defense']
        if damage < 0:
            damage = 1  # S'assure qu'il y ait toujours des dégâts

        defenseur['hp'] -= damage

        print(
            f"{attaquant['name']} attaque {defenseur['name']} avec {move_details['name']} et inflige {damage} dégâts.")

        # Vérifier si le défenseur a été vaincu
        if defenseur['hp'] <= 0:
            defenseur['hp'] = 0
            print(f"La vie de {defenseur['name']} est maintenant {defenseur['hp']}")
            print(f"{defenseur['name']} a été vaincu! {attaquant['name']} est le gagnant!")
            return attaquant

        # Afficher la vie restante du défenseur
        print(f"La vie de {defenseur['name']} est maintenant {defenseur['hp']}")

        # Inverser les rôles pour le prochain tour
        attaquant, defenseur = defenseur, attaquant
