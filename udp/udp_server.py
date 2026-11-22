from socket import *
import threading
from json_manipulation import *
from time import sleep, localtime
from tic_tac_toe import *

board = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

rooms = {}
active_ports = set()

def receive_connection(port):
    serverUDP = socket(AF_INET, SOCK_DGRAM)
    serverUDP.bind(("", port))
    print(f"[{localtime().tm_hour}:{localtime().tm_min}:{localtime().tm_sec} - {localtime().tm_mday}/{localtime().tm_mon}/{localtime().tm_year}] Server localhost:{port} is ready to receive")

    while True:
        try:
            message, address = serverUDP.recvfrom(2048) #ajustar a quantidade de bits
            message = message.decode()
            print(f"[Port {port}] [{localtime().tm_hour}:{localtime().tm_min}:{localtime().tm_sec} - {localtime().tm_mday}/{localtime().tm_mon}/{localtime().tm_year}] => Received message: {message}\nFrom: {address[0]}:{address[1]}")
            serverUDP.sendto("Message received!".encode(), address)

        except Exception as e:
            print(f"[{localtime().tm_hour}:{localtime().tm_min}:{localtime().tm_sec} - {localtime().tm_mday}/{localtime().tm_mon}/{localtime().tm_year}] An error occurred on port {port}: {e}")

def update_rooms(file):
    global rooms
    while True:
        try:
            current_rooms = read_data(file)
            if isinstance(current_rooms, dict):
                rooms = current_rooms
                
                for _, info in rooms.items():
                    port = int(info[1])
                    if port not in active_ports:
                        active_ports.add(port)
                        t = threading.Thread(target=receive_connection, args=(port,))
                        t.start()
        
        except Exception as e:
            print(f"[{localtime().tm_hour}:{localtime().tm_min}:{localtime().tm_sec} - {localtime().tm_mday}/{localtime().tm_mon}/{localtime().tm_year}] An error occurred while reading JSON: {e}")
        
        sleep(0.1)

t2 = threading.Thread(target=update_rooms, args=("rooms.json",), daemon=True)
t2.start()

while True:
    sleep(1)
