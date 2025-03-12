from typing import List, Set
from .piece import Piece, PIECE_DEFINITIONS


class Player:
    """
        Génère toutes les orientations possibles de la pièce.
        
        Returns:
            List[Piece]: Liste de toutes les variations de la pièce.
        """
    def __init__(self, color: int):
        """
        Génère toutes les orientations possibles de la pièce.
        
        Returns:
            List[Piece]: Liste de toutes les variations de la pièce.
        """
        self.color = color
        self.pieces = self._initialize_pieces()
        self.remaining_pieces = set(range(len(self.pieces)))

    def _initialize_pieces(self) -> List[Piece]:
        """
        Initialise les pièces disponibles pour le joueur.
        
        Returns:
            List[Piece]: La liste des pièces disponibles.
        """
        return [Piece(shape, i) for i, shape in enumerate(PIECE_DEFINITIONS)]
    
    def get_remaining_pieces(self) -> List[Piece]:
        """
        Retourne la liste des pièces restantes.
        
        Returns:
            List[Piece]: La liste des pièces restantes.
        """
        return [self.pieces[piece_id] for piece_id in self.remaining_pieces]