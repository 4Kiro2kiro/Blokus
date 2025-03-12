import socket
import pickle
import threading
from typing import Callable, Optional
import uuid

class BlokusClient:
    def __init__(self, host='10.77.255.43', port=6000):
        """
            fonction pour initier les parametres de la classe BlokusClient
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.game_id: Optional[str] = None
        self.player_id: Optional[str] = None
        self.callback: Optional[Callable] = None
        self.connected = False
        
    def connect(self, num_players: int = None, game_id: str = None) -> bool:
        """
        Connect to server and initialize game.

        Args:
            num_players (int, optional): Number of players for the game. Defaults to None.
            game_id (str, optional): ID of the game to join or create. Defaults to None.

        Returns:
            bool: True if connection is successful, False otherwise.
        """
        try:
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            
            # Generate unique IDs
            self.player_id = str(uuid.uuid4())
            # Use provided game_id or generate a new one
            self.game_id = game_id or str(uuid.uuid4())
            
            # Send initialization data
            init_data = {
                'type': 'init',
                'player_id': self.player_id,
                'game_id': self.game_id,
            }
            if num_players is not None:  # Only include num_players when creating a new game
                init_data['num_players'] = num_players
            
            self.send_message(init_data)
            
            # Start listening thread
            threading.Thread(target=self.receive_messages, daemon=True).start()
            return True
            
        except Exception as e:
            print(f"Connection failed: {e}")
            self.connected = False
            return False
            
    def send_move(self, move_data: dict):
        """
        Send a move to the server.

        Args:
            move_data (dict): Dictionary containing move data.
        """
        if self.connected:
            move_data['type'] = 'move'
            move_data['player_id'] = self.player_id
            self.send_message(move_data)
            
    def update_board(self, board_state):
        """
        Send board update to server.

        Args:
            board_state: Current state of the board.
        """
        if self.connected:
            self.send_message({
                'type': 'board_update',
                'board': board_state,
                'player_id': self.player_id
            })
            
    def send_message(self, message: dict):
        """
        Send message to server.

        Args:
            message (dict): Dictionary containing the message data.
        """
        try:
            data = pickle.dumps(message)
            self.client_socket.send(data)
        except Exception as e:
            print(f"Error sending message: {e}")
            self.connected = False
            
    def receive_messages(self):
        """Continuously receive messages from server"""
        while self.connected:
            try:
                data = self.client_socket.recv(4096)
                if data:
                    message = pickle.loads(data)
                    if self.callback:
                        self.callback(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.connected = False
                break
                
    def set_callback(self, callback: Callable):
        """
        Set callback function for received messages.

        Args:
            callback (Callable): Function to call when a message is received.
        """
        self.callback = callback
        
    def close(self):
        """Close the connection"""
        self.connected = False
        self.client_socket.close() 
