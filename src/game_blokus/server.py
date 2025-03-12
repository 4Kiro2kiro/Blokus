import socket
import threading
import json
from typing import Dict, List
import pickle

class BlokusServer:
    def __init__(self, host='0.0.0.0', port=6000):
        """
        Initialize the Blokus server.

        Args:
            host (str): Host address to bind the server. Defaults to '0.0.0.0'.
            port (int): Port number to bind the server. Defaults to 6000.
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(4)  # Max 4 players per game
        
        self.games: Dict[str, Dict] = {}  # game_id -> game_info
        self.clients: Dict[socket.socket, Dict] = {}  # socket -> client_info
        
        print(f"Server started on {host}:{port}")
        
    def start(self):
        """Start accepting client connections"""
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"New connection from {address}")
            
            # Start a new thread to handle this client
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket,)
            )
            client_thread.start()
            
    def handle_client(self, client_socket: socket.socket):
        """
        Handle individual client connection.
        
        Args:
            client_socket (socket.socket): The socket representing the client connection.
        """
        try:
            init_data = self.receive_message(client_socket)
            if init_data.get('type') == 'init':
                self._handle_client_initialization(client_socket, init_data)
            
            self._handle_game_messages(client_socket)
            
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            self.handle_client_disconnect(client_socket)

    def _handle_client_initialization(self, client_socket: socket.socket, init_data: dict):
        """
        Handle initial client connection and game setup.

        Args:
            client_socket (socket.socket): The socket representing the client connection.
            init_data (dict): The initialization data sent by the client.
        """
        player_id = init_data.get('player_id')
        game_id = init_data.get('game_id')
        
        self._register_client(client_socket, player_id, game_id)
        self._setup_or_join_game(client_socket, game_id, init_data.get('num_players', 2))
        self._check_game_start(game_id)

    def _register_client(self, client_socket: socket.socket, player_id: str, game_id: str):
        """
        Register new client in the server.

        Args:
            client_socket (socket.socket): The socket representing the client connection.
            player_id (str): The ID of the player.
            game_id (str): The ID of the game.
        """
        self.clients[client_socket] = {
            'player_id': player_id,
            'game_id': game_id,
            'player_number': None
        }

    def _setup_or_join_game(self, client_socket: socket.socket, game_id: str, num_players: int):
        """
        Setup new game or join existing one.

        Args:
            client_socket (socket.socket): The socket representing the client connection.
            game_id (str): The ID of the game.
            num_players (int): Number of players in the game.
        """
        if game_id not in self.games:
            self.games[game_id] = {
                'players': [],
                'current_player': 0,
                'board_state': None,
                'started': False,
                'num_players': num_players
            }
        
        player_number = len(self.games[game_id]['players'])
        self.clients[client_socket]['player_number'] = player_number
        self.games[game_id]['players'].append(client_socket)
        
        print(f"Player {player_number} joined game {game_id}")

    def _check_game_start(self, game_id: str):
        """
        Check if game can start and notify players.

        Args:
            game_id (str): The ID of the game.
        """
        game = self.games[game_id]
        if len(game['players']) == game['num_players']:
            self._start_game(game_id)
        else:
            self._send_waiting_message(game_id)

    def _start_game(self, game_id: str):
        """
        Initialize and start the game.

        Args:
            game_id (str): The ID of the game.
        """
        game = self.games[game_id]
        print(f"Game {game_id} is starting with {game['num_players']} players")
        game['started'] = True
        game['current_player'] = 0

        for player_socket in game['players']:
            player_num = self.clients[player_socket]['player_number']
            self.send_message(player_socket, {
                'type': 'game_start',
                'player_number': player_num,
                'current_player': 0,
                'total_players': game['num_players']
            })

    def _send_waiting_message(self, game_id: str):
        """
        Send waiting message to all players in the game.
        
        Args:
            game_id (str): The ID of the game.
        """
        game = self.games[game_id]
        waiting_msg = {
            'type': 'waiting',
            'message': f'Waiting for more players to join... ({len(game["players"])}/{game["num_players"]})'
        }
        self.broadcast_to_game(game_id, waiting_msg)

    def _handle_game_messages(self, client_socket: socket.socket):
        """
        Handle ongoing game messages from client.

        Args:
            client_socket (socket.socket): The socket representing the client connection.
        """
        while True:
            data = self.receive_message(client_socket)
            if not data:
                break
                
            game_id = self.clients[client_socket]['game_id']
            game = self.games.get(game_id)
            
            if not game or not game['started']:
                continue
            
            if data.get('type') == 'move':
                self._handle_move(client_socket, game_id, data)

    def _handle_move(self, client_socket: socket.socket, game_id: str, move_data: dict):
        """
        Handle a move from a player.
        
        Args:
            client_socket (socket.socket): The socket representing the client connection.
            game_id (str): The ID of the game.
            move_data (dict): The move data sent by the client.
        """
        game = self.games[game_id]
        player_number = self.clients[client_socket]['player_number']
        current_player = game['current_player']
        
        if player_number == current_player:
            self._process_valid_move(game_id, move_data)
        else:
            self._send_invalid_turn_message(client_socket)

    def _process_valid_move(self, game_id: str, move_data: dict):
        """
        Process and broadcast a valid move.
        
        Args:
            game_id (str): The ID of the game.
            move_data (dict): The move data sent by the client.
        """
        game = self.games[game_id]
        game['current_player'] = (game['current_player'] + 1) % game['num_players']
        
        move_data['current_player'] = game['current_player']
        self.broadcast_to_game(game_id, move_data)

    def _send_invalid_turn_message(self, client_socket: socket.socket):
        """
        Send error message for invalid turn.
        
        Args:
            client_socket (socket.socket): The socket representing the client connection.
        """
        self.send_message(client_socket, {
            'type': 'error',
            'message': 'Not your turn'
        })

    def handle_client_disconnect(self, client_socket: socket.socket):
        """
        Clean up when a client disconnects.

        Args:
            client_socket (socket.socket): The socket representing the client connection.
        """
        if client_socket in self.clients:
            game_id = self.clients[client_socket]['game_id']
            if game_id in self.games:
                self.games[game_id]['players'].remove(client_socket)
                # Notify other players about disconnection
                self.broadcast_to_game(game_id, {
                    'type': 'player_disconnected',
                    'player_id': self.clients[client_socket]['player_id']
                })
                # Remove game if no players left
                if not self.games[game_id]['players']:
                    del self.games[game_id]
            del self.clients[client_socket]
        client_socket.close()
            
    def broadcast_to_game(self, game_id: str, message: dict, exclude=None):
        """
        Send message to all players in a game except excluded socket.

        Args:
            game_id (str): The ID of the game.
            message (dict): The message to send.
            exclude (socket.socket, optional): The socket to exclude from the broadcast. Defaults to None.
        """
        if game_id in self.games:
            for player_socket in self.games[game_id]['players']:
                if player_socket != exclude:
                    self.send_message(player_socket, message)
                
    def send_message(self, client_socket: socket.socket, message: dict):
        """
        Send message to a client.

        Args:
            client_socket (socket.socket): The socket representing the client connection.
            message (dict): The message to send.
        """
        try:
            data = pickle.dumps(message)
            client_socket.send(data)
        except Exception as e:
            print(f"Error sending message: {e}")
            
    def receive_message(self, client_socket: socket.socket) -> dict:
        """
        Receive message from a client.

        Args:
            client_socket (socket.socket): The socket representing the client connection.

        Returns:
            dict: The received message.
        """
        try:
            data = client_socket.recv(4096)
            if data:
                return pickle.loads(data)
        except Exception as e:
            print(f"Error receiving message: {e}")
        return {}

if __name__ == "__main__":
    server = BlokusServer()
    server.start() 