import random
import requests

def get_type_effectiveness():
    type_effectiveness = {}
    try:
        # Retrieve all Pokémon types
        response = requests.get("https://pokeapi.co/api/v2/type/")
        response.raise_for_status()
        data = response.json()

        for type_info in data['results']:
            type_id = type_info['url'].split('/')[-2]
            effectiveness_response = requests.get(f"https://pokeapi.co/api/v2/type/{type_id}/")
            effectiveness_response.raise_for_status()
            effectiveness_data = effectiveness_response.json()

            # Save type effectiveness
            type_effectiveness[type_info['name']] = {
                'double_damage_to': {effect['name']: 2 for effect in effectiveness_data['damage_relations']['double_damage_to']},
                'half_damage_to': {effect['name']: 0.5 for effect in effectiveness_data['damage_relations']['half_damage_to']},
                'no_damage_to': {effect['name']: 0 for effect in effectiveness_data['damage_relations']['no_damage_to']},
            }
    except requests.RequestException as e:
        print(f"Error retrieving types: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return type_effectiveness

def get_stat(pokemon, stat_name):
    # Get the requested stat (base_stat) from the Pokémon
    for stat in pokemon['stats']:
        if stat['stat']['name'] == stat_name:
            return stat['base_stat']
    return None  # Return None if the stat is not found

def get_move_details(move_url):
    response = requests.get(move_url)
    if response.status_code == 200:
        return response.json()  # Return move details as a dictionary
    else:
        print(f"Error during GET request to {move_url}")
        return None

def combat(f1, f2):
    # Choose 4 moves
    fighter1_moves = random.sample(f1["moves"], 4)
    fighter2_moves = random.sample(f2["moves"], 4)

    # Get types
    type1_f1 = f1["types"][0]["type"]["name"]
    type2_f1 = f1["types"][1]["type"]["name"] if len(f1["types"]) > 1 else None
    type1_f2 = f2["types"][0]["type"]["name"]
    type2_f2 = f2["types"][1]["type"]["name"] if len(f2["types"]) > 1 else None

    # Prepare fighters with relevant stats
    fighter1 = {
        'name': f1["name"],
        'hp': get_stat(f1, 'hp'),
        'attack_phy': get_stat(f1, 'attack'),
        'attack_spe': get_stat(f1, 'special-attack'),
        'speed': get_stat(f1, 'speed'),
        'defense_phy': get_stat(f1, 'defense'),
        'defense_spe': get_stat(f1, 'special-defense'),
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
        'defense_spe': get_stat(f2, 'special-defense'),
        'type1': type1_f2,
        'type2': type2_f2,
        'moves': [move["move"]["url"] for move in fighter2_moves]
    }

    print(fighter1)
    print(fighter2)

    # Determine who attacks first
    if fighter1['speed'] > fighter2['speed']:
        attaquant, defenseur = fighter1, fighter2
    elif fighter1['speed'] == fighter2['speed']:
        attaquant, defenseur = random.choice([(fighter1, fighter2), (fighter2, fighter1)])
    else:
        attaquant, defenseur = fighter2, fighter1

    print(f"Le combat commence! {attaquant['name']} attaque en premier!")

    # Combat loop
    while defenseur['hp'] > 0:
        move_url = random.choice(attaquant['moves'])
        move_details = get_move_details(move_url)

        if move_details is None:
            print("Failed to retrieve move details, skipping turn.")
            continue  # Skip this turn if move details cannot be retrieved

        attack_power = move_details.get("power", 0)
        if not isinstance(attack_power, int) or attack_power < 0:
            attack_power = 0  # Reset to 0 if not an integer or negative
        typeatk = move_details['damage_class']['name']

        # Set appropriate defense
        defenseur['defense'] = defenseur['defense_spe'] if typeatk == 'special' else defenseur['defense_phy']

        effectiveness = get_type_effectiveness()
        move_type_name = move_details['type']['name']

        # Check effectiveness against defender's types
        for effective_type in effectiveness[move_type_name]['double_damage_to']:
            if effective_type in [defenseur['type1'], defenseur['type2']]:
                print(f"{move_type_name} cause le double des dégâts contre {effective_type}!")
                attack_power *= 2

        for half_damage_type in effectiveness[move_type_name]['half_damage_to']:
            if half_damage_type in [defenseur['type1'], defenseur['type2']]:
                print(f"{move_type_name} cause moitié des dégâts contre {half_damage_type}!")
                attack_power *= 0.5

        for no_damage_type in effectiveness[move_type_name]['no_damage_to']:
            if no_damage_type in [defenseur['type1'], defenseur['type2']]:
                print(f"{move_type_name} ne cause aucun dégât contre {no_damage_type}!")
                attack_power = 0  # Set attack power to 0

        # Calculate damage
        damage = attack_power - defenseur['defense']
        damage = max(damage, 1)  # Ensure there's always at least 1 damage

        defenseur['hp'] -= damage

        print(f"{attaquant['name']} attaque {defenseur['name']} avec {move_details['name']} et inflige {damage} dégâts.")

        # Check if the defender is defeated
        if defenseur['hp'] <= 0:
            defenseur['hp'] = 0
            print(f"La vie de {defenseur['name']} est maintenant {defenseur['hp']}")
            print(f"{defenseur['name']} a été vaincu! {attaquant['name']} est le gagnant!")
            return attaquant

        # Show the remaining HP of the defender
        print(f"La vie de {defenseur['name']} est maintenant {defenseur['hp']}")

        # Switch roles for the next turn
        attaquant, defenseur = defenseur, attaquant
