import json
from dataclasses import asdict
from .state import GameState

def save_game(game, filename: str = "blokus_save.json") -> None:
    """
    Sauvegarde l'état actuel du jeu.
        
    Args:
        filename (str): Le nom du fichier de sauvegarde. Par défaut, "blokus_save.json".
    """

    state = GameState(
        board_state=game.board.grid,
        current_player=game.current_player,
        player_pieces=[list(p.remaining_pieces) for p in game.players],
        player_corners=[list(game.board.corners[i+1]) for i in range(len(game.players))]
    )
    
    with open(filename, 'w') as f:
        json.dump(asdict(state), f)
    print(f"\nGame saved to {filename}")

def load_game(game, filename: str = "blokus_save.json") -> bool:
    """
    Charge un état de jeu sauvegardé.
    
    Args:
        filename (str): Le nom du fichier de sauvegarde. Par défaut, "blokus_save.json".
    
    Returns:
        bool: True si le jeu a été chargé avec succès, sinon False.
    """

    try:
        with open(filename, 'r') as f:
            state = json.load(f)
        
        game.board.grid = state['board_state']
        game.current_player = state['current_player']
        for i, pieces in enumerate(state['player_pieces']):
            game.players[i].remaining_pieces = set(pieces)
            game.players[i].pieces = {piece_id: game.players[i].pieces[piece_id] for piece_id in pieces}
        for i, corners in enumerate(state['player_corners']):
            game.board.corners[i+1] = set(tuple(c) for c in corners)
        
        print(f"\nGame loaded from {filename}")
        return True
    except FileNotFoundError:
        print(f"\nNo saved game found at {filename}")
        return False
    except KeyError as e:
        print(f"\nError loading game: missing key {e}")
        return False
    except json.JSONDecodeError:
        print(f"\nError loading game: invalid JSON format")
        return False
