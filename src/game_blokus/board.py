from typing import List, Tuple
from .piece import Piece


COLORS = {
    0: "\033[0m",    # Reset
    1: "\033[94m",   # Blue
    2: "\033[91m",   # Red
    3: "\033[92m",   # Green
    4: "\033[93m"    # Yellow
}

class Board:
    """
    Représente le plateau de jeu de Blokus.
    
    Attributs:
        size (int): La taille du plateau de jeu.
        grid (List[List[int]]): La grille représentant l'état actuel du plateau.
        corners (dict): Les coins disponibles pour chaque joueur.
        board_corners (set): Les coins initiaux du plateau.
        _adjacent_cache (dict): Cache pour les positions adjacentes valides.
    """

    def __init__(self, size: int = 20):
        """
        Initialise un nouveau plateau de jeu.
        
        Args:
            size (int): La taille du plateau de jeu. Par défaut, 20.
        """
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        # Initialize available corners for each player
        self.corners = {1: set(), 2: set(), 3: set(), 4: set()}
        # Initialize board corners as starting points
        self.board_corners = {(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)}
        # Cache for valid adjacent positions
        self._adjacent_cache = {}

    def _update_corners_after_move(self, piece: Piece, x: int, y: int, color: int) -> None:
        """
        Met à jour les coins disponibles après le placement d'une pièce.
        
        Args:
            piece (Piece): La pièce placée.
            x (int): La coordonnée x de la position de placement.
            y (int): La coordonnée y de la position de placement.
            color (int): La couleur du joueur.
        """
        # Remove used board corners
        for i in range(piece.height):
            for j in range(piece.width):
                if piece.shape[i][j] == 1:
                    pos = (x + i, y + j)
                    if pos in self.board_corners:
                        self.board_corners.remove(pos)
        
        # Add new corners
        new_corners = set()
        for i in range(piece.height):
            for j in range(piece.width):
                if piece.shape[i][j] == 1:
                    # Check diagonal positions
                    for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                        new_x, new_y = x + i + dx, y + j + dy
                        if (0 <= new_x < self.size and 
                            0 <= new_y < self.size and 
                            self.grid[new_x][new_y] == 0):
                            new_corners.add((new_x, new_y))
        
        # Update corners for the current player
        self.corners[color].update(new_corners)

    def _get_valid_adjacent(self, x: int, y: int) -> list:
        """
        Obtient les positions adjacentes valides (mise en cache).
        
        Args:
            x (int): La coordonnée x de la position.
            y (int): La coordonnée y de la position.
        
        Returns:
            list: Liste des positions adjacentes valides.
        """
        key = (x, y)
        if key not in self._adjacent_cache:
            self._adjacent_cache[key] = [
                (x + dx, y + dy)
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
                if 0 <= x + dx < self.size and 0 <= y + dy < self.size
            ]
        return self._adjacent_cache[key]

    

    def preview_move(self, piece: Piece, x: int, y: int, color: int) -> List[List[int]]:
        """
        Génère un aperçu du plateau avec la pièce placée.
        
        Args:
            piece (Piece): La pièce à placer.
            x (int): La coordonnée x de la position de placement.
            y (int): La coordonnée y de la position de placement.
            color (int): La couleur du joueur.
        
        Returns:
            List[List[int]]: Aperçu du plateau avec la pièce placée.
        """
        preview = [row[:] for row in self.grid]
        if self.is_valid_move(piece, x, y, color):
            for i in range(piece.height):
                for j in range(piece.width):
                    if piece.shape[i][j] == 1:
                        preview[x + i][y + j] = color
        return preview

    #modification de la logique pour le premier coup
    def is_valid_move(self, piece: Piece, x: int, y: int, color: int) -> bool:
        """
        Vérifie si le placement d'une pièce à (x, y) est valide.
        
        Args:
            piece (Piece): La pièce à placer.
            x (int): La coordonnée x de la position de placement.
            y (int): La coordonnée y de la position de placement.
            color (int): La couleur du joueur.
        
        Returns:
            bool: True si le placement est valide, sinon False.
        """
        # Quick bounds check
        if (x < 0 or y < 0 or 
            x + piece.height > self.size or 
            y + piece.width > self.size):
            return False
        
        has_valid_corner = False
        diagonal_positions = {(-1, -1), (-1, 1), (1, -1), (1, 1)}
        
        for i in range(piece.height):
            for j in range(piece.width):
                if piece.shape[i][j] == 1:
                    pos = (x + i, y + j)
                    
                    # Vérifier si la case est occupée
                    if self.grid[pos[0]][pos[1]] != 0:
                        return False
                    
                    # Vérifier l'adjacence avec la même couleur
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        adj_x, adj_y = pos[0] + dx, pos[1] + dy
                        if (0 <= adj_x < self.size and 
                            0 <= adj_y < self.size and 
                            self.grid[adj_x][adj_y] == color):
                            return False
                    
                    # Vérifier les connexions en coin
                    for dx, dy in diagonal_positions:
                        corner_x, corner_y = pos[0] + dx, pos[1] + dy
                        if (0 <= corner_x < self.size and 
                            0 <= corner_y < self.size and 
                            self.grid[corner_x][corner_y] == color):
                            has_valid_corner = True
        
        # Pour le premier coup, vérifier si on touche un coin du plateau
        if not self.corners[color]:
            for i in range(piece.height):
                for j in range(piece.width):
                    if piece.shape[i][j] == 1:
                        if (x + i, y + j) in self.board_corners:
                            return True
        
        return has_valid_corner
    
    

    def place_piece(self, piece: Piece, x: int, y: int, color: int) -> None:
        """
        Place une pièce et met à jour les coins disponibles.
        
        Args:
            piece (Piece): La pièce à placer.
            x (int): La coordonnée x de la position de placement.
            y (int): La coordonnée y de la position de placement.
            color (int): La couleur du joueur.
        """
        # Place the piece
        for i in range(piece.height):
            for j in range(piece.width):
                if piece.shape[i][j] == 1:
                    self.grid[x + i][y + j] = color
        
        # Update corners
        self._update_corners_after_move(piece, x, y, color)

    def find_valid_moves(self, piece: Piece, color: int) -> List[Tuple[int, int]]:
        """
        Trouve les positions valides pour placer une pièce.
        
        Args:
            piece (Piece): La pièce à placer.
            color (int): La couleur du joueur.
        
        Returns:
            List[Tuple[int, int]]: Liste des positions valides.
        """
        valid_positions = []
        
        # If first move, only check board corners
        if not self.corners[color]:
            for corner_x, corner_y in self.board_corners:
                for dx in range(-piece.height + 1, 1):
                    for dy in range(-piece.width + 1, 1):
                        if self.is_valid_move(piece, corner_x + dx, corner_y + dy, color):
                            valid_positions.append((corner_x + dx, corner_y + dy))
            return valid_positions
        
        # Otherwise, check positions around existing corners
        checked_positions = set()
        for corner_x, corner_y in self.corners[color]:
            for dx in range(-piece.height + 1, 2):
                for dy in range(-piece.width + 1, 2):
                    pos = (corner_x + dx, corner_y + dy)
                    if pos not in checked_positions:
                        checked_positions.add(pos)
                        if self.is_valid_move(piece, pos[0], pos[1], color):
                            valid_positions.append(pos)
        
        return valid_positions
    
    def can_place_piece(self, piece: Piece, color: int) -> bool:
        """
        Vérifie s'il existe une position valide pour placer la pièce.
        
        Args:
            piece (Piece): La pièce à placer.
            color (int): La couleur du joueur.
        
        Returns:
            bool: True s'il existe une position valide, sinon False.
        """
        return bool(self.find_valid_moves(piece, color))

    def display(self, preview_grid: List[List[int]] = None) -> None:
        """
        Affiche l'état actuel du plateau avec des visuels améliorés.
        
        Args:
            preview_grid (List[List[int]], optional): Grille d'aperçu avec la pièce placée. Par défaut, None.
        """
        # Caractères Unicode pour les bordures
        BORDER = {
            'top_left': '╔', 'top_right': '╗', 'bottom_left': '╚', 'bottom_right': '╝',
            'horizontal': '═', 'vertical': '║', 'cross': '╬',
            'top_cross': '╦', 'bottom_cross': '╩', 'left_cross': '╠', 'right_cross': '╣'
        }
        
        # Caractères pour les pièces
        PIECES = {
            0: '·',  # Case vide
            1: '🟦',  # Joueur 1 (Bleu)
            2: '🟥',  # Joueur 2 (Rouge)
            3: '🟩',  # Joueur 3 (Vert)
            4: '🟧'   # Joueur 4 (Jaune)
        }
        
        # Afficher les numéros de colonnes
        print("\n    ", end="")
        for j in range(self.size):
            print(f"{j:2}", end=" ")
        print("\n")
        
        # Afficher la bordure supérieure
        print("   " + BORDER['top_left'] + BORDER['horizontal'] * (self.size * 3) + BORDER['top_right'])
        
        # Afficher le contenu du plateau
        for i in range(self.size):
            # Numéro de ligne
            print(f"{i:2} ", end="")
            print(BORDER['vertical'], end="")
            
            for j in range(self.size):
                grid = preview_grid if preview_grid else self.grid
                cell = grid[i][j]
                
                if cell == 0:
                    print(f" {PIECES[cell]} ", end="")
                else:
                    print(f"{COLORS[cell]}{PIECES[cell]}{COLORS[0]} ", end="")
            print(BORDER['vertical'])
        
        # Afficher la bordure inférieure
        print("   " + BORDER['bottom_left'] + BORDER['horizontal'] * (self.size * 3) + BORDER['bottom_right'])
        
        # Afficher la légende
        print("\nLégende:")
        for color in range(1, 5):
            print(f"{COLORS[color]}Joueur {color}{COLORS[0]}", end="  ")
        print("\n")