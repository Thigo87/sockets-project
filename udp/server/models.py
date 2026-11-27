from socket import *
from time import localtime
from core.tic_tac_toe import *

class Client:
    def __init__(self, address, piece): #criador do objeto
        self.address = address
        self.piece = piece

    def __eq__(self, other): #para a verificação dos endereços e não ocorrer o erro do código "achar" que não são equivalentes
        if isinstance(other, Client):
            return self.address == other.address
        
        return self.address == other

class Server:
    def __init__(self, room_name, port):
        self.room_name = room_name
        self.port = port
        self.players = []
        self.board = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        self.turn_index = 0
        self.game_started = False

        self.serverUDP = socket(AF_INET, SOCK_DGRAM)
        self.serverUDP.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.serverUDP.bind(("", port))

    def get_timestamp(self):
        t = localtime()
        return f"[{t.tm_hour}:{t.tm_min}:{t.tm_sec} - {t.tm_mday}/{t.tm_mon}/{t.tm_year}]"

    def send_to(self, client, msg):
        self.serverUDP.sendto(msg.encode(), client.address)

    def broadcast(self, msg):
        for player in self.players:
            self.send_to(player, msg)

    def reset_room(self):
        self.players = []
        self.board = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        self.turn_index = 0
        self.game_started = False

    def add_player(self, address):
        if address in self.players:
            return None

        if len(self.players) >= 2:
            self.serverUDP.sendto("FULL: This room is already full".encode(), address)
            return None

        piece = "X" if len(self.players) == 0 else "O"
        new_client = Client(address, piece)
        self.players.append(new_client) 
        print(f"[Port {self.port} {self.get_timestamp()} => Player {address[0]}:{address[1]}] connected as {piece}")

        if len(self.players) == 1:
            self.send_to(new_client, f"WAIT: Connected as '{piece}'. Waiting for second player...")

        elif len(self.players) == 2:
            self.game_started = True
            starter_piece = "O" if start_piece() == 0 else "X"
            self.turn_index = 0 if self.players[0].piece == starter_piece else 1

            starter = self.players[self.turn_index]
            waiting = self.players[1 - self.turn_index]
            board_str = formatBoard(self.board)

            self.send_to(starter, f"TURN:\nYou are '{starter.piece}'. '{starter_piece}' will start!\n\n{board_str}\n\nPlease input a position for {starter.piece}: ")
            self.send_to(waiting, f"WAIT:\nYou are '{waiting.piece}'. '{starter_piece}' will start!\n\n{board_str}\n\nWaiting for {starter.piece}")

    def handle_message(self, message, address):
        if message == "Hello":
            self.add_player(address)
            return None

        if address not in self.players:
            self.serverUDP.sendto("ERROR: Send Hello to connect first.".encode(), address)
            return None
        
        if not self.game_started:
            self.serverUDP.sendto("WAIT: Still waiting for second player...".encode(), address)
            return None

        current_player = self.players[self.turn_index]
        if address != current_player.address:
            self.serverUDP.sendto("WAIT: Not your turn!".encode(), address)
            return None

        if not playerMove(self.board, message, current_player.piece):  
            self.send_to(current_player, f"TURN: Invalid position! Please input a number for {current_player.piece} position: ")
            return None

        board_str = formatBoard(self.board)
        conclusion = win(self.board)

        if conclusion[1]:
            self.broadcast(f"END:\n\n{board_str}\n\n{conclusion[0]} wins!")
            print(f"[Port {self.port}] {self.get_timestamp()} => {conclusion[0]} wins!")
            self.reset_room()
            return None

        if tie(self.board):
            self.broadcast(f"END:\n\n{board_str}\n\nIT'S A TIE!")
            print(f"[Port {self.port}] {self.get_timestamp()} => IT'S A TIE!")
            self.reset_room()
            return None

        self.turn_index = 1 - self.turn_index
        next_player = self.players[self.turn_index]

        self.send_to(current_player, f"WAIT:\n\n{board_str}\n\nWaiting for '{next_player.piece}' to play...")
        self.send_to(next_player, f"TURN:\n\n{board_str}\n\nPlease input a number for {next_player.piece} position: ")

    def receive_connection(self):
        print(f"{self.get_timestamp()} Server localhost:{self.port} ({self.room_name}) is ready to receive")

        while True:
            try:
                message, address = self.serverUDP.recvfrom(2048)
                message = message.decode().strip()
                print(f"[Port {self.port}] {self.get_timestamp()} => Received message: {message}\nFrom: {address[0]}:{address[1]}")
                self.handle_message(message, address)

            except Exception as e:
                print(f"{self.get_timestamp()} An error occurred on port {self.port}: {e}")