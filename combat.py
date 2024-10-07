import random

def get_stat(pokemon, stat_name):
    # Parcours les stats et retourne la stat demandée (base_stat) du Pokémon
    for stat in pokemon['stats']:
        if stat['stat']['name'] == stat_name:
            return stat['base_stat']
    return None  # Si la stat n'est pas trouvée, retourne None

def combat(f1, f2):
    # Préparer les deux combattants avec leurs stats pertinentes
    fighter1 = {'name': f1["name"], 'hp': get_stat(f1, 'hp'), 'attack': get_stat(f1, 'attack'), 'speed': get_stat(f1, 'speed')}
    fighter2 = {'name': f2["name"], 'hp': get_stat(f2, 'hp'), 'attack': get_stat(f2, 'attack'), 'speed': get_stat(f2, 'speed')}

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