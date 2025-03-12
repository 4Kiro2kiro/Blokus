# Cahier de Tests de Validation

## Fonction : Initialisation du Jeu

### Cas Nominal

- [x] **Test 1.1 :** Initialisation du jeu
  - **But du test** : Vérifier que le jeu est correctement initialisé.
  - **Entrée** : Création d'une instance de `BlokusGame` avec 4 joueurs.
  - **Sortie attendue** : Le jeu doit avoir 4 joueurs, le joueur courant doit être le premier, la taille du plateau doit être de 20, le jeu ne doit pas être en ligne et le client réseau doit être `None`.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

---

## Fonction : Initialisation du Plateau

### Cas Nominal

- [x] **Test 2.1 :** Initialisation du plateau
  - **But du test** : Vérifier que le plateau est correctement initialisé.
  - **Entrée** : Création d'une instance de `Board`.
  - **Sortie attendue** : Le plateau doit avoir une taille de 20x20, toutes les cases doivent être initialisées à 0 et il doit y avoir 4 coins disponibles.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

---

## Fonction : Initialisation des Joueurs

### Cas Nominal

- [x] **Test 3.1 :** Initialisation des joueurs
  - **But du test** : Vérifier que les joueurs sont correctement initialisés.
  - **Entrée** : Création d'une instance de `BlokusGame` avec 4 joueurs.
  - **Sortie attendue** : Chaque joueur doit avoir une couleur unique (1 à 4) et 21 pièces restantes.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

---

## Fonction : Sauvegarde et Chargement du Jeu

### Cas Nominal

- [x] **Test 4.1 :** Sauvegarde et chargement du jeu
  - **But du test** : Vérifier que l'état du jeu peut être sauvegardé et chargé correctement.
  - **Entrée** : Sauvegarde de l'état du jeu dans un fichier, puis chargement de ce fichier.
  - **Sortie attendue** : Le fichier de sauvegarde doit exister après la sauvegarde, et l'état du jeu doit être correctement restauré après le chargement.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

### Cas d’Erreur

- [x] **Test 4.2 :** Chargement d'un fichier inexistant
  - **But du test** : Vérifier que le chargement d'un fichier de sauvegarde inexistant échoue correctement.
  - **Entrée** : Tentative de chargement d'un fichier de sauvegarde qui n'existe pas.
  - **Sortie attendue** : Le chargement doit échouer et retourner `False`.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

- [x] **Test 4.3 :** Chargement d'un fichier de format invalide
  - **But du test** : Vérifier que le chargement d'un fichier de sauvegarde avec un format invalide échoue correctement.
  - **Entrée** : Tentative de chargement d'un fichier de sauvegarde contenant des données invalides.
  - **Sortie attendue** : Le chargement doit échouer et retourner `False`.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

---

## Fonction : Placement des Pièces

### Cas Nominal

- [x] **Test 5.1 :** Placement d'une pièce valide
  - **But du test** : Vérifier que le placement d'une pièce est correctement effectué.
  - **Entrée** : Joueur 1 place une pièce en position (0, 0).
  - **Sortie attendue** : La pièce doit être placée sur le plateau et la grille doit être mise à jour avec la couleur du joueur.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

### Cas d’Erreur

- [x] **Test 5.2 :** Placement d'une pièce hors des limites
  - **But du test** : Vérifier que le placement d'une pièce hors des limites du plateau est détecté comme invalide.
  - **Entrée** : Joueur 1 essaie de placer une pièce en position (-1, -1).
  - **Sortie attendue** : Le placement doit être refusé et retourner `False`.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

- [x] **Test 5.3 :** Placement d'une pièce sur une case occupée
  - **But du test** : Vérifier que le placement d'une pièce sur une case déjà occupée est détecté comme invalide.
  - **Entrée** : Joueur 1 essaie de placer une pièce en position (0, 0) où se trouve déjà une pièce.
  - **Sortie attendue** : Le placement doit être refusé et retourner `False`.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

---

## Fonction : Transformation des Pièces

### Cas Nominal

- [x] **Test 6.1 :** Rotation et retournement des pièces
  - **But du test** : Vérifier que les pièces peuvent être correctement tournées et retournées.
  - **Entrée** : Rotation et retournement d'une pièce.
  - **Sortie attendue** : La forme de la pièce doit changer après chaque transformation et revenir à la forme originale après quatre rotations et deux retournements.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

### Cas d’Erreur

- [x] **Test 6.2 :** Rotation d'une pièce invalide
  - **But du test** : Vérifier que la rotation d'une pièce invalide est détectée correctement.
  - **Entrée** : Tentative de rotation d'une pièce avec une forme invalide (par exemple, une pièce vide).
  - **Sortie attendue** : La rotation doit échouer et retourner une erreur ou un message d'erreur.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

---

## Fonction : Détection de la Fin de Partie

### Cas Nominal

- [x] **Test 7.1 :** Détection de la fin de partie
  - **But du test** : Vérifier que la fin de partie est correctement détectée lorsque tous les joueurs ont placé toutes leurs pièces.
  - **Entrée** : Tous les joueurs ont placé toutes leurs pièces.
  - **Sortie attendue** : La partie doit être détectée comme terminée.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

### Cas Particulier

- [x] **Test 7.2 :** Détection de la fin de partie pour un joueur bloqué
  - **But du test** : Vérifier que la fin de partie est correctement détectée pour un joueur qui ne peut plus jouer.
  - **Entrée** : Un joueur n'a plus de coups possibles.
  - **Sortie attendue** : La partie doit être détectée comme terminée pour ce joueur.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

### Cas d’Erreur

- [x] **Test 7.3 :** Erreur de détection de fin de partie
  - **But du test** : Vérifier le comportement de l’application lorsque la détection de fin de partie rencontre un problème.
  - **Entrée** : Erreur de détection (simulée).
  - **Sortie attendue** : Message d’erreur invitant l’utilisateur à relancer la vérification.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

---

## Fonction : Commandes de Jeu

### Cas Nominal

- [x] **Test 8.1 :** Commande pour quitter le jeu
  - **But du test** : Vérifier que la commande pour quitter le jeu fonctionne correctement.
  - **Entrée** : Commande 'q' pour quitter le jeu.
  - **Sortie attendue** : Le jeu doit se terminer.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

### Cas d’Erreur

- [x] **Test 8.2 :** Commande invalide
  - **But du test** : Vérifier que l'application gère correctement une commande invalide.
  - **Entrée** : Commande 'x' (commande invalide).
  - **Sortie attendue** : L'application doit afficher un message d'erreur indiquant que la commande est invalide.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

---

## Fonction : Affichage du Score Final

### Cas Nominal

- [x] **Test 9.1 :** Affichage du score final
  - **But du test** : Vérifier que le score final est correctement affiché à la fin de la partie.
  - **Entrée** : Fin de la partie avec des scores différents pour chaque joueur.
  - **Sortie attendue** : Le score final doit être affiché avec les joueurs classés par ordre décroissant de score.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

### Cas Particulier

- [x] **Test 9.2 :** Affichage du score final sans mouvements
  - **But du test** : Vérifier que le score final est correctement affiché même si aucun mouvement n'a été effectué.
  - **Entrée** : Fin de la partie sans aucun mouvement effectué.
  - **Sortie attendue** : Le score final doit être affiché avec tous les joueurs ayant un score de 0.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

---

## Fonction : Tests Spécifiques aux Bots

### Cas Nominal

- [x] **Test 10.1 :** Jeu aléatoire du bot
  - **But du test** : Vérifier que le bot peut jouer un coup aléatoire.
  - **Entrée** : Le bot joue un coup aléatoire.
  - **Sortie attendue** : Le bot doit jouer un coup valide.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

- [x] **Test 10.2 :** Jeu de niveau moyen du bot
  - **But du test** : Vérifier que le bot peut jouer un coup de niveau moyen.
  - **Entrée** : Le bot joue un coup de niveau moyen.
  - **Sortie attendue** : Le bot doit jouer un coup valide.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

- [x] **Test 10.3 :** Jeu de niveau difficile du bot
  - **But du test** : Vérifier que le bot peut jouer un coup de niveau difficile.
  - **Entrée** : Le bot joue un coup de niveau difficile.
  - **Sortie attendue** : Le bot doit jouer un coup valide.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**


---

## Fonction : Tests Réseau et Serveur

### Cas Nominal

- [x] **Test 11.1 :** Connexion au serveur
  - **But du test** : Vérifier que la connexion au serveur fonctionne correctement.
  - **Entrée** : Connexion au serveur.
  - **Sortie attendue** : La connexion doit être établie sans erreur.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

- [x] **Test 11.2 :** Envoi de message au serveur
  - **But du test** : Vérifier que l'envoi de message au serveur fonctionne correctement.
  - **Entrée** : Envoi d'un message au serveur.
  - **Sortie attendue** : Le message doit être envoyé sans erreur.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

- [x] **Test 11.3 :** Réception de message du serveur
  - **But du test** : Vérifier que la réception de message du serveur fonctionne correctement.
  - **Entrée** : Réception d'un message du serveur.
  - **Sortie attendue** : Le message doit être reçu sans erreur.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

- [x] **Test 11.4 :** Déconnexion du serveur
  - **But du test** : Vérifier que la déconnexion du serveur fonctionne correctement.
  - **Entrée** : Déconnexion du serveur.
  - **Sortie attendue** : La déconnexion doit être effectuée sans erreur et on ne peut plus jouer.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

### Cas d’Erreur

- [x] **Test 11.5 :** Échec de connexion au serveur
  - **But du test** : Vérifier que l'application gère correctement un échec de connexion au serveur.
  - **Entrée** : Tentative de connexion à un serveur inexistant ou indisponible.
  - **Sortie attendue** : L'application doit afficher un message d'erreur indiquant l'échec de la connexion.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**
---

## Fonction : Tests de Spectateur

### Cas Nominal

- [x] **Test 12.1 :** Démarrage du mode spectateur
  - **But du test** : Vérifier que le mode spectateur démarre correctement.
  - **Entrée** : Démarrage du mode spectateur.
  - **Sortie attendue** : Le mode spectateur doit démarrer sans erreur.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

- [x] **Test 12.2 :** Affichage des mouvements en mode spectateur
  - **But du test** : Vérifier que les mouvements des joueurs sont affichés correctement en mode spectateur.
  - **Entrée** : Mouvements des joueurs en mode spectateur.
  - **Sortie attendue** : Les mouvements doivent être affichés correctement.
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**

- [x] **Test 12.3 :** Fin du mode spectateur
  - **But du test** : Vérifier que le mode spectateur se termine correctement.
  - **Entrée** : Fin du mode spectateur.
  - **Sortie attendue** : Le mode spectateur doit se terminer sans erreur. Retourner au menu pricipal
  -----------------
  **Testé sur :**

      Visual Studio Code Version : 1.95.3 (Universal)
      Validation : f1a4fb101478ce6ec82fe9627c43efbf9e98c813
      Date : 2025-01-17T11:01:00.000Z
      Système d’exploitation : Darwin arm64 24.1.0 / macOS Sequoia 15.2
      Python : 3.13.1
  **Résultat :**
    **OK**
    