from typing import List, Set, Tuple
from dataclasses import dataclass


@dataclass
class GameState:
    """Class for serializing game state"""
    board_state: List[List[int]]
    current_player: int
    player_pieces: List[Set[int]]
    player_corners: List[Set[Tuple[int, int]]]