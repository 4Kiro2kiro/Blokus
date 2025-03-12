![badge-python](https://badgen.net/static/Python/3.13/red) ![badge-python](https://badgen.net/static/Python/3.6+/blue)

![logo-blokus](https://vignette.wikia.nocookie.net/logopedia/images/a/a7/Blokus.png/revision/latest?cb=20121223205007)

## Blokus Game

Blokus est un jeu de stratégie où les joueurs placent des pièces sur un plateau de jeu. Ce projet implémente le jeu Blokus en Python.

### Structure du projet

Le projet est organisé en plusieurs fichiers pour une meilleure modularité :

```
.
├── LICENSE
├── README.md
├── application.sh
├── docs
│   ├── cahierTestsValidation.md
│   └── specificationsFonctionnelles.md
├── server.sh
├── src
│   └── game_blokus
│       ├── __init__.py
│       ├── __main__.py
│       ├── board.py
│       ├── bot_player.py
│       ├── display.py
│       ├── game.py
│       ├── network_client.py
│       ├── piece.py
│       ├── player.py
│       ├── save_load.py
│       ├── server.py
│       ├── state.py
│       ├── spectator.py
│       ├── tutorial.py
│       └── utils.py
├── test
│   ├── __init__.py
│   └── test_game.py
└── test.sh

```

- `board.py` : Contient la classe `Board` qui représente le plateau de jeu.
- `piece.py` : Contient la classe `Piece` qui représente une pièce du jeu.
- `player.py` : Contient la classe `Player` qui représente un joueur.
- `state.py` : Contient la classe `GameState` qui représente l'état du jeu.
- `game.py` : Contient la classe `BlokusGame` qui gère la logique du jeu et l'interface utilisateur.
- `save_load.py` : Contient la logique qui permet de save la game et de revenir sur la version sauvegardée
- `tutorial.py` : Contient le tutoriel
- `utils.py` : Contient des outils créés réutilisés dans le projet
- `server.py`: Contient la logique du serveur
- `network_client.py` : Contient la logique locale du joueur pour ce qui est l'interaction du serveur
- `display.py` : Contient la logique d'affichage du plateau

### Prérequis

- Python 3.6 ou supérieur

## Installation

Clonez le dépôt :

   ```sh
   git clone https://gitlab.cri.epita.fr/anselme.garnier/project-s1
   cd project-s1/src/
   ```

## Exécution du jeu

Pour exécuter le jeu, utilisez la commande suivante :

```sh
python3 -m game_blokus
```

ou pour plus de simplicité executez directement le fichier `application.sh`

```sh
cd project-s1
./application.sh
```

## Utilisation

Lorsque vous exécutez le jeu vous serez invité à sélectionner le mode de jeu entre `Solo contre IA`, `Local Multiplayer`, `Online Multiplayer` et `Tutorial` suivez les instructions soit dans l'odre : choisir le niveau de difficulté du bot, entrer le nombre de joueurs (2-4), pour le mode en reseau avant tout chose executez le fichier `server.sh` puis fait create game dans les choix, pour les autres joueurs ils peuvent se connecter via l'id que vous trouverez dans le fil du terminal de `server.sh`, pour le tutoriel tout est guidé. Ensuite, suivez les instructions à l'écran pour jouer au jeu.

### Commandes

- `s` : Sauvegarder la partie
- `l` : Charger une partie sauvegardée
- `h` : Afficher l'aide
- `q` : Quitter le jeu

### Placement des pièces

1. Entrez les coordonnées de la ligne (x) et de la colonne (y).
2. Choisissez la rotation (0-3) pour des rotations de 90° dans le sens des aiguilles d'une montre.
3. Choisissez si vous voulez retourner la pièce (y/n).
4. Confirmez le placement après la prévisualisation.

## Contribuer

Les contributions sont les bienvenues ! Veuillez ouvrir une issue ou une pull request pour discuter des modifications que vous souhaitez apporter.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

**Avertissement :** Blokus™ et tous les logos, symboles et marques associés sont la propriété de **Mattel, Inc**.. Ce projet n'est ni affilié à, ni approuvé ou sponsorisé par Mattel. Tous les droits relatifs au jeu Blokus et à la propriété intellectuelle associée appartiennent à Mattel. Le jeu Blokus a été conçu par Bernard Tavitian et publié pour la première fois en 2000 par Sekkoïa, puis acquis par Mattel en 2009.

## Conclusion

En suivant les instructions de ce README, vous devriez être en mesure de configurer et d'exécuter votre projet Blokus sans problème. Si vous avez des questions ou des problèmes supplémentaires, n'hésitez pas à demander de l'aide.
