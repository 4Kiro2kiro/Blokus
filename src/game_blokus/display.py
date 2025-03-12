from .board import Board
from .player import Player
from .piece import Piece

COLORS = {
    0: "\033[0m",    # Reset
    1: "\033[94m",   # Blue
    2: "\033[91m",   # Red
    3: "\033[92m",   # Green
    4: "\033[93m"    # Yellow
}

BORDER_CHARS = {
    'horizontal': '━',
    'vertical': '┃',
    'corner_tl': '┏',
    'corner_tr': '┓',
    'corner_bl': '┗',
    'corner_br': '┛',
    'piece_block': '■',
    'empty_block': '·',
    't_down': '┳',
    't_up': '┻',
    't_right': '┣',
    't_left': '┫',
    'cross': '╋'
}

def display_game_header(player: Player):
    """
    Affiche l'en-tête du jeu avec les informations du joueur.
        
    Args:
        player (Player): Le joueur actuel.
    """

    header_width = 60
    player_text = f"Player's turn {player.color}"
    padding_left = (header_width - len(player_text) - 2) // 2
    padding_right = header_width - len(player_text) - 2 - padding_left

    print("\n" + BORDER_CHARS['horizontal'] * header_width)
    print(f"{COLORS[player.color]}{BORDER_CHARS['vertical']}{' ' * padding_left}"
          f"{player_text}{' ' * padding_right}{BORDER_CHARS['vertical']}{COLORS[0]}")
    print(BORDER_CHARS['horizontal'] * header_width + "\n")

def display_help():
    """Display game help and controls"""
    print("\n🎮 Blokus Help 🎮")
    print("\nGame Rules:")
    print("1. Each piece must be placed corner-to-corner with your existing pieces")
    print("2. Pieces cannot share edges with your other pieces")
    print("3. First piece must touch a corner of the board")
    print("4. Game ends when no players can place more pieces")
    
    print("\nControls:")
    print("- Enter piece number (0-20) to select a piece")
    print("- 's' to save the current game")
    print("- 'l' to load a saved game")
    print("- 'h' to show this help")
    print("- 'q' to quit the game")
    
    print("\nPiece Placement:")
    print("1. Enter row (x) and column (y) coordinates")
    print("2. Choose rotation (0-3) for 90° clockwise turns")
    print("3. Choose whether to flip the piece (y/n)")
    print("4. Confirm the placement after preview")

def display_final_score(game):
    """Display the final score for each player with colored output"""
    print("\n🏆 Game Over! 🏆")
    print("\nFinal Scores:")
    
    scores = []
    for player in game.players:
        # Count remaining squares
        remaining_squares = sum(
            sum(row) for piece_id in player.remaining_pieces 
            for row in game.players[player.color - 1].pieces[piece_id].shape
        )
        # Count placed squares
        placed_squares = sum(row.count(player.color) for row in game.board.grid)
        
        scores.append({
            'color': player.color,
            'remaining': remaining_squares,
            'placed': placed_squares,
            'score': placed_squares - remaining_squares
        })

    # Sort by score in descending order
    scores.sort(key=lambda x: x['score'], reverse=True)

    print("\n" + "═" * 40)
    print("🏆  Final Score  🏆")
    print("═" * 40)

    # Display scores with colors and formatting
    for i, score in enumerate(scores, 1):
        medal = '🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else '  '
        print(f"\n{COLORS[score['color']]}Player {score['color']}:{COLORS[0]}")
        print(f"  {medal} Final Score: {score['score']}")
        print(f"   🟩 Squares placed: +{score['placed']}")
        print(f"   🟥 Remaining squares: -{score['remaining']}")
        print("═" * 40)

def display_piece(piece: Piece, show_id: bool = True, used: bool = False, color: int = None):
    if show_id:
        print(f"\n{COLORS[color if color else 0]}Pièce {piece.piece_id}:{COLORS[0]}")
    
    # Cadre supérieur
    width = len(piece.shape[0]) * 2 + 1
    print(f"{BORDER_CHARS['corner_tl']}{BORDER_CHARS['horizontal'] * width}{BORDER_CHARS['corner_tr']}")
    
    # Contenu de la pièce
    for row in piece.shape:
        print(f"{BORDER_CHARS['vertical']} ", end="")
        for cell in row:
            if cell == 0:
                print(f"{BORDER_CHARS['empty_block']} ", end="")
            else:
                if used:
                    print(f"{COLORS[0]}{BORDER_CHARS['piece_block']}{COLORS[0]} ", end="")
                else:
                    print(f"{COLORS[color if color else 0]}{BORDER_CHARS['piece_block']}{COLORS[0]} ", end="")
        print(f"{BORDER_CHARS['vertical']}")
    
    # Cadre inférieur
    print(f"{BORDER_CHARS['corner_bl']}{BORDER_CHARS['horizontal'] * width}{BORDER_CHARS['corner_br']}")

def display_all_pieces(player: Player):
    """Affiche toutes les pièces pour un joueur, en grisant celles qui ont été utilisées"""
    print(f"\nPièces pour le Joueur {player.color}:")
    for piece_id, piece in player.pieces.items():
        if piece_id in player.remaining_pieces:
            display_piece(piece, show_id=True)
        else:
            display_piece(piece, show_id=True, used=True)
        print()
