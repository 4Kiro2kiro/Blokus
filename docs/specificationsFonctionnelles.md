# Spécifications Fonctionnelles

## 1. Introduction
Ce document décrit les spécifications fonctionnelles de l'application Blokus, un jeu de stratégie où les joueurs placent des pièces sur un plateau de jeu. Les spécifications fonctionnelles décrivent les différentes fonctions que l'application offre à l'utilisateur, en se plaçant de son point de vue externe. Elles ne décrivent pas comment l'application le fait concrètement, de façon interne.

Les spécifications fonctionnelles sont les plus précises possible. Pour chaque fonction, elles décrivent notamment les entrées attendues de l'utilisateur et les sorties que l'application affiche en retour. Elles décrivent également la dynamique des échanges entre l'utilisateur et l'application, et notamment qui, de l'application ou de l'utilisateur, a l'initiative d'activer la fonction. Elles décrivent bien sûr les cas d'utilisation nominaux de la fonction, mais aussi les cas d'utilisation erronés et la réponse de l'application dans ces cas-là.

## 2. Motivation

La phase de spécification fonctionnelle intervient avant celle de développement, de façon à ne pas se confronter à toutes les questions en même temps : d'une part la question de ce que doit faire l'application et d'autre part celle de comment elle doit le faire, sachant que, sauf exceptions, les deux sont indépendantes.

Avoir des spécifications fonctionnelles précises permet de savoir exactement ce qu'il faut coder pour traiter les différents cas d'utilisation de l'application. Avoir des spécifications fonctionnelles complètes permet d'avoir un objectif bien défini et de répondre à des questions importantes comme « avons-nous terminé les développements ? » et dans la négative, « quel est notre degré d'avancement ? ».

## 3. Fonctions de base

### 3.1 Afficher l’état courant du plateau
Objectif : Permettre à l’utilisateur de visualiser en temps réel l’état du jeu, facilitant ainsi la compréhension des coups déjà joués et des pièces encore disponibles pour chaque joueur.
##### Entrée Utilisateur : 
Aucun input direct n’est requis pour cette fonction ; elle est déclenchée automatiquement après chaque tour.

##### Sortie : 
L’application affiche une représentation graphique du plateau de jeu indiquant les pièces placées et les cellules vides. Chaque pièce est identifiable par la couleur associée au joueur qui l’a posée.

##### Initiative :
 Cette fonction est activée par l’application, et non par l’utilisateur, à chaque mise à jour du plateau (après chaque coup).

##### Cas Nominal :
 Le plateau est affiché correctement avec les pièces déjà placées et l’état libre ou occupé de chaque cellule.

##### Cas d’utilisation erronés :
 Aucun.

### 3.2 Jouer et contrôler un coup

###### Objectif :
 Permettre aux utilisateurs de sélectionner une pièce parmi celles qui leur restent et de la placer sur le plateau conformément aux règles du jeu.
##### Entrée Utilisateur :
- Sélection de la pièce : L’utilisateur choisit une pièce parmi celles qui lui restent.
- Placement de la pièce : L’utilisateur désigne une position sur le plateau pour poser la pièce.
##### Sortie :
 Une fois la pièce placée, l’application confirme le coup et affiche le plateau mis à jour.
##### Initiative :
 Cette fonction est déclenchée par l’utilisateur à chaque tour lorsqu’il souhaite poser une pièce.

###### Cas Nominal :
 L’utilisateur place une pièce dans une position autorisée, et le plateau est mis à jour.
##### Cas d’Erreur :
- Position Invalide : Si la pièce est placée en dehors du plateau ou dans une position déjà occupée, l’application affiche un message précisant que la position est invalide.
- Non-respect des Règles : Si le placement ne respecte pas les règles (ex. contact requis entre deux pièces du même joueur), l’application indique le problème et invite le joueur à sélectionner une nouvelle position ou pièce.
- Pièce Indisponible : Si l’utilisateur tente de jouer une pièce qu’il n’a plus, un message le lui signale.

### 3.3 Détecter la fin de partie pour un joueur
##### Objectif :
 Détecter les conditions de fin de partie pour chaque joueur et, si nécessaire, mettre fin au jeu en désignant le vainqueur.
##### Entrée Utilisateur :
 Aucun input direct n’est requis ; la vérification de la fin de partie se fait automatiquement après chaque tour.
##### Sortie :
- Lorsque toutes les pièces d’un joueur sont placées ou qu’il ne peut plus jouer, l’application l’indique.
- En fin de partie, l’application affiche un message annonçant le joueur gagnant.
##### Initiative :
 Cette fonction est activée par l’application à la fin de chaque tour pour vérifier les conditions de fin.
##### Cas Nominal :
 La fin de partie est détectée lorsque plus aucun coup n’est possible ou que toutes les pièces ont été jouées.

##### Cas d’utilisation erronés :
 Aucun.

## 4. Fonction additionnelle n° 1

### Système de sauvegarde
##### Description :
 Cette fonction permet de charger et sauvegarder l’état actuel du jeu dans un fichier pour pouvoir le reprendre plus tard.

##### Entrées :
 Aucune, enregistre au fur et à mesure les placementds dans la grille.

##### Sorties :
 Fichier de sauvegarde créé ou mis à jour.

###### Dynamique des échanges :
 L'utilisateur peut demander à tout moment de sauvegarder la partie.

##### Cas d’utilisation erronés : 
- Erreur d’écriture dans le fichier (par exemple, permissions insuffisantes).


## 5. Fonction additionnelle n° 2

### Créer une partie en multijoueur

##### Description :

L'objectif est de pouvoir choisir dans le pannel de selection des modes un moyen de jouer en network, ou local, avec 1, 2 ou 3 personnes

##### Entrées :

- Pour l'hôte on va lui demander de créer le serveur donc il n'aura qu'à interagir avec le menu pour pouvoir créer une serveur sur son ordinateur
- Pour les invités, on devra leur fournir l'adresse IP de l'hôte, ainsi il pourront se connecter à la partie

##### Sorties

Affiche si le jeu est en attente de connexion, si les invités sont connectés ou non. Il serait aussi intéressant de savoir quand un joeur se déconnecte. 

##### Dynamique des échanges :

- l'hôte intéragit au début pour créer le serveur
- les invités intéragissent pour se connecter à l'hôte en rentrant son IP


##### Cas d’utilisation erronés : 

- Le port de l'hôte nécessaire pour héberger et lancer le serveur est fermé, des problèmes de firewall.

- Si le joueur se déconnecte le jeu ne doit pas continuer sinon le jeu sera bloqué pour les autres joueurs

## 6. Fonction additionnelle n° 3

### Créer des bots de plusieurs niveaux de difficulté

##### Description :

L'objectif est de créer un bot permettant à un joueur seul de pouvoir joeur contre l'oridnateur. Il y aura trois niveaux de bots, le facile choisira des move aléatoires parmis les moves possibles, un bot medium qui va chercher à placer les pièces les plus grosses en premier et va chercher à aller vers le milieu afin de bloquer le joueur, le difficile va faire comme le medium mais bloquera plus le joeur dans le placement des coups. 


##### Entrées :

Aucune entrée n'est requise pas l'utilisateur. L'objectif du bot est de pouvoir jouer indépendament contre l'ordinateur. 

##### Sortie :

Le bot va jouer comme un joeur et affichera les pièces placées sur le plateau. 


##### Dynamique des échanges :

- le joeur joue contre nous 
- on demande au joueur de sélectionner le bot au début et son niveau de difficulté


##### Cas d’utilisation erronés : 

Si des cas sont mal gérés par le bot.





