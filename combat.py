import random
import requests

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
    fighter1_moves = random.sample(f1["moves"], 4 )
    fighter2_moves = random.sample(f2["moves"], 4 )


    # cherche des types
    type1_f1 = None
    type2_f1 = None
    for t in f1["types"]:
        if t["slot"] == 1:
            type1_f1 = t["type"]["name"]
        elif t["slot"] == 2:
            type2_f1 = t["type"]["name"]

    type1_f2 = None
    type2_f2 = None
    for t in f2["types"]:
        if t["slot"] == 1:
            type1_f2 = t["type"]["name"]
        elif t["slot"] == 2:
            type2_f2 = t["type"]["name"]
    # Préparer les deux combattants avec leurs stats pertinentes
    fighter1 = {'name': f1["name"], 'hp': get_stat(f1, 'hp'), 'attack_phy': get_stat(f1, 'attack'), 'attack_spe': get_stat(f1, 'special-attack'),'speed': get_stat(f1, 'speed'), 'defense_phy': get_stat(f1, 'defense'),'defense_spe': get_stat(f2, 'special-defense'),'type1': type1_f1,'type2': type2_f1,'moves': [move["move"]["url"] for move in fighter1_moves]}
    fighter2 = {'name': f2["name"], 'hp': get_stat(f2, 'hp'), 'attack_phy': get_stat(f2, 'attack'), 'attack_spe': get_stat(f2, 'special-attack'),'speed': get_stat(f2, 'speed'), 'defense_phy': get_stat(f2, 'defense'),'defense_spe': get_stat(f2, 'special-defense'),'type1': type1_f2,'type2': type2_f2,'moves': [move["move"]["url"] for move in fighter2_moves]}
    print(fighter2)
    print(fighter1)

    #choix phy ou spé
    if fighter1['attack_phy'] < fighter1['attack_spe']:
        fighter1['attack'] = fighter1['attack_spe']
        fighter2['defense'] = fighter2['defense_spe']
        print(f"{fighter1["name"]} CHOISIT SON ATK SPE")
    else:
        fighter1['attack'] = fighter1['attack_phy']
        fighter2['defense'] = fighter2['defense_phy']
        print(f"{fighter1["name"]} CHOISIT SON ATK PHY")

    if fighter2['attack_phy'] < fighter2['attack_spe']:
        fighter2['attack'] = fighter2['attack_spe']
        fighter1['defense'] = fighter1['defense_spe']
        print(f"{fighter2["name"]} CHOISIT SON ATK SPE")
    else:
        fighter2['attack'] = fighter2['attack_phy']
        fighter1['defense'] = fighter1['defense_phy']
        print(f"{fighter2["name"]} CHOISIT SON ATK PHY")



    #recalcul des attaques
    fighter1['attack'] -= fighter2['defense']
    fighter2['attack'] -= fighter1['defense']

    if fighter1['attack'] < 0:
        fighter1['attack'] = 1
    if fighter2['attack'] < 0:
        fighter2['attack'] = 1



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
        print(f"{attaquant['name']} attaque {defenseur['name']} avec une force de {attaquant['attack']}")
        defenseur['hp'] -= attaquant['attack']

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