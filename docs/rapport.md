# Rapport de Projet Blokus

---

## Introduction

Ce rapport présente un bilan complet du projet Blokus, en abordant les développements et les tests réalisés, l'organisation du projet, les difficultés rencontrées, et les apports du projet. 

---

## Bilan des Développements et des Tests

### Fonctionnalités Développées

Par rapport aux spécifications initiales à J1, les fonctionnalités suivantes ont été développées :
- **Mode Solo contre l'IA** : Les niveaux de difficulté `easy`, `medium`, et `hard` ont été implémentés.
- **Mode Multijoueur Local** : Support pour 2 à 4 joueurs.
- **Mode Multijoueur en Ligne** : Création et participation à des parties en ligne.
- **Tutoriel** : Un tutoriel interactif pour apprendre les règles et les stratégies du jeu.
- **Sauvegarde et Chargement** : Possibilité de sauvegarder et de charger des parties.

### Couverture des Tests

- **Tests Unitaires** : Les tests unitaires couvrent 80% des fonctionnalités critiques du jeu. Nous possedons 62 tests unitaires.
- **Tests Manuels** : Des tests manuels ont été effectués pour valider l'expérience utilisateur.  Nous verifions 12 scénarios.

### Pourcentage de Tests OK

- **Tests Unitaires** : 100% des tests unitaires passent avec succès.
- **Tests Manuels** : 100% des scénarios de tests manuels ont été validés.

---

## Organisation du Projet

### Répartition des Tâches

Nous nous sommes répartis les tâches dans le projet à trois. 

Pour ce projet, nous avons assigné les tâches grâce à un milestone et un board d'issues. Chaque difficulté rencontrée a été abordée collectivement afin que chacun puisse apporter son expertise sur chaque partie du jeu. La répartition était fondée sur la collaboration. 

De manière globale, Anselme s'est occupé des fonctionnalités de base, assisté par Henrique, et d'une part du developpement des IA ainsi que l'interface utilisateur.

Henrique s'est occupé de l'aspect multijoueur en particulier le multijoueur en ligne et a assisté Anselme dans la correction de bug.

Gabriel a aidé à corriger des bugs dans le projet. Il a implément le tutoriel et a participé à la conception des bots hard et medium.




### Utilisation des Outils

- **GitLab** : Utilisé pour le contrôle de version, la gestion des branches, et les merge requests.
- **IDE** : Visual Studio Code a été utilisé pour le développement, avec des extensions pour Python.
- **Outils de Communication** : Discord a été utilisé pour la communication dans le groupe.

---

## Difficultés Rencontrées

### Difficultés Organisationnelles


- **Mobilisation des troupes** : Nous avons rencontré plusieurs difficultés dues à un manque de motivation au sein de l'équipe. Un membre n’a rien fait et son manque d’implication a nécessité de répéter constamment les demandes pour avancer. Malgré son inaction, nous avons réussi à répartir les tâches entre nous et à terminer le projet dans les délais.

- **Répartition des Tâches** : La répartition initiale des tâches n'était pas optimale, mais nous avons ajusté en cours de projet pour mieux équilibrer la charge de travail.

### Difficultés Techniques

- **Intégration du Mode Multijoueur en Ligne** : La gestion des connexions et des synchronisations a été complexe. Nous avons surmonté cette difficulté en utilisant des bibliothèques de réseau robustes et en effectuant des tests approfondis.

- **Interface et interactions plus user friendly** : Nous avons amélioré l'interface pour une approche plus intuitive. Les commandes de base ont été rendues plus évidentes, et l’affichage des informations importantes a été mieux structuré pour faciliter la prise en main.

- **Conception d'algorithmes sophistiqués pour les bots** : La principale difficulté résidait dans la conception d’algorithmes de plus en plus sophistiqués, indispensables pour rendre les bots performants. Ce n'était pas le code qui posait problème, mais l'élaboration de leur logique, qui nécessitait une grande réflexion pour s’adapter à divers scénarios. Après plusieurs ajustements et itérations, nous avons réussi à surmonter cet obstacle et à concevoir des bots fiables et fonctionnels.

### Points Positifs

- **Collaboration** : La collaboration au sein de l'équipe a été excellente, avec une communication ouverte et une entraide constante.
- **Utilisation des Outils** : L'utilisation de GitLab et des IDE a grandement facilité le développement et la gestion du projet.

---

## Apports du Projet

### Apprentissage Technique

- **Développement en Équipe** : Ce projet nous a appris à travailler efficacement en équipe, à utiliser des outils de gestion de version, et à intégrer des fonctionnalités complexes.Nous avons également dû composer avec la contrainte de ne pas pouvoir importer de librairies externes en Python, ce qui a nécessité de concevoir nos propres solutions et de collaborer étroitement pour surmonter ces limitations techniques.
- **Tests et Qualité** : Nous avons acquis une expérience précieuse en écriture de tests unitaires et d'intégration, et en assurance qualité. Ces tests nous ont permis de détecter et corriger rapidement les erreurs, garantissant une stabilité accrue du projet. De plus, nous avons mis en place des scénarios de test rigoureux pour simuler des cas d’utilisation variés et nous assurer que chaque fonctionnalité répondait aux attentes. Cette démarche a également renforcé notre méthodologie, en nous incitant à adopter une approche plus structurée et systématique dans le développement.

### Apprentissage Organisationnel

- **Gestion de Projet** : Nous avons appris à planifier, répartir les tâches, et ajuster nos stratégies en fonction des défis rencontrés. Cette expérience nous a également permis de mieux anticiper les imprévus, de prioriser les tâches critiques, et de respecter les délais imposés.
- **Communication** : L'importance de la communication claire et régulière a été renforcée tout au long du projet. Pour faciliter les échanges, nous avons également créé un serveur Discord dédié, qui nous a permis de centraliser les discussions, de partager rapidement des informations, et de coordonner efficacement nos efforts. Cet espace collaboratif s'est révélé essentiel pour maintenir une bonne organisation et résoudre les problèmes en temps réel.

### Apports Personnels

Henrique Franco de Oliveira :
- Developpement de l'aspect multijoueur conception de la logique du client et du serveur
- Correction des bugs dans le code
- Développement des base du jeu (collaboration)
- Developpement des tests unitaires (collaborations)
- Aide dans l'interface IHM dans le CLI, resolution des bugs (collaboration)

Gabriel Freiss :
- Creation du mode spectateur 
- Developpement et correction du code des bots Medium (collaboration) et Hard
- Création du tutoriel textuel

Anselme Garnier (capitaine) :
- Organisation de la mise en oeuvre du projet
- Developpement de la base du jeu (logique de placement des pieces, implementation des pieces et règles associées) (collaboration)
- Developpement de l'interface IHM dans le CLI, design
- Developpement du mode de sauvegarde du jeu
- Mise en oeuvre des tests unitaires (collaboration)
- Correction des bugs
- Creation des bots medium et easy (collaboration)

---

## Conclusion

En conclusion, ce projet Blokus a été une expérience enrichissante qui nous a permis de développer des compétences techniques et organisationnelles. Nous sommes fiers des fonctionnalités que nous avons implémentées et des défis que nous avons surmontés. Nous espérons que ce rapport reflète fidèlement notre travail et nos apprentissages.


---

Merci d'avoir lu ce rapport. Bon jeu !
