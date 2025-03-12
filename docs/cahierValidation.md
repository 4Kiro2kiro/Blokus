# Cahier de Validation

## **Validation: Affichage de l’État Courant du Plateau**

### **Scénario 1 : Afficher le plateau après un coup**

- **Action :** 
  - Le joueur 1 place une pièce en position (3, 3).
- **Résultat attendu :** 
  - Le plateau s’affiche correctement, montrant la pièce du joueur 1 à la position (3, 3).
- [x] **Vérification utilisateur :** 
  - L’état du plateau est clair et sans erreur.

### **Scénario 2 : Plateau entièrement rempli**
- **Action :** 
  - Les joueurs remplissent le plateau avec toutes leurs pièces.
- **Résultat attendu :** 
  - Le plateau affiche toutes les pièces placées selon les positions prévues.
- [x] **Vérification utilisateur :** 
  - Chaque pièce est visible et identifiable.

### **Scénario 3 : Plateau vide (cas d’erreur)**
- **Action :** 
  - Le joueur demande l’affichage alors qu’aucune pièce n’a été placée.
- **Résultat attendu :** 
  - Un message indique que le plateau est vide.
- [x] **Vérification utilisateur :** 
  - Le message est compréhensible et guide l’utilisateur sur la prochaine étape.

---

## **Validation : Jouer et Contrôler un Coup**

### **Scénario 4 : Placement d’une pièce valide**

- **Action :** 
  - Le joueur 2 place une pièce en position (0, 17).
- **Résultat attendu :** 
  - Confirmation que la pièce est placée, et le plateau est mis à jour.
- [x] **Vérification utilisateur :** 
  - Le feedback est visible immédiatement, et la position est correcte.

### **Scénario 5 : Placement en bordure**

- **Action :** 
  - Le joueur 1 place une pièce en position (0, 0).
- **Résultat attendu :** 
  - La pièce est placée et visible en bordure du plateau.
- [x] **Vérification utilisateur :** 
  - L’état du plateau est cohérent et complet.

### **Scénario 6 : Tentative de placement sur une case occupée (cas d’erreur)**
- **Action :** 
  - Le joueur 1 essaie de placer une pièce sur une case déjà occupée.
- **Résultat attendu :** 
  - Un message d’erreur informe que la case est occupée.
- [x] **Vérification utilisateur :** 
  - Le message est clair et empêche toute action incorrecte.

---

## **Validation : Détection de la Fin de Partie pour un Joueur**

### **Scénario 7 : Fin de partie avec toutes les pièces placées**

- **Action :** 
  - Les joueurs placent toutes leurs pièces sur le plateau, remplissant toutes les cases.
- **Résultat attendu :** 
  - L’application affiche un message indiquant que la partie est terminée et présente le score final.
- [x] **Vérification utilisateur :** 
  - Le message de fin est clair et le score est affiché sans erreur.

### **Scénario 8 : Fin de partie pour un joueur bloqué**

- **Action :** 
  - Un joueur ne peut plus effectuer de coup valide.
- **Résultat attendu :** 
  - L’application détecte que le joueur est bloqué et affiche un message indiquant qu’il ne peut plus jouer.
- [x] **Vérification utilisateur :** 
  - Le message est compréhensible, et l’utilisateur sait que son tour est terminé.

### **Scénario 9 : Erreur de détection de fin de partie (cas d’erreur)**

- **Action :** 
  - Une erreur de détection est simulée pendant la vérification de la fin de partie.
- **Résultat attendu :** 
  - Un message d’erreur invite l’utilisateur à relancer la vérification.
- [x] **Vérification utilisateur :** 
  - Le message est explicite et guide l’utilisateur pour résoudre le problème.

---

## **Validation : Interface Homme-Machine (IHM)**

### **Scénario 10 : Identification correcte des joueurs**

- **Action :** 
  - Une partie commence avec quatre joueurs, chacun jouant à son tour.
- **Résultat attendu :** 
  - L’IHM affiche correctement les noms ou les couleurs des joueurs pendant leurs tours respectifs.
- [x] **Vérification utilisateur :** 
  - Chaque joueur est identifié sans ambiguïté, et les informations affichées sont correctes.

### **Scénario 11 : Pause lors d’une déconnexion réseau**

- **Action :** 
  - Un joueur se déconnecte en cours de partie.
- **Résultat attendu :** 
  - L’application détecte la déconnexion et affiche un message indiquant une pause en attendant la reconnexion.
- [x] **Vérification utilisateur :** 
  - Le message de pause est clair, et l’utilisateur comprend qu’il doit attendre.

### **Scénario 12 : Gestion de l’erreur de communication (cas d’erreur)**

- **Action :** 
  - Une erreur de communication entre les joueurs est simulée.
- **Résultat attendu :** 
  - L’IHM affiche un message d’erreur et donne des instructions pour reprendre la partie.
- [x] **Vérification utilisateur :** 
  - Le message est compréhensible, et l’utilisateur sait comment rétablir la situation.
