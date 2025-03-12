from typing import List

PIECE_DEFINITIONS = [
    [[1]],  # 1 square (monomino)
    [[1, 1]],  # 2 squares (domino)
    [[1, 1, 1]],  # 3 straight (tromino)
    [[1, 1], [1, 0]],  # 3 L (tromino)
    [[1, 1, 1, 1]],  # 4 straight (tetromino)
    [[1, 1], [1, 1]],  # 4 square (tetromino)
    [[1, 1, 1], [1, 0, 0]],  # 4 L (tetromino)
    [[1, 1, 0], [0, 1, 1]],  # 4 Z (tetromino)
    [[1, 1, 1], [0, 1, 0]],  # 4 T (tetromino)
    [[1, 1, 1, 1, 1]],  # 5 straight (pentomino)
    [[1, 1, 1, 1], [1, 0, 0, 0]],  # 5 L (pentomino)
    [[0, 1, 1, 1], [1, 1, 0, 0]],  # 5 P (pentomino)
    [[1, 1, 1], [0, 1, 0], [0, 1, 0]],  # 5 T (pentomino)
    [[1, 1, 0], [0, 1, 0], [0, 1, 1]],  # 5 Z (pentomino)
    [[1, 1, 1], [0, 1, 1]],  # 5 W (pentomino)
    [[1, 1, 0], [0, 1, 1], [0, 0, 1]],  # 5 Z (pentomino)
    [[1, 1, 1], [1, 0, 0], [1, 0, 0]],  # 5 L (pentomino)
    [[1, 1], [0, 1], [1, 1]],  # 5 U (pentomino)
    [[1, 0], [1, 1], [1, 0], [1, 0]],  # 5 N (pentomino)
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],  # 5 + (pentomino)
    [[0, 1, 1], [1, 1, 0], [0, 1, 0]]  # 5 Y (pentomino)
]

class Piece:
    """
    Représente une pièce du jeu Blokus.
    
    Attributs:
        shape (List[List[int]]): La forme de la pièce représentée par une matrice de 0 et 1.
        piece_id (int): L'identifiant unique de la pièce.
        height (int): La hauteur de la pièce.
        width (int): La largeur de la pièce.
    """
    def __init__(self, shape: List[List[int]], piece_id: int):
        """
        Initialise une nouvelle pièce.
        
        Args:
            shape (List[List[int]]): La forme de la pièce représentée par une matrice de 0 et 1.
            piece_id (int): L'identifiant unique de la pièce.
        """
        self.shape = shape
        self.piece_id = piece_id
        self.height = len(shape)
        self.width = len(shape[0])

    def rotate(self) -> 'Piece':
        """
        Fait pivoter la pièce de 90 degrés dans le sens des aiguilles d'une montre.
        
        Returns:
            Piece: La pièce pivotée.
        """
        rotated = list(zip(*self.shape[::-1]))
        return Piece([list(row) for row in rotated], self.piece_id)

    def flip(self) -> 'Piece':
        """
        Retourne la pièce horizontalement.
        
        Returns:
            Piece: La pièce retournée.
        """
        flipped = [row[::-1] for row in self.shape]
        return Piece(flipped, self.piece_id)

    def get_all_variations(self) -> List['Piece']:
        """
        Génère toutes les orientations possibles de la pièce.
        
        Returns:
            List[Piece]: Liste de toutes les variations de la pièce.
        """
        variations = []
        current = self
        # Get all rotations
        for _ in range(4):
            variations.append(current)
            current = current.rotate()
        # Get all flipped rotations
        flipped = self.flip()
        current = flipped
        for _ in range(4):
            variations.append(current)
            current = current.rotate()
        return variations