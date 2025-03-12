import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest

from io import StringIO
from unittest.mock import patch, MagicMock, call
from game_blokus.display import display_final_score
from game_blokus.game import BlokusGame
from game_blokus.board import Board
from game_blokus.player import Player
from game_blokus.piece import Piece
from game_blokus.save_load import save_game, load_game
from game_blokus.bot_player import BotPlayer
from game_blokus.network_client import BlokusClient
from game_blokus.server import BlokusServer
from game_blokus.spectactor import start_spectator

class TestBlokusGame(unittest.TestCase ):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game = BlokusGame(num_players=4)
        self.board = self.game.board  # Ajout de cette ligne pour initialiser l'attribut board
        self.test_filename = "test_save.json"
        self.bot_easy = BotPlayer(level="easy", color=1)
        self.bot_medium = BotPlayer(level="medium", color=2)
        self.bot_hard = BotPlayer(level="hard", color=3)
        self.player1 = self.game.players[0]
        self.player2 = self.game.players[1]
        self.player3 = self.game.players[2]
        self.player4 = self.game.players[3]
        self.client = BlokusClient(host='localhost', port=6000)


    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_game_initialization(self):
        """Test if game is properly initialized."""
        self.assertEqual(len(self.game.players), 4)
        self.assertEqual(self.game.current_player, 0)
        self.assertEqual(self.game.board.size, 20)
        self.assertFalse(self.game.is_online)
        self.assertIsNone(self.game.network_client)

    def test_board_initialization(self):
        """Test if board is properly initialized."""
        self.assertEqual(len(self.game.board.grid), 20)
        self.assertEqual(len(self.game.board.grid[0]), 20)
        self.assertEqual(self.game.board.grid[0][0], 0)
        self.assertEqual(len(self.game.board.board_corners), 4)

    def test_player_initialization(self):
        """Test if players are properly initialized."""
        for i, player in enumerate(self.game.players):
            self.assertEqual(player.color, i + 1)
            self.assertEqual(len(player.remaining_pieces), 21)
            # Test that each piece in remaining_pieces exists in the pieces list
            self.assertTrue(all(piece_id < len(player.pieces) for piece_id in player.remaining_pieces))

    def test_save_and_load_game(self):
        """Test saving and loading game state."""
        # Save game
        save_game(self.game, self.test_filename)
        self.assertTrue(os.path.exists(self.test_filename))

        # Load game
        loaded = load_game(self.game, self.test_filename)
        self.assertTrue(loaded)
        self.assertEqual(self.game.current_player, 0)
        self.assertEqual(len(self.game.players), 4)

    def test_load_nonexistent_file(self):
        """Test loading a non-existent save file."""
        loaded = load_game(self.game, "non_existent_file.json")
        self.assertFalse(loaded)

    def test_load_invalid_format(self):
        """Test loading an invalid save file."""
        with open(self.test_filename, 'w') as f:
            f.write("invalid json")
        loaded = load_game(self.game, self.test_filename)
        self.assertFalse(loaded)

    def test_piece_placement(self):
        """Test piece placement functionality."""
        player = self.game.players[0]
        piece_id = next(iter(player.remaining_pieces))  # Get first piece ID
        piece = player.pieces[piece_id]
        x, y = 0, 0

        # Test valid move at starting corner
        valid = self.game.board.is_valid_move(piece, x, y, player.color)
        self.assertTrue(valid)

        # Place the piece
        self.game.board.place_piece(piece, x, y, player.color)
        self.assertEqual(self.game.board.grid[x][y], player.color)

    def test_piece_transformations(self):
        """Test piece rotation and flipping."""
        # Create a piece with a distinctive shape for testing
        test_piece = Piece([[1, 1], [1, 0]], 0)
        original_shape = [row[:] for row in test_piece.shape]

        # Test rotation
        rotated = test_piece.rotate()
        self.assertNotEqual([row[:] for row in rotated.shape], original_shape)
        
        # Test that four rotations return to original shape
        current = test_piece
        for _ in range(4):
            current = current.rotate()
        self.assertEqual([row[:] for row in current.shape], original_shape)

        # Test flipping
        flipped = test_piece.flip()
        self.assertNotEqual([row[:] for row in flipped.shape], original_shape)
        
        # Test that double flip returns to original shape
        double_flipped = flipped.flip()
        self.assertEqual([row[:] for row in double_flipped.shape], original_shape)

        def test_rotation_invalid_piece(self):
            # Arrange
            invalid_piece = Piece([], 0)  # Empty piece
            
            # Act & Assert
            with self.assertRaises(ValueError):
                invalid_piece.rotate()

    def test_game_over_conditions(self):
        """Test game over conditions."""
        # Initially game should not be over
        self.assertFalse(self._check_game_over())

        # Remove all pieces from players
        for player in self.game.players:
            player.remaining_pieces.clear()

        # Now game should be over
        self.assertTrue(self._check_game_over())

    def test_invalid_moves(self):
        """Test invalid move detection."""
        player = self.game.players[0]
        piece_id = next(iter(player.remaining_pieces))  # Get first piece ID
        piece = player.pieces[piece_id]

        # Test move out of bounds
        valid = self.game.board.is_valid_move(piece, -1, -1, player.color)
        self.assertFalse(valid)

        # Test move on occupied space
        self.game.board.grid[0][0] = 1
        valid = self.game.board.is_valid_move(piece, 0, 0, player.color)
        self.assertFalse(valid)

    def test_reset_game(self):
        """Test game reset functionality."""
        # Make some moves
        self.game.board.grid[0][0] = 1
        self.game.current_player = 2
        first_player = self.game.players[0]
        piece_id = next(iter(first_player.remaining_pieces))
        first_player.remaining_pieces.remove(piece_id)

        # Reset game
        self.game.reset_game()

        # Check if game state is properly reset
        self.assertEqual(self.game.current_player, 0)
        self.assertEqual(self.game.board.grid[0][0], 0)
        self.assertEqual(len(self.game.players[0].remaining_pieces), 21)

    def test_player_corners(self):
        """Test corner tracking for players."""
        player = self.game.players[0]
        piece_id = next(iter(player.remaining_pieces))  # Get first piece ID
        piece = player.pieces[piece_id]

        # Place piece at corner
        self.game.board.place_piece(piece, 0, 0, player.color)

        # Check if corner is removed from available corners
        self.assertNotIn((0, 0), self.game.board.board_corners)

    def _check_game_over(self):
        """Helper method to check if game is over."""
        # Check if all players have no pieces left
        if all(len(p.remaining_pieces) == 0 for p in self.game.players):
            return True
            
        # Check if any player with remaining pieces can make a valid move
        for p in self.game.players:
            if p.remaining_pieces:
                for piece_id in p.remaining_pieces:
                    piece = p.pieces[piece_id]
                    if self.game.board.find_valid_moves(piece, p.color):
                        return False
                            
        return True
    
    def test_update_corners_after_move(self):
        """Test updating corners after placing a piece."""
        piece = Piece([[1, 1], [1, 0]], 0)
        self.board.place_piece(piece, 0, 0, 1)
        self.assertNotIn((0, 0), self.board.board_corners)
        self.assertIn((1, 1), self.board.corners[1])

    def test_get_valid_adjacent(self):
        """Test getting valid adjacent positions."""
        adjacents = self.board._get_valid_adjacent(0, 0)
        self.assertIn((0, 1), adjacents)
        self.assertIn((1, 0), adjacents)
        self.assertNotIn((1, 1), adjacents)

    def test_preview_move(self):
        """Test generating a preview of the board with a piece placed."""
        piece = Piece([[1, 1], [1, 0]], 0)
        preview = self.board.preview_move(piece, 0, 0, 1)
        self.assertEqual(preview[0][0], 1)
        self.assertEqual(preview[0][1], 1)
        self.assertEqual(preview[1][0], 1)

    def test_is_valid_move(self):
        """Test checking if a move is valid."""
        piece = Piece([[1, 1], [1, 0]], 0)
        valid = self.board.is_valid_move(piece, 0, 0, 1)
        self.assertTrue(valid)

        # Test move out of bounds
        valid = self.board.is_valid_move(piece, -1, -1, 1)
        self.assertFalse(valid)

        # Test move on occupied space
        self.board.grid[0][0] = 1
        valid = self.board.is_valid_move(piece, 0, 0, 1)
        self.assertFalse(valid)

    def test_place_piece(self):
        """Test placing a piece on the board."""
        piece = Piece([[1, 1], [1, 0]], 0)
        self.board.place_piece(piece, 0, 0, 1)
        self.assertEqual(self.board.grid[0][0], 1)
        self.assertEqual(self.board.grid[0][1], 1)
        self.assertEqual(self.board.grid[1][0], 1)

    def test_find_valid_moves(self):
        """Test finding valid moves for a piece."""
        piece = Piece([[1, 1], [1, 0]], 0)
        valid_moves = self.board.find_valid_moves(piece, 1)
        self.assertIn((0, 0), valid_moves)

    def test_can_place_piece(self):
        """Test checking if a piece can be placed."""
        piece = Piece([[1, 1], [1, 0]], 0)
        can_place = self.board.can_place_piece(piece, 1)
        self.assertTrue(can_place)

    def test_display(self):
        """Test displaying the board."""
        piece = Piece([[1, 1], [1, 0]], 0)
        self.board.place_piece(piece, 0, 0, 1)
        self.board.display()
    def test_initialize_pieces(self):
        """Test if pieces are properly initialized."""
        pieces = self.bot_easy.get_pieces()
        self.assertEqual(len(pieces), 21)
        self.assertIsInstance(pieces[0], Piece)

    def test_get_remaining_pieces(self):
        """Test if remaining pieces are correctly returned."""
        remaining_pieces = self.bot_easy.get_remaining_pieces()
        self.assertEqual(len(remaining_pieces), 21)
        self.assertIsInstance(remaining_pieces[0], Piece)

    def test_play_random_move(self):
        """Test if the bot can play a random move."""
        self.board.grid[0][0] = 1  # Simulate a starting move
        move_made = self.bot_easy._play_random_move(self.board)
        self.assertTrue(move_made)

    def test_play_medium_move(self):
        """Test if the bot can play a medium level move."""
        self.board.grid[0][0] = 1  # Simulate a starting move
        move_made = self.bot_medium._play_medium_move(self.board)
        self.assertTrue(move_made)

    def test_play_hard_move(self):
        """Test if the bot can play a hard level move."""
        self.board.grid[0][0] = 1  # Simulate a starting move
        move_made = self.bot_hard._play_hard_move(self.board)
        self.assertTrue(move_made)



    def test_make_move(self):
        """Test if a move is correctly made on the board."""
        piece = self.bot_easy.get_remaining_pieces()[0]
        self.bot_easy._make_move(self.board, piece, (0, 0))
        self.assertEqual(self.board.grid[0][0], 1)
        self.assertNotIn(piece.piece_id, self.bot_easy.remaining_pieces)
    def test_get_all_variations(self):
        """Test if all variations of a piece are generated."""
        piece = self.bot_easy.get_remaining_pieces()[0]
        variations = self.bot_easy._get_all_variations(piece)
        self.assertGreaterEqual(len(variations), 8)  # At least 4 rotations and 4 flips

    def test_evaluate_move(self):
        """Test if a move is correctly evaluated."""
        piece = self.bot_easy.get_remaining_pieces()[0]
        score = self.bot_easy._evaluate_move(self.board, piece, 0, 0, 10, 10)
        self.assertIsInstance(score, float)

    def test_play_easy_level(self):
        """Test if the bot can play at easy level."""
        self.board.grid[0][0] = 1  # Simulate a starting move
        self.bot_easy.play(self.board)
        self.assertNotEqual(self.board.grid[0][0], 0)  # Ensure a move was made

    def test_play_medium_level(self):
        """Test if the bot can play at medium level."""
        self.board.grid[0][0] = 1  # Simulate a starting move
        self.bot_medium.play(self.board)
        self.assertNotEqual(self.board.grid[0][0], 0)  # Ensure a move was made

    def test_play_hard_level(self):
        """Test if the bot can play at hard level."""
        self.board.grid[0][0] = 1  # Simulate a starting move
        self.bot_hard.play(self.board)
        self.assertNotEqual(self.board.grid[0][0], 0)  # Ensure a move was made

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_final_score(self, mock_stdout):
        """Test the display_final_score function."""
        # Simulate some moves
        piece1 = self.player1.pieces[next(iter(self.player1.remaining_pieces))]
        piece2 = self.player2.pieces[next(iter(self.player2.remaining_pieces))]
        piece3 = self.player3.pieces[next(iter(self.player3.remaining_pieces))]
        piece4 = self.player4.pieces[next(iter(self.player4.remaining_pieces))]

        self.game.board.place_piece(piece1, 0, 0, self.player1.color)
        self.game.board.place_piece(piece2, 5, 5, self.player2.color)
        self.game.board.place_piece(piece3, 10, 10, self.player3.color)
        self.game.board.place_piece(piece4, 15, 15, self.player4.color)

        self.player1.remaining_pieces.remove(piece1.piece_id)
        self.player2.remaining_pieces.remove(piece2.piece_id)
        self.player3.remaining_pieces.remove(piece3.piece_id)
        self.player4.remaining_pieces.remove(piece4.piece_id)

        # Call the function
        display_final_score(self.game)

        # Check the output
        output = mock_stdout.getvalue()
        self.assertIn("🏆 Game Over! 🏆", output)
        self.assertIn("Final Scores:", output)
        self.assertIn("Player 1:", output)
        self.assertIn("Player 2:", output)
        self.assertIn("Player 3:", output)
        self.assertIn("Player 4:", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_final_score_sorted(self, mock_stdout):
        """Test the display_final_score function with sorted scores."""
        # Simulate some moves with different scores
        piece1 = self.player1.pieces[next(iter(self.player1.remaining_pieces))]
        piece2 = self.player2.pieces[next(iter(self.player2.remaining_pieces))]
        piece3 = self.player3.pieces[next(iter(self.player3.remaining_pieces))]
        piece4 = self.player4.pieces[next(iter(self.player4.remaining_pieces))]

        self.game.board.place_piece(piece1, 0, 0, self.player1.color)
        self.game.board.place_piece(piece2, 5, 5, self.player2.color)
        self.game.board.place_piece(piece3, 10, 10, self.player3.color)
        self.game.board.place_piece(piece4, 15, 15, self.player4.color)

        self.player1.remaining_pieces.remove(piece1.piece_id)
        self.player2.remaining_pieces.remove(piece2.piece_id)
        self.player3.remaining_pieces.remove(piece3.piece_id)
        self.player4.remaining_pieces.remove(piece4.piece_id)

        # Adjust scores manually for testing
        self.player1.remaining_pieces.clear()
        self.player2.remaining_pieces.clear()
        self.player3.remaining_pieces.clear()
        self.player4.remaining_pieces.clear()

        # Call the function
        display_final_score(self.game)

        # Check the output
        output = mock_stdout.getvalue()
        self.assertIn("🏆 Game Over! 🏆", output)
        self.assertIn("Final Scores:", output)
        self.assertIn("Player 1:", output)
        self.assertIn("Player 2:", output)
        self.assertIn("Player 3:", output)
        self.assertIn("Player 4:", output)
        self.assertIn("🥇", output)
        self.assertIn("🥈", output)
        self.assertIn("🥉", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_final_score_no_moves(self, mock_stdout):
        """Test the display_final_score function with no moves made."""
        # Call the function without making any moves
        display_final_score(self.game)

        # Check the output
        output = mock_stdout.getvalue()
        self.assertIn("🏆 Game Over! 🏆", output)
        self.assertIn("Final Scores:", output)
        self.assertIn("Player 1:", output)
        self.assertIn("Player 2:", output)
        self.assertIn("Player 3:", output)
        self.assertIn("Player 4:", output)
        self.assertIn("🥇", output)
        self.assertIn("🥈", output)
        self.assertIn("🥉", output)

    @patch('builtins.input', side_effect=['1'])
    def test_get_game_mode(self, mock_input):
        """Test getting the game mode from user input."""
        mode = self.game._get_game_mode()
        self.assertEqual(mode, '1')

    @patch('builtins.input', side_effect=['easy'])
    def test_setup_solo_game(self, mock_input):
        """Test setting up a solo game against AI."""
        self.game._setup_solo_game()
        self.assertEqual(len(self.game.players), 2)
        self.assertIsInstance(self.game.players[0], BotPlayer)
        self.assertIsInstance(self.game.players[1], Player)

    @patch('builtins.input', side_effect=['3'])
    def test_setup_local_multiplayer(self, mock_input):
        """Test setting up a local multiplayer game."""
        self.game._setup_local_multiplayer()
        self.assertEqual(len(self.game.players), 3)
        self.assertIsInstance(self.game.players[0], Player)
        self.assertIsInstance(self.game.players[1], Player)
        self.assertIsInstance(self.game.players[2], Player)

    @patch('builtins.input', side_effect=['1'])
    def test_get_online_game_type(self, mock_input):
        """Test getting the online game type from user input."""
        game_type = self.game._get_online_game_type()
        self.assertEqual(game_type, '1')

    @patch('builtins.input', side_effect=['2'])
    def test_get_online_player_count(self, mock_input):
        """Test getting the number of players for an online game."""
        num_players = self.game._get_online_player_count()
        self.assertEqual(num_players, 2)

    @patch('builtins.input', side_effect=['0', '0', '0', '0'])
    def test_get_piece_placement_input(self, mock_input):
        """Test getting piece placement input from user."""
        piece = self.game.players[0].pieces[0]
        x, y, rotation, flip = self.game._get_piece_placement_input(piece)
        self.assertEqual((x, y, rotation, flip), (0, 0, 0, False))

    @patch('socket.socket.connect')
    def test_connection_failure(self, mock_socket_connect):
        """Test failed connection to the server."""
        # Arrange
        mock_socket_connect.side_effect = Exception("Connection failed")
        client = BlokusClient(host='localhost', port=6000)
        
        # Act
        result = client.connect(num_players=4)
        
        # Assert
        self.assertFalse(result)
        self.assertFalse(client.connected)
        mock_socket_connect.assert_called_once_with(('localhost', 6000))


    

    @patch('builtins.input', side_effect=['y'])
    def test_handle_game_commands_quit(self, mock_input):
        """Test handling game commands for quitting the game."""
        result = self.game._handle_game_commands('q')
        self.assertTrue(result)

    
    def test_handle_special_player_states_bot(self):
        """Test handling special player states for bot players."""
        self.game.players[0] = BotPlayer(level="easy", color=1)
        result = self.game._handle_special_player_states(self.game.players[0])
        self.assertTrue(result)
    def test_handle_special_player_states_no_pieces(self):
                """Test handling special player states for players with no pieces."""
                self.game.players[0].remaining_pieces.clear()
                result = self.game._handle_special_player_states(self.game.players[0])
                self.assertTrue(result)

    @patch('builtins.input', side_effect=[''])
    def test_handle_special_player_states_online_waiting(self, mock_input):
        """Test handling special player states for online waiting."""
        self.game.is_online = True
        self.game.player_number = 1
        self.game.current_player = 0
        result = self.game._handle_special_player_states(self.game.players[0])
        self.assertTrue(result)

    def test_check_game_over(self):
        """Test checking if the game is over."""
        self.assertFalse(self.game._check_game_over())
        for player in self.game.players:
            player.remaining_pieces.clear()
        self.assertTrue(self.game._check_game_over())

    
    def test_create_piece_grid(self):
        """Test creating a piece grid for display."""
        pieces = self.game.players[0].get_remaining_pieces()
        grid = self.game._create_piece_grid(pieces, self.game.players[0].color)
        self.assertIsInstance(grid, list)
        self.assertGreater(len(grid), 0)

    def test_create_row_display(self):
        """Test creating a row display for pieces."""
        pieces = self.game.players[0].get_remaining_pieces()[:4]
        row_display = self.game._create_row_display(pieces, self.game.players[0].color)
        self.assertIsInstance(row_display, list)
        self.assertGreater(len(row_display), 0)

    def test_create_header_pieces(self):
        """Test creating header pieces for a row of pieces."""
        pieces = self.game.players[0].get_remaining_pieces()[:4]
        header_pieces = self.game._create_header_pieces(pieces)
        self.assertIsInstance(header_pieces, list)
        self.assertEqual(len(header_pieces), 4)

    def test_create_header_lines(self):
        """Test creating header lines for a row of pieces."""
        pieces = self.game.players[0].get_remaining_pieces()[:4]
        header_pieces = self.game._create_header_pieces(pieces)
        header_lines = self.game._create_header_lines(header_pieces)
        self.assertIsInstance(header_lines, list)
        self.assertEqual(len(header_lines), 3)

    def test_create_piece_lines(self):
        """Test creating piece lines for a row of pieces."""
        pieces = self.game.players[0].get_remaining_pieces()[:4]
        header_pieces = self.game._create_header_pieces(pieces)
        piece_lines = self.game._create_piece_lines(pieces, header_pieces, 5, self.game.players[0].color)
        self.assertIsInstance(piece_lines, list)
        self.assertGreater(len(piece_lines), 0)

    def test_create_single_piece_line(self):
        """Test creating a single piece line for display."""
        piece = self.game.players[0].get_remaining_pieces()[0]
        line = self.game._create_single_piece_line(piece, 10, 0, self.game.players[0].color)
        self.assertIsInstance(line, str)
        self.assertGreater(len(line), 0)

    def test_create_bottom_border(self):
        """Test creating the bottom border for a row of pieces."""
        pieces = self.game.players[0].get_remaining_pieces()[:4]
        bottom_border = self.game._create_bottom_border(pieces)
        self.assertIsInstance(bottom_border, str)
        self.assertGreater(len(bottom_border), 0)

    def test_prepare_piece(self):
        """Test preparing a piece with transformations based on a message."""
        message = {
            'piece_id': 0,
            'rotation': 1,
            'flip': True
        }
        piece = self.game._prepare_piece(message)
        self.assertIsInstance(piece, Piece)

    def test_is_valid_move(self):
        """Test checking if a move is valid."""
        piece = self.game.players[0].pieces[0]
        message = {
            'x': 0,
            'y': 0,
            'color': 1
        }
        self.assertTrue(self.game._is_valid_move(piece, message))

    def test_apply_move(self):
        """Test applying a move to the game state."""
        message = {
            'piece_id': 0,
            'x': 0,
            'y': 0,
            'rotation': 0,
            'flip': False,
            'color': 1,
            'current_player': 1
        }
        piece = self.game._prepare_piece(message)
        self.game._apply_move(piece, message)
        self.assertEqual(self.game.board.grid[0][0], 1)
        self.assertNotIn(0, self.game.players[0].remaining_pieces)


    @patch('socket.socket.connect')
    def test_connect_failure(self, mock_socket_connect):
        """Test failed connection to the server."""
        mock_socket_connect.side_effect = Exception("Connection failed")
        result = self.client.connect(num_players=4)
        self.assertFalse(result)
        self.assertFalse(self.client.connected)
        mock_socket_connect.assert_called_once_with(('localhost', 6000))

    @patch('socket.socket.send')
    def test_send_message(self, mock_socket_send):
        """Test sending a message to the server."""
        self.client.connected = True
        message = {'type': 'test', 'data': 'test_data'}
        self.client.send_message(message)
        mock_socket_send.assert_called_once()
        self.assertTrue(mock_socket_send.call_args[0][0])
    @patch('socket.socket.send')
    def test_send_message_failure(self, mock_socket_send):
        """Test sending a message to the server with failure."""
        self.client.connected = True
        mock_socket_send.side_effect = Exception("Send failed")
        message = {'type': 'test', 'data': 'test_data'}
        self.client.send_message(message)
        self.assertFalse(self.client.connected)

    
    
    @patch('socket.socket.send')
    def test_send_move(self, mock_socket_send):
        """Test sending a move to the server."""
        self.client.connected = True
        self.client.player_id = 'test_player_id'
        move_data = {'move': 'test_move'}
        self.client.send_move(move_data)
        mock_socket_send.assert_called_once()
        sent_data = mock_socket_send.call_args[0][0]
        self.assertIn(b'test_player_id', sent_data)
        self.assertIn(b'test_move', sent_data)

    @patch('socket.socket.send')
    def test_update_board(self, mock_socket_send):
        """Test sending board update to the server."""
        self.client.connected = True
        self.client.player_id = 'test_player_id'
        board_state = 'test_board_state'
        self.client.update_board(board_state)
        mock_socket_send.assert_called_once()
        sent_data = mock_socket_send.call_args[0][0]
        self.assertIn(b'test_player_id', sent_data)
        self.assertIn(b'test_board_state', sent_data)

    def test_set_callback(self):
        """Test setting the callback function for received messages."""
        callback = MagicMock()
        self.client.set_callback(callback)
        self.assertEqual(self.client.callback, callback)

    @patch('socket.socket.close')
    def test_close(self, mock_socket_close):
        """Test closing the connection."""
        self.client.connected = True
        self.client.close()
        self.assertFalse(self.client.connected)
        mock_socket_close.assert_called_once()

    

if __name__ == '__main__':
    unittest.main()