from typing import List, Tuple, Optional
from .board import Board
from .piece import Piece
from .bot_player import BotPlayer
from .spectactor import start_spectator
from .player import Player
from .state import GameState
from .display import (
    display_game_header, display_help, display_final_score, 
    display_piece, display_all_pieces, COLORS, BORDER_CHARS
)
from .tutorial import start_tutorial
from .save_load import save_game, load_game
from .utils import clear_screen
from .network_client import BlokusClient

class BlokusGame:
    def __init__(self, num_players: int = 4, ai_levels: List[str] = None):
        """
        Initialise une nouvelle partie de Blokus.
        
        Args:
            num_players (int): Le nombre de joueurs. Par défaut, 4.
            ai_levels (List[str]): Les niveaux de difficulté des bots. Par défaut, None.
        """

        self.network_client = None
        self.is_online = False
        self.player_number = None  # For online games: player's assigned number (0 to 3)
        self.current_player = 0  # For online games: tracks whose turn it is
        self.total_players = num_players  # Total number of players in the game
        self._initialize_game(num_players, ai_levels)

    def _initialize_game(self, num_players: int = 4, ai_levels: List[str] = None) -> None:
        """
        Initialize or reset the game state with the given parameters.
        
        Args:
            num_players (int): Number of players for the game.
            ai_levels (List[str]): List of AI levels for bot players
        """
        self.board = Board()
        self.players = []
        self.current_player = 0
        ai_levels = ai_levels or []
        for i in range(num_players):
            color = i + 1 # Assign a unique color to each player
            if i < len(ai_levels):
                self.players.append(BotPlayer(ai_levels[i], color))
            else:
                self.players.append(Player(color))

    def reset_game(self, num_players: int = None, ai_levels: List[str] = None) -> None:
        """
        Reset the game state for a new game.
        
        Args:
            num_players (int): Number of players for the game.
            ai_levels (List[str]): List of AI levels for bot players
        Returns:
            None
        """
        if num_players is None:
            num_players = len(self.players)
        self._initialize_game(num_players, ai_levels)

    def start_game(self) -> None:
        """
        Start a new game with initial setup
        
        Returns:
            None
        """
        print("\n🎮 Welcome to Blokus! 🎮")
        mode = self._get_game_mode()

        if mode == '1':
            self._setup_solo_game()
        elif mode == '2':
            self._setup_local_multiplayer()
        elif mode == '3':
            self._setup_online_multiplayer()
        elif mode == '4':
            start_tutorial(self)
        elif mode == '5':
            start_spectator(self)

        if mode != '5':
            print("\nGame starting!")
            display_help()
            self.play()

    def _get_game_mode(self) -> str:
        """
        Get the game mode selection from the user
        
        Returns:
            str: The selected game mode
        """
        while True:
            mode = input("Choose game mode:\n1. Solo against AI\n2. Local Multiplayer\n3. Online Multiplayer\n4. Tutorial\n5. Spectator mode\nEnter choice (1/2/3/4/5): ")
            if mode in ['1', '2', '3', '4', '5']:
                return mode
            print("Invalid choice. Please enter 1, 2, 3, 4 or 5.")

    def _setup_solo_game(self) -> None:
        """
        Setup a solo game against AI
        
        Returns:
            None
        """
        valid_levels = ["easy", "medium", "hard"]
        ai_level = ""
        while ai_level not in valid_levels:
            ai_level = input("Choose AI level (easy/medium/hard): ").lower()
            if ai_level not in valid_levels:
                print("Invalid choice. Please choose either 'easy', 'medium', or 'hard'.")
        self.reset_game(num_players=2, ai_levels=[ai_level])

    def _setup_local_multiplayer(self) -> None:
        """
        Setup a local multiplayer game
        
        Returns:
            None
        """
        while True:
            try:
                num_players = int(input("\nEnter number of players (2-4): "))
                if 2 <= num_players <= 4:
                    self.reset_game(num_players)
                    break
                print("Please enter a number between 2 and 4.")
            except ValueError:
                print("Invalid input! Please enter a number.")

    def _setup_online_multiplayer(self) -> None:
        """
        Setup an online multiplayer game

        Returns:
            None
        """
        game_type = self._get_online_game_type()
        
        if game_type == '1':
            self._create_online_game()
        else:
            self._join_online_game()

    def _get_online_game_type(self) -> str:
        """Get the online game type selection from the user
        
        Returns:
            str: The selected game type
        """
        while True:
            try:
                game_type = input("\nDo you want to:\n1. Create a new game\n2. Join an existing game\nEnter choice (1/2): ")
                if game_type in ['1', '2']:
                    return game_type
                print("Please enter 1 or 2.")
            except ValueError:
                print("Invalid input! Please enter a number.")

    def _create_online_game(self) -> None:
        """
        Create a new online game
        Returns:
            None"""
        num_players = self._get_online_player_count()
        self.setup_online_game(num_players)
        if self.network_client and self.network_client.game_id:
            print(f"\nGame created! Share this game ID with the other players: {self.network_client.game_id}")
            input("Press Enter to continue...")

    def _join_online_game(self) -> None:
        """
        Join an existing online game
        
        Returns:
            None
        """
        game_id = input("\nEnter the game ID to join: ").strip()
        self.setup_online_game(None, game_id)

    def _get_online_player_count(self) -> int:
        """Get the number of players for an online game
        
        Returns:
            int: Number of players for the game
        """
        while True:
            try:
                num_players = int(input("\nEnter number of players (2-4): "))
                if 2 <= num_players <= 4:
                    return num_players
                print("Please enter a number between 2 and 4.")
            except ValueError:
                print("Invalid input! Please enter a number.")

    def play(self) -> None:
        """Main game loop with network support
        
        Returns:
            None
        """
        game_over = False
        while not game_over:
            self._display_current_game_state()
            player = self.players[self.current_player]

            # Handle special states but don't skip game over check
            if self._handle_special_player_states(player):
                game_over = self._check_game_over()
                if not game_over:
                    continue

            # Display available pieces and commands
            self._display_player_interface(player)
            
            # Handle player command
            if self._handle_player_command(player):
                game_over = self._check_game_over()
                if not game_over:
                    continue
            
            # Check game end conditions
            game_over = self._check_game_over()
            
            # Autosave if needed
            self._handle_autosave(game_over)
        
        self._handle_game_over_sequence()

    def _display_current_game_state(self):
        """Display the current state of the game board

        Returns:
            None
        """
        clear_screen()
        self.board.display()
        display_game_header(self.players[self.current_player])

    def _handle_special_player_states(self, player: Player) -> bool:
        """Handle bot players, players with no pieces, and online waiting states
        
        Returns:
            bool: True if a special state was handled, False otherwise
        """
        if isinstance(player, BotPlayer):
            print(f"\n{COLORS[player.color]}AI is thinking...{COLORS[0]}")
            player.play(self.board)
            self.current_player = (self.current_player + 1) % len(self.players)
            input("\nPress Enter to continue...")
            return True
        
        if not player.remaining_pieces:
            print(f"{COLORS[player.color]}No pieces left!{COLORS[0]}")
            self.current_player = (self.current_player + 1) % len(self.players)
            input("\nPress Enter to continue...")
            return True

        if self.is_online and self.player_number != self.current_player:
            print(f"\n{COLORS[player.color]}Waiting for other player's move...{COLORS[0]}")
            input("\nPress Enter to refresh...")
            return True
        
        return False

    def _display_player_interface(self, player: Player):
        """
        Display available pieces and command menu
        
        Args:
            player (Player): The current player"""
        remaining_pieces = [player.pieces[pid] for pid in sorted(player.remaining_pieces)]
        print("\nAvailable pieces:")
        piece_grid = self._create_piece_grid(remaining_pieces, player.color)
        for line in piece_grid:
            print(line)

        self._display_command_menu()

    def _display_command_menu(self):
        """Display the command menu in a frame
        
        Returns:
            None
        """
        print("\n" + BORDER_CHARS['horizontal'] * 40)
        print(f"{BORDER_CHARS['vertical']} Available commands:".ljust(39) + BORDER_CHARS['vertical'])
        print(f"{BORDER_CHARS['vertical']} • Piece number to place it".ljust(39) + BORDER_CHARS['vertical'])
        print(f"{BORDER_CHARS['vertical']} • 's' to save".ljust(39) + BORDER_CHARS['vertical'])
        print(f"{BORDER_CHARS['vertical']} • 'l' to load".ljust(39) + BORDER_CHARS['vertical'])
        print(f"{BORDER_CHARS['vertical']} • 'q' to quit".ljust(39) + BORDER_CHARS['vertical'])
        print(BORDER_CHARS['horizontal'] * 40)

    def _handle_player_command(self, player: Player) -> bool:
        """
        Handle player command input and piece placement

        Args:
            player (Player): The current player
        
        """
        command = input(f"\n{COLORS[player.color]}Your choice >{COLORS[0]} ").lower()
        
        if self._handle_game_commands(command):
            return True

        try:
            return self._handle_piece_placement(player, int(command))
        except ValueError as e:
            print(f"Invalid input! {e}")
            input("Press Enter to continue...")
        except Exception as e:
            print(f"An error occurred: {e}")
            input("Press Enter to continue...")
        
        return False

    def _handle_game_commands(self, command: str) -> bool:
        """Handle non-piece commands like save, load, quit
        
        Args:
            command (str): The command entered by the player
        Returns:
            bool: True if a game command was handled, False otherwise

        """
        if command == 's':
            save_game(self)
            return True
        elif command == 'l':
            load_game(self)
            return True
        elif command == 'q':
            if input("Are you sure you want to quit? (y/n): ").lower() == 'y':
                print("\nThanks for playing!")
                self.game_over = True
                return True
        return False

    def _handle_piece_placement(self, player: Player, piece_id: int) -> bool:
        """Handle the piece placement workflow
        
        Args:
            player (Player): The current player
            piece_id (int): The ID of the piece to place
            
        Returns:
            bool: True if the piece placement was handled, False otherwise
        """
        if piece_id not in player.remaining_pieces:
            print("Invalid piece selection!")
            input("Press Enter to continue...")
            return True

        piece = player.pieces[piece_id]
        if not self._show_piece_and_options(piece, player.color):
            return True

        x, y, rotation, flip = self._get_piece_placement_input(piece)
        return self._process_piece_placement(player, piece, piece_id, x, y, rotation, flip)

    def _show_piece_and_options(self, piece: Piece, color: int) -> bool:
        """
        Show selected piece and handle placement options
        
        Args:
            piece (Piece): The selected piece
            color (int): The color of the player
        Returns:
            bool: True if the piece can be placed, False
        """
        clear_screen()
        self.board.display()
        print("\nSelected piece:")
        display_piece(piece, color=color)

        if not self.board.can_place_piece(piece, color):
            print("No valid moves available for this piece!")
            input("Press Enter to continue...")
            return False

        print("\nOptions:")
        for i, option in enumerate(["Place piece", "View possible moves", "Back to selection"], 1):
            print(f"{BORDER_CHARS['vertical']} {i}. {option}")

        option = input("\nChoose an option > ")
        if option == "2":
            self.show_possible_moves(piece, color)
            return False
        elif option == "3" or option != "1":
            return False
        
        return True

    def _process_piece_placement(self, player: Player, piece: Piece, piece_id: int, 
                               x: int, y: int, rotation: int, flip: bool) -> bool:
        """
        Process the actual piece placement
        
        Args:
            player (Player): The current player
            piece (Piece): The selected piece
            piece_id (int): The ID of the piece
            x (int): The x-coordinate for placement
            y (int): The y-coordinate for placement
            rotation (int): The rotation of the piece
            flip (bool): Whether the piece is flipped
        Returns:
            bool: True if the placement was not successful, False otherwise
        """
        # Apply transformations
        if flip:
            piece = piece.flip()
        for _ in range(rotation):
            piece = piece.rotate()

        # Show preview
        preview = self.board.preview_move(piece, x, y, player.color)
        print("\nPlacement preview:")
        self.board.display(preview)

        if input("\nConfirm placement? (y/n): ").lower() != 'y':
            return True

        if not self._place_piece(player, piece, piece_id, x, y, rotation, flip):
            input("\nPress Enter to continue...")
            return True
        
        return False

    def _place_piece(self, player: Player, piece: Piece, piece_id: int, 
                    x: int, y: int, rotation: int, flip: bool) -> bool:
        """
        Place the piece on the board
        
        Args:
            player (Player): The current player
            piece (Piece): The selected piece
            piece_id (int): The ID of the piece
            x (int): The x-coordinate for placement
            y (int): The y-coordinate for placement
            rotation (int): The rotation of the piece
            flip (bool): Whether the piece is flipped
        Returns:
            bool: True if the placement was not successful, False otherwise"""
        
        if not self.board.is_valid_move(piece, x, y, player.color):
            print(f"\n{COLORS[player.color]}Invalid move! Try again.{COLORS[0]}")
            return False

        if self.is_online:
            self.network_client.send_move({
                'piece_id': piece_id,
                'x': x, 'y': y,
                'rotation': rotation,
                'flip': flip,
                'color': player.color
            })
        else:
            self.board.place_piece(piece, x, y, player.color)
            player.remaining_pieces.remove(piece_id)
            self.current_player = (self.current_player + 1) % len(self.players)
            print(f"\n{COLORS[player.color]}Piece placed successfully!{COLORS[0]}")
        
        return True

    def _check_game_over(self) -> bool:
        """
        Check if the game is over
        
        Returns:
            bool: True if the game is over, False otherwise
            """
        # First check if all players have no pieces left
        if all(len(p.remaining_pieces) == 0 for p in self.players):
            return True
            
        # Then check if any player with remaining pieces can make a valid move
        for p in self.players:
            if p.remaining_pieces:
                for piece_id in p.remaining_pieces:
                    piece = p.pieces[piece_id]
                    for variant in piece.get_all_variations():
                        if self.board.find_valid_moves(variant, p.color):
                            return False
                            
        # If no player can make a valid move, the game is over
        return True

    def _handle_autosave(self, game_over: bool):
        """
        Handle periodic autosave

        Args:
            game_over (bool): Whether the game is over

        """
        if not game_over and self.current_player == 0:
            save_game(self, "blokus_autosave.json")

    def _handle_game_over_sequence(self):
        """
        Handle the game over sequence and restart option

        Returns:
            None
        """
        self.board.display()
        print("\n🎮 Game Over! 🎮")
        print("\nFinal board state:")
        self.board.display()
        display_final_score(self)
        
        if input("\nWould you like to play again? (y/n): ").lower() == 'y':
            self.reset_game()
            self.play()
        else:
            print("\nThanks for playing! 👋")

    def _create_piece_grid(self, pieces: List[Piece], color: int, pieces_per_row: int = 4) -> List[str]:
        """
        Crée une grille d'affichage des pièces avec un espacement et des bordures appropriés.
        
        Args:
            pieces (List[Piece]): Liste des pièces à afficher.
            color (int): Indice de couleur pour les pièces.
            pieces_per_row (int): Nombre de pièces à afficher par ligne.
        
        Returns:
            List[str]: Liste de chaînes représentant la grille formatée.
        """
        # Group pieces into rows
        rows = [pieces[i:i + pieces_per_row] for i in range(0, len(pieces), pieces_per_row)]
        grid_lines = []
        
        for row_pieces in rows:
            grid_lines.extend(self._create_row_display(row_pieces, color))
            grid_lines.append("")  # Add blank line between rows
        
        return grid_lines

    def _create_row_display(self, row_pieces: List[Piece], color: int) -> List[str]:
        """Creates display lines for a single row of pieces.
        
        Args:
            row_pieces (List[Piece]): List of pieces in a row.
            color (int): Color index for the pieces.
        Returns:
            List[str]: List of formatted lines for the row."""
        max_height = max(len(piece.shape) for piece in row_pieces)
        header_pieces = self._create_header_pieces(row_pieces)
        
        grid_lines = self._create_header_lines(header_pieces)
        grid_lines.extend(self._create_piece_lines(row_pieces, header_pieces, max_height, color))
        grid_lines.append(self._create_bottom_border(row_pieces))
        
        return grid_lines

    def _create_header_pieces(self, row_pieces: List[Piece]) -> List[Tuple[str, str, str, int]]:
        """Creates header information for each piece in a row.
        
        Args:
            row_pieces (List[Piece]): List of pieces in a row.
        Returns:
            List[Tuple[str, str, str, int]]: List of header pieces with formatting information."""
        header_pieces = []
        for piece in row_pieces:
            piece_width = len(piece.shape[0]) * 2 + 3  # +3 for borders and spacing
            header = f"╔{'═' * (piece_width-2)}╗"
            middle = f"║ {piece.piece_id:^{piece_width-4}} ║"
            footer = f"╚{'═' * (piece_width-2)}╝"
            header_pieces.append((header, middle, footer, piece_width))
        return header_pieces

    def _create_header_lines(self, header_pieces: List[Tuple[str, str, str, int]]) -> List[str]:
        """Creates the header lines for a row of pieces.
        
        Args:
            header_pieces (List[Tuple[str, str, str, int]]): List of header pieces with formatting information.
        Returns:
            List[str]: List of formatted header lines."""
        header_line = " ".join(h[0] for h in header_pieces)
        number_line = " ".join(h[1] for h in header_pieces)
        separator_line = " ".join(h[2] for h in header_pieces)
        return [header_line, number_line, separator_line]

    def _create_piece_lines(self, row_pieces: List[Piece], header_pieces: List[Tuple[str, str, str, int]], 
                           max_height: int, color: int) -> List[str]:
        """
        Creates the lines displaying the actual pieces.
        
        Args:
            row_pieces (List[Piece]): List of pieces in a row.
            header_pieces (List[Tuple[str, str, str, int]]): List of header pieces with formatting information.
            max_height (int): Maximum height of the pieces in the row.
            color (int): Color index for the pieces.
        Returns:
            List[str]: List of formatted lines for the pieces.
            """
        
        piece_lines = []
        for row in range(max_height):
            line_parts = []
            for piece_idx, piece in enumerate(row_pieces):
                line = self._create_single_piece_line(piece, header_pieces[piece_idx][3], row, color)
                line_parts.append(line)
            piece_lines.append(" ".join(line_parts))
        return piece_lines

    def _create_single_piece_line(self, piece: Piece, width: int, row: int, color: int) -> str:
        """
        Creates a single line for a piece display.
        
        Args:
            piece (Piece): The piece to display.
            width (int): Width of the piece display.
            row (int): Row index to display.
            color (int): Color index for the piece.
        Returns:
            str: Formatted line for the piece.
        """
        if row < len(piece.shape):
            piece_line = "║ "
            for cell in piece.shape[row]:
                if cell:
                    piece_line += f"{COLORS[color]}■{COLORS[0]} "
                else:
                    piece_line += "· "
            padding = width - len(piece_line) - 1
            return piece_line + " " * padding + "║"
        else:
            return f"║{' ' * (width-2)}║"

    def _create_bottom_border(self, row_pieces: List[Piece]) -> str:
        """
        Creates the bottom border for a row of pieces.
        
        Args:
            row_pieces (List[Piece]): List of pieces in a row.
        Returns:
            str: Formatted bottom border line.
        """
        bottom_borders = []
        for piece in row_pieces:
            width = len(piece.shape[0]) * 2 + 3
            bottom_borders.append(f"╚{'═' * (width-2)}╝")
        return " ".join(bottom_borders)

    def _get_piece_placement_input(self, piece: Piece) -> Tuple[int, int, int, bool]:
        """
        Get and validate piece placement input from user
        
        Args:
            piece (Piece): The piece to place.
        Returns:
            Tuple[int, int, int, bool]: The x-coordinate, y-coordinate, rotation, and flip flag.
            """
        while True:
            try:
                print("\nEnter placement details:")
                x = int(input("Column (x): "))  # Columns as x
                y = int(input("Row (y): "))  # Rows as y
                rotation = int(input("Rotation (0-3): "))
                flip = input("Flip piece? (y/n): ").lower() == 'y'

                if not (0 <= x < self.board.size and 0 <= y < self.board.size):
                    print("Position out of bounds!")
                    continue
                if not (0 <= rotation <= 3):
                    print("Invalid rotation! Must be between 0 and 3.")
                    continue

                # Swap x and y when returning to match the board's internal representation
                return y, x, rotation, flip  # Return y,x instead of x,y
            except ValueError:
                print("Invalid input! Please enter numbers for coordinates and rotation.")

    def show_possible_moves(self, piece: Piece, color: int) -> None:
        """
        Affiche tous les mouvements valides possibles pour une pièce.
        
        Args:
            piece (Piece): La pièce à placer.
            color (int): La couleur du joueur.
        """

        valid_moves = self.board.find_valid_moves(piece, color)
        if not valid_moves:
            print("No valid moves available for this piece!")
            return

        print(f"\nPossible moves for selected piece ({len(valid_moves)} positions):")
        for x, y in valid_moves[:10]: # Show first 10 moves to avoid cluttering
            # Swap x and y when displaying to match user's perspective
            print(f"Position: ({y}, {x})") # y for column, x for row
            preview = self.board.preview_move(piece, x, y, color)
            self.board.display(preview)
            input("Press Enter to see next possible move...")

    def setup_online_game(self, num_players: int, game_id: str = None):
        """
        Setup online multiplayer game
        
        Args:
            num_players (int): Number of players for the game.
            game_id (str): ID of the game to join.
        
        """
        self.network_client = BlokusClient()
        if not self.network_client.connect(num_players, game_id):
            print("Failed to connect to server!")
            return
        
        self.network_client.set_callback(self.handle_network_message)
        self.is_online = True
        print("Waiting for other players to join...")
        self.reset_game(num_players)

    def handle_network_message(self, message: dict):
        """
        Handle messages received from server
        
        Args:
            message (dict): The message received from the server
        """
        message_handlers = {
            'game_start': self._handle_game_start,
            'waiting': self._handle_waiting,
            'move': self._handle_move,
            'error': self._handle_error,
            'player_disconnected': self._handle_player_disconnected
        }
        
        handler = message_handlers.get(message['type'])
        if handler:
            handler(message)

    def _handle_game_start(self, message: dict):
        """
        Handle game start message from server
        
        Args:
            message (dict): The message received from the server
        """
        print("\nAll players connected! Game starting...")
        self.player_number = message['player_number']
        self.current_player = message['current_player']
        self.total_players = message['total_players']
        print(f"You are Player {self.player_number + 1} of {self.total_players}")

    def _handle_waiting(self, message: dict):
        """
        Handle waiting message from server
        
        Args:
            message (dict): The message received from the server
        """
        print(f"\n{message['message']}")

    def _handle_move(self, message: dict):
        """Handle move message from server
        
        Args:
            message (dict): The message received from the server
        """
        piece = self._prepare_piece(message)
        if piece and self._is_valid_move(piece, message):
            self._apply_move(piece, message)

    def _prepare_piece(self, message: dict) -> Optional[Piece]:
        """Prepare piece with transformations based on message
        
        Args:
            message (dict): The message received from the server
        Returns:
            Optional[Piece]: The prepared piece or None
        """
        player = self.players[self.current_player]
        piece = player.pieces[message['piece_id']]
        
        if message['flip']:
            piece = piece.flip()
        for _ in range(message['rotation']):
            piece = piece.rotate()
        
        return piece

    def _is_valid_move(self, piece: Piece, message: dict) -> bool:
        """Check if the move is valid
        
        Args:
            piece (Piece): The piece to place
            message (dict): The message received from the server
        Returns:
            bool: True if the move is valid, False otherwise
        """
        return self.board.is_valid_move(piece, message['x'], message['y'], message['color'])

    def _apply_move(self, piece: Piece, message: dict):
        """
        Apply the move to the game state
        
        Args:
            piece (Piece): The piece to place
            message (dict): The message received from the server
        """
        player = self.players[self.current_player]
        self.board.place_piece(piece, message['x'], message['y'], message['color'])
        player.remaining_pieces.remove(message['piece_id'])
        self.current_player = message['current_player']

    def _handle_error(self, message: dict):
        """
        Handle error message from server
        
        Args:
            message (dict): The message received from the server
        """
        print(f"\nError: {message['message']}")
        input("Press Enter to continue...")

    def _handle_player_disconnected(self, message: dict):
        """Handle player disconnection message from server
        
        Args:
            message (dict): The message received from the server
        """
        print("\nPlayer disconnected from the game!")
        # Handle disconnection (maybe end game or wait for reconnection)
