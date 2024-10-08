Pokémon Battle Simulator
Ce projet est une simulation de combat Pokémon utilisant des données provenant de l'API PokeAPI. L'application permet de faire s'affronter deux Pokémon en simulant leurs attaques, en prenant en compte leurs statistiques, types, et moves, avec des ajustements d'efficacité de type (type effectiveness).

Fonctionnalités
Sélection automatique de mouvements : Chaque Pokémon sélectionne aléatoirement jusqu'à 4 moves parmi ceux qu'il possède.
Prise en compte des types : L'application prend en compte les types des Pokémon et l'efficacité des moves (double, moitié, ou pas de dégâts selon le type).
Gestion des statistiques : Les statistiques telles que la vitesse, l'attaque, la défense, etc., sont récupérées pour chaque Pokémon et utilisées dans les calculs des dégâts.
Combat simulé : Le Pokémon avec la meilleure vitesse attaque en premier. Si les vitesses sont égales, un choix aléatoire décide de l'attaquant. Le combat continue jusqu'à ce qu'un Pokémon soit KO.
Installation
Cloner le dépôt :

Copier le code
git clone https://github.com/username/pokemon-battle-simulator.git
cd pokemon-battle-simulator
Installer les dépendances : Assurez-vous d'avoir Python 3 installé. Ensuite, installez les dépendances requises avec pip :

Copier le code
pip install -r requirements.txt
Exécuter l'application : Vous pouvez lancer l'application avec :

Copier le code
python main.py
Dépendances
Python 3.x
Requests : Utilisé pour effectuer des appels à l'API PokeAPI.
Installer les dépendances en utilisant la commande suivante :

Copier le code
pip install requests
Utilisation
L'application simule des combats entre deux Pokémon, qui sont automatiquement sélectionnés à partir de l'API.

Étapes :
Récupération des Pokémon : L'application récupère deux Pokémon aléatoires de l'API PokeAPI pour les faire s'affronter.

Récupération des statistiques et des types : Les statistiques et types de chaque Pokémon sont récupérés via l'API, et utilisés dans les calculs de combat.

Choix des moves : Jusqu'à 4 moves sont sélectionnés aléatoirement pour chaque Pokémon.

Combat : Les deux Pokémon s'affrontent en utilisant leurs moves, en prenant en compte l'efficacité des types et leurs statistiques pour déterminer les dégâts infligés à l'adversaire.

Exemple de log de combat :

Le combat commence! Pikachu attaque en premier!
Pikachu attaque Bulbizarre avec Thunderbolt et inflige 30 dégâts.
La vie de Bulbizarre est maintenant 70.
Bulbizarre attaque Pikachu avec Vine Whip et inflige 15 dégâts.
La vie de Pikachu est maintenant 85.
...
Pikachu a été vaincu! Bulbizarre est le gagnant!
Fichiers principaux
main.py : Fichier principal qui lance le tournoi entre plusieurs Pokémon.
combat.py : Contient la logique du combat entre deux Pokémon.
pokeapi_helpers.py (optionnel) : Contient des fonctions d'aide pour récupérer les données de l'API PokeAPI (comme les statistiques, les moves, etc.).
Améliorations possibles
Ajouter une interface utilisateur (UI) pour rendre l'application plus interactive.
Implémenter un mode de tournoi avec plusieurs rounds.
Ajouter la possibilité pour l'utilisateur de choisir les Pokémon qui se battent.
Améliorer l'IA pour rendre les combats plus stratégiques en fonction des forces et faiblesses des Pokémon.
API utilisée
PokeAPI : API gratuite qui fournit des données sur les Pokémon, leurs statistiques, types, moves, et bien plus.
