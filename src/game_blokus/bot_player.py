import random
from typing import List
from .piece import Piece, PIECE_DEFINITIONS

class BotPlayer:
    """
    Représente un joueur bot dans le jeu Blokus.
    
    Attributs:
        level (str): Le niveau de difficulté du bot ('easy', 'medium', 'hard').
        color (int): La couleur du joueur bot.
        pieces (List[Piece]): La liste des pièces disponibles pour le bot.
        remaining_pieces (set): L'ensemble des indices des pièces restantes.
    """
    def __init__(self, level, color):
        """
        Initialise un nouveau joueur bot.
        
        Args:
            level (str): Le niveau de difficulté du bot ('easy', 'medium', 'hard').
            color (int): La couleur du joueur bot.
        """
        self.level = level
        self.color = color
        self.pieces = self._initialize_pieces()
        self.remaining_pieces = set(range(len(self.pieces)))

    def _initialize_pieces(self) -> List[Piece]:
        """
        Initialise les pièces disponibles pour le bot.
        
        Returns:
            List[Piece]: La liste des pièces disponibles.
        """
        return [Piece(shape, i) for i, shape in enumerate(PIECE_DEFINITIONS)]

    def play(self, board):
        """
        Joue un tour en fonction du niveau de difficulté du bot.
        
        Args:
            board (Board): Le plateau de jeu.
        """
        if self.level == "easy":
            self._play_random_move(board)
        elif self.level == "medium":
            self._play_medium_move(board)
        elif self.level == "hard":
            self._play_hard_move(board)
        else:
            raise ValueError("Invalid level specified")

    def _play_random_move(self, board):
        """
        Stratégie de jeu aléatoire améliorée qui évalue tous les mouvements possibles avant de choisir.
        
        Args:
            board (Board): Le plateau de jeu.
        
        Returns:
            bool: True si un mouvement a été effectué, sinon False.
        """
        pieces = list(self.get_remaining_pieces())
        if not pieces:
            return False
        
        # Collect all possible moves
        all_possible_moves = []
        for piece in pieces:
            for variant in self._get_all_variations(piece):
                moves = board.find_valid_moves(variant, self.color)
                for x, y in moves:
                    all_possible_moves.append((piece, variant, x, y))
        
        if all_possible_moves:
            # Choose a random move from all possibilities
            chosen_piece, chosen_variant, x, y = random.choice(all_possible_moves)
            print(f"Placing piece {chosen_piece.piece_id} at ({y}, {x})")
            self._make_move(board, chosen_variant, (x, y))
            return True
        
        print("No available moves")
        return False

    def _make_move(self, board, piece, move):
        """
        Effectue un mouvement en plaçant une pièce sur le plateau.
        
        Args:
            board (Board): Le plateau de jeu.
            piece (Piece): La pièce à placer.
            move (Tuple[int, int]): La position (x, y) où placer la pièce.
        """
        x, y = move
        board.place_piece(piece, x, y, self.color)
        self.remaining_pieces.remove(piece.piece_id)

    def _get_all_variations(self, piece):
        """
        Génère toutes les rotations et inversions d'une pièce.
        
        Args:
            piece (Piece): La pièce à varier.
        
        Returns:
            List[Piece]: Liste de toutes les variations de la pièce.
        """
        variations = []
        for _ in range(4):
            piece = piece.rotate()
            variations.append(piece)
            variations.append(piece.flip())
        return variations

    def get_pieces(self):
        """
        Retourne la liste de toutes les pièces.
        
        Returns:
            List[Piece]: La liste de toutes les pièces.
        """
        return self.pieces

    def get_remaining_pieces(self):
        """
        Retourne la liste des pièces restantes.
        
        Returns:
            List[Piece]: La liste des pièces restantes.
        """
        return [self.pieces[piece_id] for piece_id in self.remaining_pieces]
    
    def _play_medium_move(self, board):
        """
        Stratégie de niveau moyen pour le bot :
        1. Prioriser les plus grandes pièces en début de partie.
        2. Essayer de rester proche du centre du plateau.
        3. Contrôle de territoire de base.
        
        Args:
            board (Board): Le plateau de jeu.
        
        Returns:
            bool: True si un mouvement a été effectué, sinon False.
        """
        pieces = sorted(self.get_remaining_pieces(), 
                    key=lambda p: sum(sum(row) for row in p.shape), 
                    reverse=True)  # Sort by piece size
        
        best_move = None
        best_score = float('-inf')
        
        # Calculate board center
        center_x = board.size // 2
        center_y = board.size // 2
        
        for piece in pieces:
            for variant in self._get_all_variations(piece):
                moves = board.find_valid_moves(variant, self.color)
                for move in moves:
                    x, y = move
                    score = self._evaluate_move(board, variant, x, y, center_x, center_y, 
                                                CENTER_WEIGHT=1.0, SIZE_WEIGHT=0.5, TERRITORY_WEIGHT=1.0)
                    if score > best_score:
                        best_score = score
                        best_move = (variant, x, y)
        
        if best_move:
            piece, x, y = best_move
            print(f"Placing piece {piece.piece_id} at ({y}, {x})")
            self._make_move(board, piece, (x, y))
            return True
        return False

    def _play_hard_move(self, board):
        """
        Stratégie de niveau difficile pour le bot :
        1. Prioriser les plus grandes pièces en début de partie.
        2. Essayer de rester proche du centre du plateau.
        3. Contrôle de territoire avancé et blocage de l'adversaire.
        
        Args:
            board (Board): Le plateau de jeu.
        
        Returns:
            bool: True si un mouvement a été effectué, sinon False.
        """
        pieces = sorted(self.get_remaining_pieces(), 
                    key=lambda p: sum(sum(row) for row in p.shape), 
                    reverse=True)  # Sort by piece size
        
        best_move = None
        best_score = float('-inf')
        
        # Calculate board center
        center_x = board.size // 2
        center_y = board.size // 2
        
        for piece in pieces:
            for variant in self._get_all_variations(piece):
                moves = board.find_valid_moves(variant, self.color)
                for move in moves:
                    x, y = move
                    score = self._evaluate_move(board, variant, x, y, center_x, center_y, 
                                                CENTER_WEIGHT=2.0, SIZE_WEIGHT=1.5, TERRITORY_WEIGHT=2.0)
                    if score > best_score:
                        best_score = score
                        best_move = (variant, x, y)
        
        if best_move:
            piece, x, y = best_move
            print(f"Placing piece {piece.piece_id} at ({y}, {x})")
            self._make_move(board, piece, (x, y))
            return True
        return False

    def _evaluate_move(self, board, piece, x, y, center_x, center_y, 
                    CENTER_WEIGHT=2.0, SIZE_WEIGHT=1.0, TERRITORY_WEIGHT=1.5):
        """
        Évalue un mouvement potentiel basé sur plusieurs facteurs.
        
        Args:
            board (Board): Le plateau de jeu.
            piece (Piece): La pièce à placer.
            x (int): La coordonnée x de la position de placement.
            y (int): La coordonnée y de la position de placement.
            center_x (int): La coordonnée x du centre du plateau.
            center_y (int): La coordonnée y du centre du plateau.
            CENTER_WEIGHT (float): Poids du facteur de distance au centre.
            SIZE_WEIGHT (float): Poids du facteur de taille de la pièce.
            TERRITORY_WEIGHT (float): Poids du facteur de contrôle du territoire.
        
        Returns:
            float: Le score du mouvement évalué.
        """
        score = 0
        
        # Factor 1: Piece size
        piece_size = sum(sum(row) for row in piece.shape)
        score += piece_size * SIZE_WEIGHT
        
        # Factor 2: Distance from center (prefer moves closer to center)
        distance_from_center = -((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
        score += distance_from_center * CENTER_WEIGHT
        
        # Factor 3: Territory control (count accessible corners created)
        preview = board.preview_move(piece, x, y, self.color)
        corners_created = 0
        for i in range(max(0, x-1), min(board.size, x+piece.height+1)):
            for j in range(max(0, y-1), min(board.size, y+piece.width+1)):
                if preview[i][j] == 0:  # Empty square
                    # Check if it's a corner of our piece
                    corner_count = 0
                    for dx, dy in [(1,1), (1,-1), (-1,1), (-1,-1)]:
                        new_x, new_y = i + dx, j + dy
                        if (0 <= new_x < board.size and 
                            0 <= new_y < board.size and 
                            preview[new_x][new_y] == self.color):
                            corner_count += 1
                    if corner_count > 0:
                        corners_created += 1
        
        score += corners_created * TERRITORY_WEIGHT
        
        return score